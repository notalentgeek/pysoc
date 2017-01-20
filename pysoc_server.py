"""pysoc_server

Usage:
    pysoc_server.py (--help | -h)
    pysoc_server.py (--version | -v)
    pysoc_server.py <dba> [-o|--dbn=<dbnv>|--dbp=<dbpv>|--tout=<toutv>]...
    pysoc_server.py [-o|--dbn=<dbnv>|--dbp=<dbpv>|--nodb|--tout=<toutv>]...

Options:
    --help -h           Refer to help manual.
    --version -v        Refer to this version of application.

    -o                  Online.
    --nodb              Run without RethinkDB.

    dba                 RethinkDB address [default: 127.0.0.1].
    --dbn=<dbnv>        RethinkDB database name [default: sociometric_server].
    --dbp=<dbpv>        RethinkDB port [default: 28015].
    --tout=<toutv>      RethinkDB connection time out [default: 20].

"""
from   docopt         import docopt          as doc
from   flask          import Flask
from   flask          import render_template
from   flask_socketio import emit
from   flask_socketio import SocketIO        as sio
from   socket         import socket

import rethinkdb      as     r

app        = Flask(__name__)
sIO        = sio(app)

cDB        = None
conn       = None
db         = None

def main(_docArgs):

    global conn
    global db

    dbAddress  = _docArgs["<dba>"]
    dbName     = _docArgs["--dbn"][0]
    dbPort     = int(_docArgs["--dbp"][0])
    noDB       = int(_docArgs["--nodb"])
    timeout    = int(_docArgs["--tout"][0])

    if(noDB != 1):

        try:

            cDB    = ConnDB(
                dbAddress,
                dbName,
                dbPort,
                timeout
            )
            conn   = cDB[0]
            db     = cDB[1]

            #print(conn)
            #print(db)

        except r.errors.ReqlTimeoutError as error: print(error)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/api/client")
def api_client():
    return str(list(db.table("client_name").run(conn)))
@app.route("/api/cam/<_clientName>")
def api_cam(_clientName):
    return str(list(db.table(_clientName + "_cam").run(conn)))
@app.route("/api/ir/<_clientName>")
def api_ir(_clientName):
    return str(list(db.table(_clientName + "_ir").run(conn)))
@app.route("/api/mic/<_clientName>")
def api_mic(_clientName):
    return str(list(db.table(_clientName + "_mic").run(conn)))

@sIO.on("latestInputRequest")
def LatestInput():

    #print("test")
    #print(conn)
    #print(db)

    if conn != None and db != None:

        latestInput     = None
        latestInputComp = None

        clientNameArray = None
        camTable        = None
        irTable         = None
        micTable        = None

        userDictArray   = []

        try:

            clientNameTable = db.table("client_name").run(conn)
            clientNameArray = list(clientNameTable)
            #print(clientNameTable)
            #print(clientNameArray)

        except r.errors.ReqlOpFailedError as error: clientNameArray = None

        #print(clientNameArray)

        if clientNameArray != None:

            for c in clientNameArray:

                latestInputTemp = c.get("latest_input")
                latestInputCompTemp = float(latestInputTemp)/1000

                if latestInputComp == None:

                    latestInput = latestInputTemp
                    latestInputComp = latestInputCompTemp

                if latestInputComp < latestInputCompTemp:

                    latestInput = latestInputTemp
                    latestInputComp = latestInputCompTemp

            #print(latestInput)

            for c in clientNameArray:

                if c.get("latest_input") == latestInput:

                    tableList = db.table_list().run(conn)
                    userDict = {}
                    userDict["client_name"] = c.get("client_name")


                    if (c.get("client_name") + "_cam") in tableList: camTable = db.table(c.get("client_name") + "_cam")
                    else: camTable = None

                    if (c.get("client_name") + "_ir") in tableList: irTable = db.table(c.get("client_name") + "_ir")
                    else: irTable = None

                    if (c.get("client_name") + "_mic") in tableList: micTable = db.table(c.get("client_name") + "_mic")
                    else: micTable = None

                    if camTable != None:

                        camTableConn = camTable.get(latestInput).run(conn)
                        if camTableConn: userDict["faces"] = camTableConn.get("faces")

                    if irTable != None:

                        irTableConn = irTable.get(latestInput).run(conn)
                        if irTableConn: userDict["ir_code"] = irTableConn.get("ir_code")

                    if micTable != None:

                        micTableConn = micTable.get(latestInput).run(conn)

                        if micTableConn:
                            userDict["pitch"] = micTableConn.get("pitch")
                            userDict["volume"] = micTableConn.get("volume")

                    userDictArray.append(userDict)

            emit("latestInputSend", userDictArray)
            #print("test")

def ConnDB(_dba, _dbn,
    _dbp, _timeout):

    print("trying to establish database connection")

    conn = r.connect(
        host=_dba, port=_dbp,
        timeout=_timeout)

    db = r.db(_dbn)

    return [conn, db]

if __name__ == "__main__":

    docArgs = doc(__doc__, version="0.0.1")
    #print(docArgs)
    online = int(docArgs["-o"])

    main(docArgs)

    #print(conn)
    #print(db)

    if online == 1: sIO.run(app, host="0.0.0.0")
    else: sIO.run(app)
