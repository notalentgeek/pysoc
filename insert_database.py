# Import the super class for this class.
# ModThread is just a threading.Thread class
# with some additional variables that necessary
# specifically for this program.
from mod_thread import ModThread as mt

# Import Python json library for JSON manipulation.
import json

# Import RethinkDB Python library to manipulate
# RethinkDB database.
import rethinkdb as r

# Import the shared Python file to gain access over
# some global variables (read - only).
import shared

class InsertDatabase(mt):

    # The constructor. The _conn is the current connection
    # to _db. So, the _db class is the database information,
    # while the _conn is the variable that hold connection
    # between this program and the database.
    def __init__(self, _threadName, _array,
        _db, _conn):

        #print(type(_array))

        # Append this array into database.
        _array.append(self)

        # Initiate the super class.
        mt.__init__(self,
            _array.index(self) + 1,
            _array.index(self) + 1, _threadName)

        # Class wide variables that hold reference to
        # the connected database.
        self.db = _db
        self.conn = _conn
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

                # The first element of the firstElement is
                # from which sensor the data is coming from.
                # In this example there are two sensors which
                # are the cam and microphone.
                sensorSource = firstElement[0]
                # The table name of which data should be stored.
                tableName = shared.clientName + "_" + sensorSource

                # The next elements after the first elements
                # are for time stamps. I am making it with
                # timezone in case there is a necessity to
                # test the project with remote office environment.
                # Put the available data.
                jsonRaw["year"]     = firstElement[1] # Year.
                jsonRaw["month"]    = firstElement[2] # Month.
                jsonRaw["day"]      = firstElement[3] # Day.
                jsonRaw["hour"]     = firstElement[4] # Hour.
                jsonRaw["minutes"]  = firstElement[5] # Minute.
                jsonRaw["second"]   = firstElement[6] # Second.

                #print(jsonRaw["second"])

                jsonRaw["utc"]      = firstElement[7] # Timezone.

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
                index = 8
                while index < len(firstElement):

                    # Parse the field name.
                    fieldName = firstElement[index]
                    index = index + 1
                    # Parse the value.
                    value = firstElement[index]
                    index = index + 1
                    jsonRaw[fieldName] = value

                # Cooked the JSON so that it is ready to be served
                # to the database.
                jsonCooked = json.dumps(jsonRaw)
                # jsonCooked is still a string, hence I need to
                # format it again so that it become dictionary.
                jsonCookedAgain = json.loads(jsonCooked)

                # Check if the target table is exist in the
                # database. If the target table is not exist
                # then create a new table.
                try:

                    self.db.table(tableName).run(self.conn)
                    self.table = self.db.table(tableName)

                except r.ReqlOpFailedError as error:

                    print(
                        "Table for " +
                        shared.clientName +
                        " to store " +
                        sensorSource +
                        " data does not exist."
                    )
                    print("Creating " + tableName + " table.")
                    self.db.table_create(tableName).run(self.conn)
                    self.table = self.db.table(tableName)

                # Finally insert the table.
                self.table.insert(jsonCookedAgain).run(self.conn)

                print(jsonCooked)

                # Pop the first element of the array!
                self.mainArray.pop(0)