"""pysoc_server

Usage:
    pysoc_server.py (--help|-h)
    pysoc_server.py (--version|-v)
    pysoc_server.py [--nodb|-o|--dba=<dbav>|--dbn=<dbnv>|--tout=<toutv>]...

Options:
    --help -h           Refer to help manual.
    --version -v        Refer to this version of application.

    --nodb              Run this web server without database.
                        Useful for debugging the simulation.
    -o                  Make this web server to be online.

    --dba=<dbav>        Database address [default: 127.0.0.1].
    --dbn=<dbnv>        Database name [default: pysoc_server].
    --tout=<toutv>      Connection timeout. Amount of this
                        application needs to wait for database
                        connection [default: 20].

"""
import sys
sys.path.append("./test-unit-python")

from   docopt         import docopt          as doc
from   flask          import Flask
from   flask          import render_template
from   flask_socketio import emit
from   flask_socketio import SocketIO        as sio
from   socket         import socket
import database
import rethinkdb      as     r

# Function to get database API.
def DatabaseAPI(

    _c,
    _db,       # Database reference without the connection.
    _noDB,     # Running with or without database connection.
    _tableName # Table name.

):

    #print("test1")
    #print(type(_db))

    if   _noDB: return "web server is running without connection to database server"
    else      :
        return str(list(_db.table(_tableName).run(_c)))

# Make a function to connect to database and to set up connection.
# So 1 function to return database information. The INFORMATION
# without database connection!!!! And then another function to
# constantly create connection. I need to re - create new
# connection object every time I need to connect to database
# to make sure there will be still a connection in case the
# database is turned off and then turned on again.
#
# Function to create connection object. Make sure this function
# return connection object.
#
# PENDING - DONE: Can use the new function from `database.py`.
# Obsolete method.
def DatabaseConnection(

    _dbA,      # Database address. The default is "127.0.0.1" if the database server and the
    _dbP,      # Database port. Make sure it goes by default at port 28015.
    _tOut=None # Connection time out. Make sure it has at least the default 20 seconds.

):

    if _tOut == None: _tOut = int(20)

    #print(_dbA)
    #print(_dbP)
    #print(_tOut)

    return r.connect(

        host=str(_dbA),
        port=int(_dbP),
        timeout=int(_tOut)

    )

def DatabaseGetAllClientName(_c, _db, _tableName):

    #_db = _db.coerce_to("binary")

    #print(_db)
    #print(type(_db))

    return list(_db.table(_tableName).run(_c))

def DatabaseGetAllClientNameMod1(_c, _db):

    #_db = _db.coerce_to("binary")

    #print(_db)
    #print(type(_db))

    return DatabaseGetAllClientName(_c, _db, "client_name")

def DatabaseGetAllTableName(_c, _db):

    #_db = _db.coerce_to("binary")

    #print(_db)
    #print(type(_db))

    return _db.table_list().run(_c)

# Function to assign column with latest input to dictionary.
def DatabaseGetLatestInputColumnValueToDict(

    _c,
    _colName,
    _dict,
    _latestInputStr,
    _table

):

    # Make sure to have `latest_input` as primary index in RethinkDB.
    tableConn = _table.filter({ "dt":_latestInputStr }).run(_c)
    tableConnList = list(tableConn)

    #print(_colName)
    #print(_latestInputStr)
    #print(_table)
    #print(tableConn)
    #print(tableConnList)

    if len(tableConnList) > 0 and tableConnList[0].get(_colName) != None:
        _dict[_colName] = tableConnList[0][_colName]

    #print(_dict)

# Function to assign table with latest input to dictionary.
def DatabaseGetLatestInputTableValueToDict(

    _c,
    _dict,           # Dictionary we want to fill.
    _latestInputStr, # Latest input in string so that we can query faster with database.
    _tableName,      # Table name we are looking for column.
    _tableNameList,  # All table name in the database.
    *_colName        # Table column name we are looking for.

):

    #print("test1")
    #print(_tableName)
    #print(_tableNameList)

    if   _tableName in _tableNameList: table = db.table(_tableName)
    else                             : table = None

    if table != None:

        #print("test2")
        #print(_colName)
        #print(len(_colName))
        #print("="*5)
        #print(_colName)
        #print(list(_colName))
        #print(type(_colName))
        #print(type(list(_colName)))
        #print("="*5)

        for i in list(_colName):

            #print("="*5)
            #print(c)
            #print(_colName)
            #print(list(_colName))
            #print(type(_colName))
            #print("="*5)

            DatabaseGetLatestInputColumnValueToDict(
                _c, i, _dict, _latestInputStr, table);

def GetLatestInput(_clientNameList, _columnLatestInput):

    latestInputFlo = None
    latestInputStr = None
    for c in _clientNameList:

        #print(c)
        latestInputStrTemp = c.get(_columnLatestInput)
        #print(latestInputStrTemp)
        latestInputFloTemp = float(latestInputStrTemp)/1000

        if latestInputFlo == None:

            latestInputStr = latestInputStrTemp
            latestInputFlo = latestInputFloTemp

        if latestInputFlo < latestInputFloTemp:

            latestInputStr = latestInputStrTemp
            latestInputFlo = latestInputFloTemp

    return [latestInputFlo, latestInputStr]

