"""sociometric.

Usage:
    main.py (-h | --help)
    main.py (-v | --version)
    main.py check
    main.py check [cam] [db] [ir] [mic]
    main.py reset
    main.py set (-a --dba=<dbav> | -c --cname=<cnamev> | -n --dbn=<dbnv> | -p --dbp=<dbpv>)
    main.py show config
    main.py start
    main.py start [without-face-detection] [without-db] [without-ir-detection] [without-log] [without-pv-detection] [save]
    main.py start all-default [save]
    main.py start wizard

Options:
    For example you want to set this client name to "Richard Dawkins". Then you can
    use these launch commands, `-c "Richard Dawkins"` or `--cname="Richard Dawkins"`.
    You only need to use quotation marks if there is at least one spaces, otherwise
    you may not use it. For example `-c Dawkins` or `--cname=Dawkins` also works.

    -a --dba=<dbav>             Database address, [default: 127.0.0.1].
    -c --cname=<cnamev>         Client name for this device. Camel case (for example,
                                myNameIsAlpha), no space, start with alphabet, and
                                alpha - numeric, [default: clientTest]
    -h --help                   Show this screen.
    -n --dbn=<dbnv>             Database name. Only alpha - numeric and under score,
                                [default: sociometric_server].
    -p --dbp=<dbpv>             Database port, [default: 28015].
    -v --version                Show version.
    check                       Check the availability of input devices and/or database.
    reset                       Delete all tables in the database and config file.
    save                        Write setting into configuration file.
    set                         Set and write the configuration variables.
    show config                 Show current configuration values.
    start                       Start this program using previously written configurations.
                                If first time use then it launches wizard.
    start all-default           Start this program using default value.
    start wizard                Start this program guided with configuration wizard.
    without-db                  This program will run without db.
    without-face-detection      This program will run without OpenCV face detection..
    without-ir-detection        This program will run without IR detection.
    without-log                 This program will run without database insertion log.
    without-pv-detection        This program will run without pitch and volume detection.

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

        print(_docArgs)

        docArgs             = _docArgs                              # Arguments supplied from Docopt.

        CONFIG_FILE_NAME    = "config.ini"                          # File name for the configuration file.

        config              = conf()                                # Configuration variable.
        configAbsPath       = os.path.join("./", CONFIG_FILE_NAME)  # Absolute path to the configuration file exist or not.
        conn                = None                                  # For holding information about the connection between this application and the database.
        db                  = None                                  # For holding information about the database.
        firstRun            = False                                 # Check if this application on its first time run (after reset).
        threads             = []                                    # An empty array to hold all threading.Thread object.

        # Threads variables. You may ask on why I am not putting this directly
        # into the `threads` variable. The answer is because not every thread
        # will be put into `threads`. In case `config.withoutPVDetection[2]`
        # is True then `mPVD` will not be in the `threads`.
        cFD     = None
        iDB     = None
        mPVD    = None

        # PENDING - 1, if this application `reset` but then the first run
        # is using `set` command then do not forget to set `first_run`
        # parameter in the `config.ini` to False, because the setting had
        # been set.
        #
        # I want to know the `type()` of `docArgs`.
        #print(type(docArgs))
        # `docArgs` is apparently a native Python dictionary type data.
        #print(docArgs.get("start"))
        #
        # `docArgs.get("start")` will return either True or False depending
        # whether `start` sub - command is used or not when starting this
        # application.
        #
        # Check if there is a configuration file. If not then create one.
        if not os.path.exists(configAbsPath): self.CreateConfig(config,
            configAbsPath)

        # Assign all value into run - time variables.
        self.AssignConfig(config, configAbsPath)

        # Docopt arguments handlers.
        self.DocoptControl(docArgs, config)
        self.ShowConfig(config)

        # Initiates all necessary threads. Check if the
        # config.withoutDatabase[2] is True. If it is True
        # then do not initiate iDB variable.
        #
        # iDB variable is used for a buffer for every value
        # that will be inserted into database.

        #if not config.withoutDB[3]:
        #    # Connect to database.
        #    self.ConnDB(config, conn, db)
        #    # Add database insertion object.
        #    iDB = idb("IDB_1", threads, database,
        #        conn, config)

        #if not config.withoutFaceDetection[3]:
        #    cFD = cfd("CFD_1", threads, iDB)

        #if not config.withoutPVDetection[3]:
        #    mPVD = mpvd("MPVD_1", threads, iDB)

        # Then run all available threads.
        #for t in threads: t.start()

        #Infinite loop.
        #while True:

        #    self.Update(threads)

    # Function to loop.
    def Update(self, _threads):

        try:

            # Join all threads using timeout
            # so it does not block. Filter out
            # thread which have been joined or
            # is a `None`.
            for t in _threads:
                if t.isAlive() and t != None: t.join(1)

        except KeyboardInterrupt as error:

            print(error)
            print("quitting application")
            for t in threads:

                t.killMe = True
                # This is dangerous better find another
                # method on exiting the program. Preferably
                # when all threads are finished then
                # close this program. However, I do not
                # know yet how.
                os._exit(1)

    # Function to create config.ini at this program root directory.
    def CreateConfig(self, _config, _configAbsPath):

        # Create configuration file using FileIO.
        io.FileIO(_configAbsPath, "w")
        cfg     = open(_configAbsPath, "w")
        cfgRaw  = cfgp.ConfigParser()

        cfgRaw.add_section(_config.iniSections[0]) # Database.
        cfgRaw.add_section(_config.iniSections[1]) # Flag.
        cfgRaw.add_section(_config.iniSections[2]) # Setting.

        # Create the configuration value and then add its default value.
        cfgRaw.set(_config.iniSections[0], _config.clientName           [0], _config.clientName             [1])
        cfgRaw.set(_config.iniSections[0], _config.dbAddress            [0], _config.dbAddress              [1])
        cfgRaw.set(_config.iniSections[0], _config.dbName               [0], _config.dbName                 [1])
        cfgRaw.set(_config.iniSections[0], _config.dbPort               [0], _config.dbPort                 [1])

        cfgRaw.set(_config.iniSections[1], _config.firstRun             [0], _config.firstRun               [1])

        cfgRaw.set(_config.iniSections[2], _config.withoutFaceDetection [0], _config.withoutFaceDetection   [1])
        cfgRaw.set(_config.iniSections[2], _config.withoutDB            [0], _config.withoutDB              [1])
        cfgRaw.set(_config.iniSections[2], _config.withoutIRDetection   [0], _config.withoutIRDetection     [1])
        cfgRaw.set(_config.iniSections[2], _config.withoutLog           [0], _config.withoutLog             [1])
        cfgRaw.set(_config.iniSections[2], _config.withoutPVDetection   [0], _config.withoutPVDetection     [1])

        cfgRaw.write(cfg)
        cfg.close()

    # Function to assign value from configuration file (config.ini) into
    # the run - time configuration variables.
    def AssignConfig(self, _config, _configAbsPath):

        # Read the configuration file.
        cfg = cfgp.ConfigParser()
        cfg.read(_configAbsPath)

        # These are variable value taken from the configuration file.
        clientName              = cfg.get(_config.iniSections[0], _config.clientName[0])
        dbAddress               = cfg.get(_config.iniSections[0], _config.dbAddress[0])
        dbName                  = cfg.get(_config.iniSections[0], _config.dbName[0])
        dbPort                  = cfg.get(_config.iniSections[0], _config.dbPort[0])
        firstRun                = cfg.get(_config.iniSections[1], _config.firstRun[0])
        withoutDB               = cfg.get(_config.iniSections[2], _config.withoutDB[0])
        withoutFaceDetection    = cfg.get(_config.iniSections[2], _config.withoutFaceDetection[0])
        withoutIRDetection      = cfg.get(_config.iniSections[2], _config.withoutIRDetection[0])
        withoutLog              = cfg.get(_config.iniSections[2], _config.withoutLog[0])
        withoutPVDetection      = cfg.get(_config.iniSections[2], _config.withoutPVDetection[0])

        # Assign the variables from the configuration file into
        # run - time configuration variables.
        _config.clientName[2]           = clientName
        _config.dbAddress[2]            = dbAddress
        _config.dbName[2]               = dbName
        _config.dbPort[2]               = dbPort
        _config.firstRun[2]             = firstRun
        _config.withoutDB[2]            = withoutDB
        _config.withoutFaceDetection[2] = withoutFaceDetection
        _config.withoutIRDetection[2]   = withoutIRDetection
        _config.withoutLog[2]           = withoutLog
        _config.withoutPVDetection[2]   = withoutPVDetection

        self.ShowConfig(_config)

    # Function to simply print real - time configuration values.
    def ShowConfig(self, _config):

        print("client name                              : " + str(_config.clientName[2]))
        print("database address                         : " + str(_config.dbAddress[2]))
        print("database name                            : " + str(_config.dbName[2]))
        print("database port                            : " + str(_config.dbPort[2]))
        print("first time run                           : " + str(_config.firstRun[2]))
        print("start without face detection             : " + str(_config.withoutFaceDetection[2]))
        print("start without database                   : " + str(_config.withoutDB[2]))
        print("start without ir detection               : " + str(_config.withoutIRDetection[2]))
        print("start without log                        : " + str(_config.withoutLog[2]))
        print("start without pitch and volume detection : " + str(_config.withoutPVDetection[2]))

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

    # Function to control Docopt arguments.
    def DocoptControl(self, _docArgs, _config):

        if _docArgs.get("check"):

            print("check")

            if _docArgs.get("cam"):

                print("cam")

            if _docArgs.get("db"):

                print("db")

            if _docArgs.get("ir"):

                print("ir")

            if _docArgs.get("mic"):

                print("mic")

        if _docArgs.get("reset"):

            print("reset")

        if _docArgs.get("set"):

            print("set")

        if _docArgs.get("show"):

            print("show")

            if _docArgs.get("config"):

                print("config")

        # `start` has four sub command. The first one
        # is start without any additional arguments.
        # And then there is `start all-default [save]`.
        # The `[save]` is an optional arguments. There
        # is `start [without-xxx] [save]`, to start
        # without specific functions. And finally there
        # `start wizard` to start this application
        # with a guided wizard.
        #
        # If `first_run` in the configuration file
        # is True then `start` will actually be
        # `start wizard`.
        if _docArgs.get("start"):

            print("start")

            if _docArgs.get("without-db"):
                print("without-db")
                _config.withoutDB[2] = True
            if _docArgs.get("without-face-detection"):
                print("without-face-detection")
                _config.withoutFaceDetection[2] = True
            if _docArgs.get("without-ir-detection"):
                print("without-ir-detection")
                _config.withoutIRDetection[2] = True
            if _docArgs.get("without-log"):
                print("without-log")
                _config.withoutLog[2] = True
            if _docArgs.get("without-pv-detection"):
                print("without-pv-detection")
                _config.withoutPVDetection[2] = True
            if _docArgs.get("save"):
                print("save")

        if _docArgs.get("start") and _docArgs.get("all-default"):

            print("start all-default")

            if _docArgs.get("save"):

                print("save")

        if _docArgs.get("start") and _docArgs.get("wizard"):

            print("start wizard")

            if _docArgs.get("save"):

                print("save")

def main(_docArgs): main = Main(_docArgs)
if __name__ == "__main__":
    docArgs = doc(__doc__, version="0.0.1")
    main(docArgs)