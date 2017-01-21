"""pysoc_server

Usage:
    pysoc_server.py (--help|-h)
    pysoc_server.py (--version|-v)
    pysoc_server.py [--nodb|-o|--dba=<dbav>|--dbp=<dbpv>|--dbn=<dbnv>|--tout=<toutv>]...

Options:
    --help -h           Refer to help manual.
    --version -v        Refer to this version of application.

    --nodb              Run this web server without database.
                        Useful for debugging the simulation.
    -o                  Make this web server to be online.

    --dba=<dbav>        Database address [default: 127.0.0.1].
    --dbp=<dbpv>        Database port [default: 28015].
    --dbn=<dbnv>        Database name [default: pysoc_server].
    --tout=<toutv>      Connection timeout. Amount of this
                        application needs to wait for database
                        connection [default: 20].

"""
from   docopt         import docopt          as doc
from   flask          import Flask
from   flask          import render_template
from   flask_socketio import emit
from   flask_socketio import SocketIO        as sio
from   socket         import socket
import rethinkdb      as     r

# Function to get database API.
def DatabaseAPI(

    _db,       # Database reference without the connection.
    _dbA,      # Database address.
    _dbP,      # Database port.
    _noDB,     # Running with or without database connection.
    _tableName # Table name.

):

    #print("test1")
    #print(type(_db))

    if   _noDB: return "web server is running without connection to database server"
    else      :

        #print("test2")
        #print(_db.table(_tableName))
        #print(_db.table(_tableName).run(DatabaseConnection(_dbA, _dbP)))

        return str(list(_db.table(_tableName).run(DatabaseConnection(_dbA, _dbP))))

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
def DatabaseConnection(

    _dbA,      # Database address. The default is "127.0.0.1" if the database server and the
    _dbP,      # Database port. Make sure it goes by default at port 28015.
    _tOut=None # Connection time out. Make sure it has at least the default 20 seconds.

):

    if _tOut == None: _tOut = int(20)

    #print(_dbA)
    #print(_dbP)
    #print(_tOut)

    conn = r.connect(

        host=str(_dbA),
        port=int(_dbP),
        timeout=int(_tOut)

    )

    """
    try:

        conn = r.connect(

            host=str(_dBA),
            port=int(_dbP),
            timeout=int(_tOut)

        )

    except:

        while True: "there is an error when connecting to database"
    """

    return conn

def DatabaseGetAllClientName(_db, _dbA, _dbP, _tableName):

    #_db = _db.coerce_to("binary")

    #print(_db)
    #print(type(_db))

    return list(_db.table(_tableName).run(DatabaseConnection(_dbA, _dbP)))

def DatabaseGetAllClientNameMod1(_db, _dbA, _dbP):

    #_db = _db.coerce_to("binary")

    #print(_db)
    #print(type(_db))

    return DatabaseGetAllClientName(_db, _dbA, _dbP, "client_name")

def DatabaseGetAllTableName(_db, _dbA, _dbP):

    #_db = _db.coerce_to("binary")

    #print(_db)
    #print(type(_db))

    return _db.table_list().run(DatabaseConnection(_dbA, _dbP))

# Function to assign column with latest input to dictionary.
def DatabaseGetLatestInputColumnValueToDict(

    _colName,
    _dBA,
    _dbP,
    _dict,
    _latestInputStr,
    _table

):

    # Make sure to have `latest_input` as primary index in RethinkDB.
    tableConn = _table.get(_latestInputStr).run(DatabaseConnection(_dBA, _dbP))

    print(_dBA)
    print(_dbP)
    print(_latestInputStr)
    print(_table)
    print(tableConn)

    if tableConn: _dict[_colName] = tableConn.get(_colName)

    print(_dict)

# Function to assign table with latest input to dictionary.
def DatabaseGetLatestInputTableValueToDict(

    _dbA,            # Database address.
    _dbP,            # Database port.
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

        for c in list(_colName):

            #print("="*5)
            #print(c)
            #print(_colName)
            #print(list(_colName))
            #print(type(_colName))
            #print("="*5)

            DatabaseGetLatestInputColumnValueToDict(
                c, _dbA, _dbP, _dict, _latestInputStr, table);

def GetLatestInput(_clientNameList, _columnLatestInput):

    latestInputFlo = None
    for c in _clientNameList:

        latestInputStrTemp = c.get(_columnLatestInput)
        latestInputFloTemp = float(latestInputStrTemp)/1000

        if latestInputFlo == None:

            latestInputStr = latestInputStrTemp
            latestInputFlo = latestInputFloTemp

        if latestInputFlo < latestInputFloTemp:

            latestInputStr = latestInputStrTemp
            latestInputFlo = latestInputFloTemp

    return latestInputStr

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
    dbP     = int(docArgs["--dbp"][0])
    tOut    = int(docArgs["--tout"][0])

    app     = Flask(__name__)
    sIO     = sio(app)
    db      = r.db(dbN)

    #print(db)
    #print(type(db))

    # Routings.
    @app.route("/")
    def index(): return render_template("index.html")

    @app.route("/api/client")
    def api_client(): return DatabaseAPI(db, dbA, dbP, noDB, "client_name")

    @app.route("/api/cam/<_clientName>")
    def api_cam(_clientName): return DatabaseAPI(db, dbA, dbP, noDB, _clientName + "_cam")

    @app.route("/api/ir/<_clientName>")
    def api_ir(_clientName): return DatabaseAPI(db, dbA, dbP, noDB, _clientName + "_ir")

    @app.route("/api/mic/<_clientName>")
    def api_mic(_clientName):  return DatabaseAPI(db, dbA, dbP, noDB, _clientName + "_mic")

    # Web socket routing.
    @sIO.on("latestInputRequest")
    def LatestInputRequest():

        if not noDB:

            clientNameDictList = []                                          # All client information that will be sent to client.
            clientNameList     = DatabaseGetAllClientNameMod1(db, dbA, dbP)  # All client name from `client_name` table in database.
            latestInputStr     = GetLatestInputMod1(clientNameList)          # Latest input time in string as we received from database.
            tableCam           = None                                        # Database table to hold camera data.
            tableIR            = None                                        # Database table to hold infrared transceiver data.
            tableMic           = None                                        # Database table to hold microphone data.
            tableNameList      = DatabaseGetAllTableName(db, dbA, dbP)       # All tables in database.

            for c in clientNameList:

                if c.get("latest_input") == latestInputStr:

                    clientName = c.get("client_name")
                    clientNameDict = {}
                    clientNameDict["client_name"] = clientName

                    def DatabaseGetLatestInputTableValueToDictMod1(_tableName, *_colName):
                        DatabaseGetLatestInputTableValueToDict(dbA, dbP, clientNameDict,
                            latestInputStr, _tableName, tableNameList, *_colName)
                    DatabaseGetLatestInputTableValueToDictMod1(clientName + "_cam", "faces")
                    DatabaseGetLatestInputTableValueToDictMod1(clientName + "_ir" , "ir_code")
                    DatabaseGetLatestInputTableValueToDictMod1(clientName + "_mic", "pitch", "volume")

                    clientNameDictList.append(clientNameDict)

            #print(clientNameDictList)
            #print(type(clientNameDictList))

            emit("latestInputSend", clientNameDictList)

    if   online: sIO.run(app, host="0.0.0.0")
    else       : sIO.run(app)