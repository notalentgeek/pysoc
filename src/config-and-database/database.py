# Import the super class for this class.
# ModThread is just a threading.Thread class
# with some additional variables that necessary
# specifically for this program.
import sys
sys.path.append("./src")
sys.path.append("./src/collection-function")

from collection_function_value_manipulation_and_conversion import GetValueFromConfig as gvfc
from mod_thread                                            import ModThread          as mt

# Import Python json library for JSON manipulation.
import json
import os
# Import RethinkDB Python library to manipulate
# RethinkDB database.
import rethinkdb as r
import shutil

class InsertDatabase(mt):

    # The constructor. The _conn is the current connection
    # to _db. So, the _db class is the database information,
    # while the _conn is the variable that hold connection
    # between this program and the database.
    def __init__(self, _threadName,
        _array, _config, _withoutDB,
        _db, _conn, _logAbsPath):

        # Append this array into database.
        _array.append(self)

        # Initiate the super class.
        mt.__init__(self,
            _array.index(self) + 1,
            _array.index(self) + 1, _threadName)

        # Class wide variables that hold reference to
        # the connected database.
        self.config             = _config
        self.withoutDB          = _withoutDB
        self.db                 = _db
        self.logAbsPath         = _logAbsPath
        # Specifically for table, it will be checked and
        # generated from this class if the destined table
        # is not exists yet.
        self.table = None

        # The main array that holds all data that will
        # be inserted into specific table in self.db.
        self.mainArray = []

    def run(self):

        while self.killMe == False:

            # Check if there is at least one element in the
            # main array. The mainArray is the array that
            # list all element that will be put into database
            # before it pops.
            if len(self.mainArray) > 0:

                log = ""
                # Initiate empty JSON array.
                jsonRaw = {}
                # The cooked JSON array ready to be
                # served into database :d :d :d.
                jsonCooked = {}

                # Take the FIRST element in the main array.
                # The first element in the main array is the
                # earliest element that was added into the
                # main array.
                firstElement = self.mainArray[0]

                # The first element of the `firstElement` is
                # from which sensor the data is coming from.
                # In this example there are two sensors which
                # are the cam and microphone.
                sensorSource = firstElement[0]
                # The table name of which data should be stored.
                tableName = self.config.clientName[2] + "_" + sensorSource

                # The next elements after the first elements
                # are for time stamps. I am making it with
                # timezone in case there is a necessity to
                # test the project with remote office environment.
                # Put the available data.
                jsonRaw["dt"] = (
                    firstElement[1] + # Year.
                    firstElement[2] + # Month.
                    firstElement[3] + # Day.
                    firstElement[4] + # Hour.
                    firstElement[5] + # Minute.
                    firstElement[6]   # Second.
                )
                jsonRaw["utc"] = firstElement[7] # Timezone.

                # Ada everything into log.
                log = log + self.config.clientName[2] + "-"
                log = log + jsonRaw["dt"] + "-" + jsonRaw["utc"] + "-"

                latestInput = jsonRaw["dt"]

                # Next elements are the sensor data itself. So,
                # here I try to parse the data from the index
                # after 8 in firstElement. The first even index
                # after is the field name of the value (for
                # example, pitch or volume). While the odd index
                # after index 7 is the value of its previous index.
                #
                # For example:
                #
                # Index 8 is pitch. Then index 9 is the value of
                # the pitch.
                # Index 9 is force. Then index 10 is the value of
                # the force.

                valueIsValid = True

                index = 8
                while index < len(firstElement):

                    # Parse the field name.
                    fieldName = firstElement[index]
                    index = index + 1
                    # Parse the value.
                    value = firstElement[index]
                    index = index + 1

                    # Specifically for IR detection. The data received is
                    # the IR code. That IR code need to be matched in
                    # `client_name` table in the database to search over
                    # which user has the IR code. The IR code is the IR
                    # namespaces in LIRC in Raspbian. You can check it
                    # using this command, `irrecord --list-namespace`.
                    if sensorSource == "ir" and not self.withoutDB:

                        clientNameArray = None

                        # The value array is the all IR codes received by the
                        # IR receiver during one second interval. The elements
                        # in this array/list is unique.
                        valueArray = value.split(",")
                        # Value new is the "converted" IR codes into client names.
                        valueNew = ""
                        # Iterate through all received IR codes.
                        for vE in valueArray:

                            # Search for all client names that attached to
                            # current inspected IR code.
                            clientNameArray = self.db.table(self.config.clientName[0]).filter(lambda doc:
                                doc[self.config.irCode[0]].match(vE)).run(ConnDB(self.config, True, False))
                            # Convert the returned data into Python's list.
                            clientNameArray = list(clientNameArray)

                            #print(clientNameArray)

                            # Make sure there are at least one client name
                            # returned. In case `len(clientNameArray) == 0`
                            # that means that the IR codes received is not
                            # "attached" into any client names in the
                            # database's table `client_name`.
                            if len(clientNameArray) > 0:
                                clientNameE = str(clientNameArray[0])
                                clientNameE = clientNameE.split("\'client_name\': \'")[1]
                                clientNameE = clientNameE.split("\'")[0]
                                valueNew = valueNew + clientNameE + ","
                            else: value = None

                        # Make sure there are at least a client name returned.
                        # Remove the last comma.
                        if valueNew != "":
                            valueNew = valueNew[:-1]

                            if valueNew != self.config.clientName[2]: value = valueNew
                            elif len(clientNameArray) == 0: value = None
                            else: value = None

                    # Enter the value into `jsonRaw`
                    if value != None:

                        jsonRaw[fieldName] = value
                        log = log + "(" + str(fieldName) + ":" + str(value) + ")"

                    else: valueIsValid = False

                # Cooked the JSON so that it is ready to be served
                # to the database.
                jsonCooked = json.dumps(jsonRaw)
                # jsonCooked is still a string, hence I need to
                # format it again so that it become dictionary.
                jsonCookedAgain = json.loads(jsonCooked)

                if valueIsValid:

                    # Only use this `try` and `except` if only
                    # `self.withoutDB` is `False`.
                    if not self.withoutDB:
                        # Check if the target table is exist in the
                        # database. If the target table is not exist
                        # then create a new table.
                        #
                        # On, 23rd December 2016 there is a problem
                        # that the read request to the database is
                        # getting exponentially higher over times.
                        # After commenting right there and here the
                        # culprit is this try catch statement below.
                        #
                        # The problem here is that I need to check
                        # if a table exist or not by using these codes
                        # self.db.table(tableName).run(ConnDB(self.config, True, False)).
                        # However, those codes makes the exponentially
                        # increase read request over time. In the other
                        # hand I need to know if the table is exists or
                        # not without using the connection codes.
                        #
                        # The solution is to do try checking when a
                        # document inserted. And not to do try checking
                        # if a table is exists.
                        try:

                            #self.db.table(tableName).run(ConnDB(self.config, True, False))
                            self.table = self.db.table(tableName)
                            # Insert the jsonCookedAgain into the database.
                            # The fix to exponentially higher process is to do try
                            # statement for the insert database instead of
                            # checking the connection.
                            r.expr(

                                [

                                    self.table.insert(jsonCookedAgain).run(ConnDB(self.config, True, False)),

                                    # Here I need to update the `latest_input` column
                                    # in `client_name` database.
                                    self.db\
                                        .table(self.config.clientName[0]).get(self.config.clientName[2])\
                                        .update({"latest_input": latestInput})

                                ]

                            ).run(ConnDB(self.config, True, False))

                        except r.ReqlOpFailedError as error:

                            print(
                                "table for " +
                                self.config.clientName[2] +
                                " to store " +
                                sensorSource +
                                " data does not exist"
                            )
                            print("creating " + tableName + " table")
                            self.db.table_create(tableName, primary_key="dt").run(ConnDB(self.config, True, False))
                            self.table = self.db.table(tableName)
                            # Insert the jsonCookedAgain into the database.
                            # The fix to exponentially higher is to do try
                            # statement for the insert database instead of
                            # checking the connection.
                            self.table.insert(jsonCookedAgain).run(ConnDB(self.config, True, False))

                            # Here I need to update the `latest_input` column
                            # in `client_name` database.
                            self.db\
                                .table(self.config.clientName[0]).get(self.config.clientName[2])\
                                .update({"latest_input": latestInput}).run(ConnDB(self.config, True, False))

                    #print(jsonCooked)
                    if not self.config.withoutLog[2] : print(log)

                    # Write the log value into log file.
                    with open(self.logAbsPath, "a") as logTxt:
                        logTxt.write(log + "\n")

                # Pop the first element of the array!
                self.mainArray.pop(0)

