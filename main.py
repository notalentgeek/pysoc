from microphone import MicPVDetection
from text_collection import textCollection, TextUpdate
from webcam import WebcamFaceDetection
import os
import rethinkdb as r
import sys
import thread


# Client name must be unique.
clientName = "client-1"


# Variable that hold "object" to database and table.
connection = None
database = None
mainTable = None


# Function to connect to database.
def ConnectDB():


    try:


        global connection
        global database
        global mainTable


        connection = r.connect(
            host="127.0.1.1",
            port=28015
        )
        database = r.db("sociometric_server")
        mainTable = database.table("main")


        # Create document entry for this client.
        # The name of the client must be unique.
        CreateDoc()


        return True


    except r.errors.ReqlDriverError as error:


        print(textCollection.dbConnRefused)
        print(error)
        return False


#Create document in the database table.
def CreateDoc():


    # Make sure there is no document with same name in
    # the database.
    clientWithSameName = list(
        r.db("sociometric_server").table("main")
            .filter({"clientName":clientName}).run(connection)
    )


    #If the length is 0 means there is no document with
    # a same name in the "clientName" entry
    clientWithSameNameAmount = len(clientWithSameName)
    if clientWithSameNameAmount == 0:
        mainTable.insert({

            "clientName": clientName

        }).run(connection)
    else:
        print(textCollection.clientWithSameName)



def main(args):


    # Only run the program if the database is connected.
    if ConnectDB():


        # Create an array to hold all threads.
        threads = []
        # Create new threads.
        textUpdate = TextUpdate(
            threads,
            clientName,
            1,
            1,
            "textUpdate"
        )
        micPVDetection = MicPVDetection(
            threads,                # _array
            2,                      # _counter
            textUpdate,             # _textUpdate
            2,                      # _threadID
            "MicPVDetection"        # _threadName
        )
        webcamFaceDetection = WebcamFaceDetection(
            threads,                # _array
            3,                      # _counter
            textUpdate,             # _textUpdate
            3,                      # _threadID
            "WebcamFaceDetection"   # _threadName
        )


        # Start all threads.
        for thread in threads:
            thread.start()


        # Main loop.
        while(len(threads) > 0):



            try:


                # Join all threads using a timeout
                # so it does not block. Filter out
                # threads which have been joined or
                # are None.
                for thread in threads:
                    if thread.isAlive() and thread != None:
                        thread.join(1)


            except KeyboardInterrupt:


                print(textCollection.quitProgram)
                for thread in threads:
                    thread.killMe = True
                    os._exit(1)


if __name__ == '__main__':
    main(sys.argv)