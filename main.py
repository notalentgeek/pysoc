# Import the face detection object.
from cam import CamFaceDetect as cfd
# Get access to the variables in shared.py.
from config import Config as conf
# Import the database inserter.
from insert_database import InsertDatabase as idb
# Import the pitch and volume detection object.
from mic import MicPVDetect as  mpvd

# Import the OpenCV library just for
# the user interface.
import cv2
import os
# Python library for RethinkDB.
import rethinkdb as r
import sys

# Shared variables.
config = conf()

# Variables that hold database information and the database
# connection object.
connection = None
database = None

# Function to connect to the database.
def ConnDB():

    # Initiating value.
    config.InitConfigVariables()
    # This is just for development purposes only.
    # I do not know yet on how I can add the parameter
    # into this program.
    config.cfgDBAddress = "198.211.123.92"

    try:

        global connection
        global database

        # The default port to connect is
        # 127.0.1.1 or localhost if you
        # use RethinkDB in local environment.
        # The default port for ReThinkDB is
        # 28015.
        connection = r.connect(
            host=config.cfgDBAddress,
            port=config.cfgDBPort
        )
        database = r.db(config.cfgDBName)

        return True

    # If there is an error on the database connection,
    # then halt this program and show the error ONCE
    # on the terminal.
    except r.errors.ReqlDriverError as error:

        print(error)
        while True: pass

def main(args):

    # Only run database when there is connection to
    # the database.
    if ConnDB():

        # Create arrays to hold all threads.
        threads = []

        #print(type(database))

        # Initiates some thread objects.
        iDB = idb("IDB_1", threads, database, connection, config)
        cFD = cfd("CFD_1", threads, iDB)
        mPVD = mpvd("MPVD_1", threads, iDB)
        # Run all threads!
        for t in threads: t.start()

        # Loop
        while len(threads) > 0:

            try:

                # Join all threads using a timeout
                # so it does not block. Filter out
                # thread which have been joined or
                # is `None`.
                for t in threads:
                    if t.isAlive() and t != None: t.join(1)

            except KeyboardInterrupt:

                print("Quitting program")
                for t in threads:
                    t.killMe = True
                    # This is dangerous better find another
                    # method on exiting the program. Preferably
                    # when all threads are finished then
                    # close this program. However, I do not know
                    # yet how.
                    os._exit(1)

if __name__ == "__main__": main(sys.argv)