# Function to initiating connection to database.
# `_requestStart` is used to indicate if this application
# is requested to `start` after database connection.
# If this application is only requested to check the
# database then `_requestStart` should be `False`.
def ConnDB(_config, _persistent, _requestStart):

    conn    = None
    db      = None

    if not _persistent and not _requestStart:

        try:

            conn = r.connect(
                host=_config.dbAddress[2],
                port=_config.dbPort[2])

            return conn

        except r.errors.ReqlDriverError as error:

            # Print the error.
            print("connection to database error with error code of \"" + str(error) + "\"")
            print("please check database or check database configuration from this application")

    else:

        while True:

            # Try to connecting to RethinkDB server.
            # If without_database flag is False and
            # the connection from this application to
            # the database failed then halt this
            # program.
            try:

                # The default port to connect is the
                # localhost "127.0.0.1" (in string).
                # Whereas the default port for RethinkDB
                # is 28015.
                #
                # In local you can run RethinkDB with
                # using `rethinkdb` command from terminal.
                # From hosted environment (like
                # DigitalOcean) run RethinkDB using
                # `rethinkdb --bind all` from SSH - ed
                # terminal.
                #
                # Connect into database.
                conn = r.connect(
                    host=_config.dbAddress[2],
                    port=_config.dbPort[2])

                if _persistent: return conn
                # Initiating trial and error for database.
                # Trying to make persistent connection into
                # database.
                else:

                    # Pick which database to get its information stored.
                    db = r.db(_config.dbName[2])
                    if not _config.dbName[2] in r.db_list().run(conn) and _requestStart:
                        db = r.db_create(_config.dbName[2]).run(conn)
                        db = r.db(_config.dbName[2])
                        print("database " + _config.dbName[2] + " does not exist")
                        print("creating database " + _config.dbName[2])

                    if _requestStart:
                        # Check if there is a table called `client_name`.
                        # If not then create one.
                        clientNameTable = None
                        try:
                            db.table(_config.clientName[0]).run(conn)
                            clientNameTable = db.table(_config.clientName[0])
                        except r.errors.ReqlOpFailedError as error:
                            print("creating " + _config.clientName[0] + " table")
                            db.table_create(_config.clientName[0], primary_key=_config.clientName[0]).run(conn)
                            clientNameTable = db.table(_config.clientName[0])

                        # Check if there is document with `client_name` equals
                        # to `_config.clientName[2]`. If there is not created new
                        # document with the respective IR code. This means that
                        # this user is new in the system. If there is document
                        # with `_config.clientName[0]` equals `_config.clientName[2]`,
                        # then just update the value of its `ir_code` into
                        # `_config.irCode[2]` (the current real time variable value
                        # of IR code).
                        if clientNameTable.get(_config.clientName[2]).run(conn) == None:
                            print("no client found")
                            jsonRaw = {}

                            jsonRaw[_config.clientName[0]] = _config.clientName[2]
                            jsonRaw[_config.irCode[0]] = _config.irCode[2]

                            jsonCooked = json.dumps(jsonRaw)
                            jsonCookedAgain = json.loads(jsonCooked)
                            clientNameTable.insert(jsonCookedAgain).run(conn)
                        else:
                            clientNameTable.get(_config.clientName[2]).update({_config.irCode[0]: _config.irCode[2]}).run(conn)

                    # If connection success return True and the database.
                    return [True, db, conn]

            except r.errors.ReqlDriverError as error:

                # Print the error.
                print("connection to database error with error code of \"" + str(error) + "\"")
                print("please check database or check database configuration from this application")

# Python function to delete database.
def DeleteDatabaseAndLog(_config, _configAbsPath, _logFolderAbsPath):

    # Try to connect to database.
    connDB = ConnDB(_config, False, False)
    if connDB != None:

        # Delete all tables. But first get all table list.
        dbNameFromConfig = str(gvfc(_configAbsPath, _config.iniSections[0], _config.dbName[0]))
        try:
            r.db_drop(dbNameFromConfig).run(connDB)
            print("database deleted")
        except r.errors.ReqlOpFailedError as error: print("database does not exists")

    # Delete log folder.
    if os.path.exists(_logFolderAbsPath): shutil.rmtree(_logFolderAbsPath)
    print("log folder deleted")
