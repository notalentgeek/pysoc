from cam import CamFaceDetection as cfd
from insert_database import InsertDatabase as idb
from mic import MicPVDetect as mpvd
import os
import rethinkdb as r
import shared
import sys

DEFAULT_DB_ADDRESS = "127.0.1.1"
DEFAULT_DB_NAME = "sociometric_server"
DEFAULT_DB_PORT = 28015

# Variable that hold connection to
# the database.
conn = None
db = None

# Function to connect to database.
def ConnDB():

    try:

        global conn
        global db

        # The default port to connect is
        # 127.0.1.1 or localhost if you
        # use RethinkDB in local environment.
        # The default port for ReThinkDB is
        # 28015.
        conn = r.connect(
            host=DEFAULT_DB_ADDRESS,
            port=DEFAULT_DB_PORT
        )
        db = r.db(DEFAULT_DB_NAME)

        return True

    except r.errors.ReqlDriverError as error:

        print(error)
        return False

def main(args):

    # Only run the program when there is connection
    # to database.
    if ConnDB():

        # Create arrays to hold all threads.
        threads = []
        # Initiates some thread objects.
        iDB = idb("IDB_1", threads, db, conn)
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