def GetLatestInputMod1(_clientNameList): return GetLatestInput(_clientNameList, "latest_input")

if __name__ == "__main__":

    # Returned Docopt arguments.
    docArgs = doc(__doc__, version="0.0.1")

    # Values from Docopt.
    noDB    = True if (int(docArgs["--nodb"]) == 1) else (False if (int(docArgs["--nodb"]) == 0) else None)
    online  = True if (int(docArgs["-o"    ]) == 1) else (False if (int(docArgs["-o"    ]) == 0) else None)

    #print(docArgs)

    dbA     = str(docArgs["--dba"][0])
    dbN     = str(docArgs["--dbn"][0])
    tOut    = int(docArgs["--tout"][0])

    app     = Flask(__name__)
    sIO     = sio(app)
    db      = r.db(dbN)

    if not noDB:
        c = database.conn(dbA);

    #print(db)
    #print(type(db))

    # Routings.
    @app.route("/")
    def index(): return render_template("index.html")

    @app.route("/api/client")
    def api_client():
        return DatabaseAPI(c, db, dbA, noDB, "client_name")

    @app.route("/api/cam/<_clientName>")
    def api_cam(_clientName):
        return DatabaseAPI(c, db, dbA, noDB, _clientName + "_cam")

    @app.route("/api/ir/<_clientName>")
    def api_ir(_clientName):
        return DatabaseAPI(c, db, dbA, noDB, _clientName + "_ir")

    @app.route("/api/mic/<_clientName>")
    def api_mic(_clientName):
        return DatabaseAPI(c, db, dbA, noDB, _clientName + "_mic")

    # Web socket routing.
    @sIO.on("goToInputRequest")
    def GoToInputRequest(_data):
        requestedDT = _data["dt"]
        if not noDB:

            # Check database if not exists then this method creates it.
            database.create_db(c, "pysoc_server");
            # Check table if not exists then this method creates it.
            database.create_table(c, "client_name",
                "pysoc_server");

            clientDictList     = []                                    # All client information that will be sent to client.
            clientNameList     = DatabaseGetAllClientNameMod1(c, db)            # All client name from `client_name` table in database.
            tableNameList      = DatabaseGetAllTableName(c, db)                 # All tables in database.

            for i in clientNameList:

                clientName = i.get("client_name")
                face_temp = (database.get_first_doc_value(c, str(requestedDT), "dt", "face", "{}_face".format(clientName), dbN));
                pitch_temp = (database.get_first_doc_value(c, str(requestedDT), "dt", "pitch", "{}_pitch".format(clientName), dbN));
                presence_temp = (database.get_first_doc_value(c, str(requestedDT), "dt", "presence", "{}_presence".format(clientName), dbN));
                volume_temp = (database.get_first_doc_value(c, str(requestedDT), "dt", "volume", "{}_volume".format(clientName), dbN));

                if type(face_temp) is not list: i["face"] = face_temp
                if type(pitch_temp) is not list: i["pitch"] = pitch_temp
                if type(presence_temp) is not list: i["presence"] = presence_temp
                if type(volume_temp) is not list: i["volume"] = volume_temp

                clientDictList.append(i)

            emit("inputSend", clientDictList)

    @sIO.on("latestInputRequest")
    def LatestInputRequest():

        if not noDB:

            # Check database if not exists then this method creates it.
            database.create_db(c, "pysoc_server");
            # Check table if not exists then this method creates it.
            database.create_table(c, "client_name",
                "pysoc_server");

            clientDictList     = []
            clientNameList     = DatabaseGetAllClientNameMod1(c, db)            # All client name from `client_name` table in database.
            latestInput        = GetLatestInputMod1(clientNameList)
            latestInputStr     = latestInput[1]                                 # Latest input time in string as we received from database.
            tableNameList      = DatabaseGetAllTableName(c, db)                 # All tables in database.

            for i in clientNameList:

                if i.get("latest_input") == latestInputStr:
                    clientName = i.get("client_name")
                    #clientNameDict = {}
                    #clientNameDict["client_name"] = clientName

                    def DatabaseGetLatestInputTableValueToDictMod1(_tableName, *_colName):
                        DatabaseGetLatestInputTableValueToDict(c, i,
                            i.get("latest_input"), _tableName, tableNameList, *_colName)
                    #DatabaseGetLatestInputTableValueToDictMod1(clientName + "_cam", "faces")
                    #DatabaseGetLatestInputTableValueToDictMod1(clientName + "_ir" , "ir_code")
                    #DatabaseGetLatestInputTableValueToDictMod1(clientName + "_mic", "pitch", "volume")
                    DatabaseGetLatestInputTableValueToDictMod1(clientName + "_face", "face")
                    DatabaseGetLatestInputTableValueToDictMod1(clientName + "_pitch", "pitch")
                    DatabaseGetLatestInputTableValueToDictMod1(clientName + "_presence" , "presence")
                    DatabaseGetLatestInputTableValueToDictMod1(clientName + "_volume", "volume")

                    clientDictList.append(i)

            print(latestInputStr)
            emit("inputSend", clientDictList)

    context = ("/etc/ssl/certs/apache-selfsigned.crt", "/etc/ssl/private/apache-selfsigned.key")
    if   online: sIO.run(app, host="0.0.0.0", ssl_context=context)
    else       : sIO.run(app)