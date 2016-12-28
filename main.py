"""sociometric.

Usage:
    main.py (-h | --help)
    main.py (-v | --version)
    main.py check
    main.py check [cam] [db] [ir] [mic]
    main.py reset
    main.py set (-a --dba=<dbav> | -c --clientName=<cname> | -n --dbn=<dbnv> | -p --dbp=<dbpv>)
    main.py start
    main.py start [without-cam] [without-db] [without-ir] [without-mic] [save]
    main.py start all-default [save]
    main.py start wizard [save]

Options:
    -a --dba=<dbav>             Database address, [default: 127.0.0.1].
    -c --clientName=<cname>     Client name for this device. Camel case (for example,
                                myNameIsAlpha), no space, start with alphabet, and
                                alpha - numeric, [default: clientTest]
    -h --help                   Show this screen.
    -n --dbn=<dbnv>             Database name. Only alpha - numeric and under score,
                                [default: sociometric_server].
    -p --dbp=<dbpv>             Database port, [default: 28015].
    -v --version                Show version.
    check                       Check the availability of input devices.
    reset                       Delete all tables in the database.
    save                        Write setting into configuration file.
    set                         Set and write the configuration variables.
    start                       Start this program using previously written configurations.
                                If first time use then launch wizard.1
    start all-default           Start this program using default value.
    start wizard                Start this program guided with configuration wizard.
    without-cam                 This program will run without cam.
    without-db                  This program will run without db.
    without-ir                  This program will run without IR.
    without-mic                 This program will run without mic.

"""

# Import the face detection object.
from cam import CamFaceDetect as cfd
# Get access to the variables in shared.py.
from config import Config as conf
# Import docopt.
from docopt import docopt as doc
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

def main(_docArgs):

    #print("test")
    #print(_docArgs)

    # Creates space for initiation function.
    # Get the arguments from Docopt Python library.
    docArgs = _docArgs

    # I want to know the type of docoptArgs.
    #print(type(docArgs)) # This is Python's dictionary.
    #print(docArgs.get("start"))

    # Check if a configuration file exist.

    # If the starting command is "start".
    if docArgs.get("start"):

        #print("the starting command is start")

        # Now check the other possible sub - commands.
        if docArgs.get("all-default"):

            print("all-default")

            # Check if it has [save] parameter.
            if docArgs.get("save"):

                print("save")

        elif docArgs.get("wizard"):

            print("wizard")

            # Check if it has [save] parameter.
            if docArgs.get("save"):

                print("save")

        elif (docArgs.get("without-cam") or docArgs.get("without-db") or
            docArgs.get("without-ir") or docArgs.get("without-mic")):

            print("without-input(s)")

            # Check if it has [save] parameter.
            if docArgs.get("save"):

                print("save")

        else:

            print("start normally")


    """
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
    """

if __name__ == "__main__":
    docArgs = doc(__doc__, version="0.0.1")
    main(docArgs)