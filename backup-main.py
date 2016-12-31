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
    reset                       Delete all tables in the database and config file.
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

from    cam             import CamFaceDetect    as cfd      # Import the face detection object.
from    config          import Config           as conf     # Get access to the variables in shared.py.
from    docopt          import docopt           as doc      # Import docopt, the "user interface" library for CLI application.
from    insert_database import InsertDatabase   as idb      # Import the database inserter.
from    mic             import MicPVDetect      as mpvd     # Import the pitch and volume detection object.

import  configparser    as cfgp     # Import library to managing config.
import  io                          # Import io library to deal with opening/writing config file.
import  os                          # Import os Python library to deal with file management.
import  rethinkdb       as r        # Python library for RethinkDB.
import  sys

class Main(object):

    def __init__(self, _docArgs):

        docArgs             = _docArgs                              # Arguments supplied from Docopt.

        CONFIG_FILE_NAME    = "config.ini"                          # File name for the configuration file.

        config              = conf()                                # Configuration variable.
        configAbsPath       = os.path.join("./", CONFIG_FILE_NAME)  # Absolute path to the configuration file exist or not.
        conn                = None                                  # For holding information about the connection between this application and the database.
        db                  = None                                  # For holding information about the database.
        firstRun            = False                                 # Check if this application on its first time run (after reset).

        # PENDING - 1, If this application reset but then the first run
        # is to using `set` command then set do not forget to set `first_run`
        # parameter in the `config.ini` to False, because the setting had
        # been set.
        #
        # I want to know the `type()` of `docArgs`.
        #print(type(docArgs))
        # `docArgs` is apparently a native Python dictionary type data.
        #print(docArgs.get("start"))
        #
        # `docArgs.get("start")` will return either True or False depending
        # whether `start` sub - command is used or not.
        #
        # Check if there is a configuration file. If not then create one.
        if os.path.exists(configAbsPath):

            # If the configuration file exist then we assign the value.

        else:

            # If the configuration file is not exist then we create it
            # then we assign the value.


    # Function to loop.
    def Update(self):

    # Function to assign value to the run - time configuration variables.
    def AssignConfig(self, _config, _configAbsPath):

    # Function to create config.ini at this program root directory.
    def CreateConfig(self):

    # Function to initiating connection to database.
    def ConnDB(self, _config, _conn,
        _db):

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
            _conn = r.connect(
                host=_config.dbAddress[2],
                port=_config.dbPort[2])

            # Pick which database to get its
            # information stored.
            _db = r.db(config.dbName[2])

            # If connection success return True.
            return True

        except r.errors.ReqlDriverError as error:

            # Print the error.
            print("connection to database error with error code of " + error)
            print("please check database")
            print("or check database configuration from this application")
            print("re - trying connection")

            # Run this function again until the connection
            # to database established or the user stopped
            # this application.
            self.ConnDB(_config, _conn, _db)

def main(_docArgs): main = Main(_docArgs)
if __name__ == "__main__":
    docArgs = doc(__doc__, version="0.0.1")
    main(docArgs)