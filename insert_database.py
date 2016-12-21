from mod_thread import ModThread as mt
import json
import rethinkdb as r
import shared

class InsertDatabase(mt):

    def __init__(
        self,
        _threadName,
        _array,
        _db,
        _conn
    ):

        # Append this object into array.
        _array.append(self)

        mt.__init__(
            self,
            _array.index(self) + 1,
            _array.index(self) + 1,
            _threadName
        )

        # Local variable that hold reference to
        # the connected database.
        self.db = _db
        self.conn = _conn
        self.table = None

        # The main array that holds all data to be
        # inserted into specific table in self.db.
        self.mainArray = []

    def run(self):

        while self.killMe == False:

            # Check if there is at least one element in
            # the array.
            if len(self.mainArray) > 0:

                # Empty unformatted JSON.
                jsonRaw = {}
                # Cooked JSON ready for database :d.
                jsonCooked = None

                # Take the latest element in the main array
                # to be put into database.
                latestElement = self.mainArray[len(self.mainArray) - 1]

                # The first element of the latestElement is
                # from which sensor the data is coming from.
                # In this example there are two sensors which
                # are the cam and microphone.
                sensorSource        = latestElement[0]
                tableName           = shared.clientName + "_" + sensorSource
                # The next elements after the first elements
                # are for time stamps. I am making it with
                # timezone in case there is a necessity to
                # test the project with remote office environment.
                # Put the available data.
                jsonRaw["year"]     = latestElement[1] # Year.
                jsonRaw["month"]    = latestElement[2] # Month.
                jsonRaw["day"]      = latestElement[3] # Day.
                jsonRaw["hour"]     = latestElement[4] # Hour.
                jsonRaw["minutes"]  = latestElement[5] # Minute.
                jsonRaw["second"]   = latestElement[6] # Second.

                #print(jsonRaw["second"])

                jsonRaw["utc"]      = latestElement[7] # Timezone.
                # Next elements are the sensor data itself. So, here
                # I try to parse the data from the index after 8 in
                # latestElement.
                index = 8
                while index < len(latestElement):

                    # Parse the field name.
                    fieldName = latestElement[index]
                    index = index + 1
                    # Parse the value.
                    value = latestElement[index]
                    index = index + 1
                    jsonRaw[fieldName] = value

                # Cooked the JSON so that it is ready to be served
                # to the database.
                jsonCooked =json.dumps(jsonRaw)

                # Check if the target table is exist in the database.
                # If the target table is not exist then create a new
                # table.
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
                    self.table = self.db.table_create(tableName)

                # Finally insert the table.
                # self.table.insert(jsonCooked).run(self.connection)
                print(jsonCooked)

                # Pop the array!
                self.mainArray.pop()