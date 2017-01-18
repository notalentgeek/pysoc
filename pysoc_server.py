"""pysoc_server

Usage:
    pysoc_server.py (--help | -h)
    pysoc_server.py (--version | -v)
    pysoc_server.py <dba> [--dbn=<dbnv>|--dbp=<dbpv>|--tout=<toutv>]...
    pysoc_server.py

Options:
    --help -h           Refer to help manual.
    --version -v        Refer to this version of application.

    dba                 RethinkDB address [default: 127.0.0.1].
    --dbn=<dbnv>        RethinkDB database name [default: sociometric_server]
    --dbp=<dbpv>        RethinkDB port [default: 28015].
    --tout=<toutv>      RethinkDB connection time out [default: 1]

"""
from   docopt         import docopt          as doc
from   flask          import Flask
from   flask          import render_template
from   flask_socketio import emit
from   flask_socketio import SocketIO        as sio
from   socket         import socket

import rethinkdb      as     r

def ConnDB(_dba, _dbn,
    _dbp, _timeout):

    print("trying to establish database connection")

    conn = r.connect(
        host=_dba, port=_dbp,
        timeout=_timeout)

    db = r.db(_dbn)

    return [conn, db]

class Main(object):

    def __init__(self, _docArgs):

        #print(_docArgs)
        #print(_docArgs["<dba>"])
        #print(_docArgs["--dbn"][0])
        #print(_docArgs["--dbp"][0])
        #print(_docArgs["--tout"][0])

        self.dbAddress  = _docArgs["<dba>"];
        self.dbName     = _docArgs["--dbn"][0];
        self.dbPort     = int(_docArgs["--dbp"][0]);
        self.timeout    = int(_docArgs["--tout"][0]);

        self.app        = Flask(__name__)
        self.sIO        = sio(self.app)

        self.cDB        = None
        self.conn       = None
        self.db         = None

        try:

            self.cDB    = ConnDB(
                self.dbAddress,
                self.dbName,
                self.dbPort,
                self.timeout
            )
            self.conn   = self.cDB[0]
            self.db     = self.cDB[1]

        except r.errors.ReqlTimeoutError as error: print(error)

        self.AddRoute()
        self.sIO.run(self.app)

    def AddRoute(self):

        @self.app.route("/")
        def index():
            return render_template("index.html")
        @self.app.route("/api/client")
        def api_client():
            return str(list(self.db.table("client_name").run(self.conn)))
        @self.app.route("/api/cam/<_clientName>")
        def api_cam(_clientName):
            return str(list(self.db.table(_clientName + "_cam").run(self.conn)))
        @self.app.route("/api/ir/<_clientName>")
        def api_ir(_clientName):
            return str(list(self.db.table(_clientName + "_ir").run(self.conn)))
        @self.app.route("/api/mic/<_clientName>")
        def api_mic(_clientName):
            return str(list(self.db.table(_clientName + "_mic").run(self.conn)))

        @self.sIO.on("latestInputRequest")
        def LatestInput():

            if self.cDB == None:

                clientList      = []
                latestInput     = None
                latestInputComp = None

                clientNameArray = None
                camTable        = None
                irTable         = None
                micTable        = None

                userDictArray   = [];

                try: clientNameArray = list(self.db.table("client_name").run(self.conn))
                except r.errors.ReqlOpFailedError as error: clientNameArray = None

                if clientNameArray != None:

                    for c in clientNameArray:

                        clientList.append(c.get("client_name"))

                        latestInputTemp = c.get("latest_input")
                        latestInputCompTemp = float(latestInputTemp)/1000

                        if latestInputComp == None:

                            latestInput = latestInputTemp
                            latestInputComp = latestInputCompTemp

                        if latestInputComp < latestInputCompTemp:

                            latestInput = latestInputTemp
                            latestInputComp = latestInputCompTemp

                    print(latestInput)

                    for c in clientList:

                        userDict = {};
                        userDict["client_name"] = c;

                        try:
                            self.db.table(c + "_cam").run(self.conn)
                            camTable = self.db.table(c + "_cam")
                        except r.errors.ReqlOpFailedError as error: camTable = None

                        try:
                            self.db.table(c + "_ir").run(self.conn)
                            irTable = self.db.table(c + "_ir")
                        except r.errors.ReqlOpFailedError as error: irTable = None

                        try:
                            self.db.table(c + "_mic").run(self.conn)
                            micTable = self.db.table(c + "_mic")
                        except r.errors.ReqlOpFailedError as error: micTable = None

                        if camTable != None:

                            camTableConn = camTable.get(latestInput).run(self.conn)
                            if camTableConn: userDict["faces"] = camTableConn.get("faces")

                        if irTable != None:

                            irTableConn = irTable.get(latestInput).run(self.conn)
                            if irTableConn: userDict["ir_code"] = irTableConn.get("ir_code")

                        if micTable != None:

                            micTableConn = micTable.get(latestInput).run(self.conn)

                            if micTableConn:
                                userDict["pitch"] = micTableConn.get("pitch")
                                userDict["volume"] = micTableConn.get("volume")

                        userDictArray.append(userDict)

                    emit("latestInputSend", userDictArray)

def main(_docArgs): main = Main(_docArgs)

if __name__ == "__main__":

    docArgs = doc(__doc__, version="0.0.1")
    main(docArgs)
