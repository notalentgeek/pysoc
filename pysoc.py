"""Sociometric Application

Usage:
    main.py (--help | -h)
    main.py (--version | -v)
    main.py reset [--dbl]
    main.py set (--cname=<cnamev>|--dba=<dbav>|--dbn=<dbnv>|--dbp=<dbpv>|--irc=<ircv>|--cvgui|--db|--faced|--ird|--log|--pvd)...
    main.py set all-default
    main.py show (--config)
    main.py start [--rpi [--picam]]
    main.py start all-default [--rpi [--picam]] [--save]
    main.py start without (--cvgui|--db|--faced|--ird|--log|--pvd)... [--rpi [--picam]] [--save]
    main.py start wizard

Options:
    --help -h           Refer to help manual.
    --version -v        Refer to this version of application.

    --cname=<cnamev>    Refer to client/this device name. Value is
                        a must.
    --dba=<dbav>        Refer to RethinkDB database address. Value
                        is a must.
    --dbn=<dbnv>        Refer to RethinkDB database name. Value is
                        a must.
    --dbp=<dbpv>        Refer to RethinkDB database port. Value is
                        a must.
    --irc=<ircv>        Refer to LIRC's IR code. Value is a must.

    --rpi               Start this application in Raspberry PI's
                        Raspbian instead of normal desktop operating
                        system.
    --picam             Refer to ribbon camera of the Raspberry PI.
                        This ribbon camera is located between the 3.5mm
                        output jack and HDMI in Raspberry PI 3. If
                        you want to use USB camera then do not use this
                        arguments.

    --config            Refer to `config.ini` in the root of this
                        application.
    --db                Refer to RethinkDB database.
    --dbl               Refer to RethinkDB database and log folder.
    --log               Refer to log that prints JSON document to
                        database. Log still written in `./log/` at
                        any case.

    --cvgui             Refer to OpenCV face detection GUI.

    --cam               Refer to cam/webcam.
    --ir                Refer to IR.
    --mic               Refer to microphone.

    --faced             Refer to face detection using `--cam`.
    --ird               Refer to IR detection using `--ir`.
    --pvd               Refer to pitch and volume detection using
                        `--mic`.

    --save              Write all values into configuration .ini
                        files. Otherwise, value will only for
                        current runtime.

    check               Check component(s). Additional argument(s)
                        is necessary.
    reset               Set configuration values in .ini file to
                        their default values. This command also
                        delete database that is named in `config.ini`.
    set                 Command to set client name, database
                        configurations variables and component flags.
                        The component flags will reverse between
                        True to False for each `set`. These values
                        will be automatically `--save` into the
                        configuration file.
    set all-default     Command to write every default values
                        (except config.firstRun) into the `config.ini`.
    show                To show something :D.
    start               Start this application with values from
                        the configuration file.
    start all-default   Start this application with default values.
    start without       Start this application without component(s).
                        Additional argument(s) is necessary.
    start wizard        Start this application with wizard.

"""
import sys
sys.path.append("./src/cli")
sys.path.append("./src/collection_function")
sys.path.append("./src/config_and_database")
sys.path.append("./src/input")
sys.path.append("./src/other")

from    cam                                                     import CamFaceDetect                    as cfd                      # Import the face detection object.
from    cascade_front_face_default                              import cascadeFrontFaceDefault          as ccfd                     # Cascade .xml string.
from    cli_1                                                   import Set                              as ss                       # Function for CLI `set`.
from    cli_1                                                   import StartAllDefault                  as sad                      # Function for CLI `start all-deafult`
from    cli_1                                                   import StartRPI                         as srpi                     # Function to let user choose if they are using Raspberry PI.
from    cli_1                                                   import StartWithout                     as sw                       # Function for CLI `start without`.
from    cli_2                                                   import StartWizard                      as swi                      # Function for CLI `start wizard`.
from    collection_function_value_manipulation_and_conversion   import AssignAllConfigDefault           as assignallconfigdefault   # Function that convert string into boolean.
from    collection_function_value_manipulation_and_conversion   import AssignAllRTVConfig               as assignallrtvconfig       # Function that convert string into boolean.
from    collection_function_value_manipulation_and_conversion   import GetValueFromConfig               as gvfc                     # Function to get value from `config.ini`.
from    collection_function_value_manipulation_and_conversion   import SaveValue                        as sv                       # Function that convert string into boolean.
from    collection_function_value_manipulation_and_conversion   import StringToBool                     as stb                      # Function that convert string into boolean.
from    config                                                  import Config                           as conf                     # Get access to the variables in shared.py.
from    config                                                  import CreateConfig                     as cc                       # Function to create `config.ini` file.
from    config                                                  import DeleteConfig                     as dc                       # Function to delete `config.ini`.
from    config                                                  import ShowConfigFile                   as showcf                   # Function to see `config.ini`.
from    config                                                  import ShowConfigRuntime                as showcr                   # Function to see run time variables.
from    database                                                import ConnDB                           as cdb                      # Import the database inserter.
from    database                                                import DeleteDatabaseAndLog             as ddl                      # Function to delete database and log folder.
from    database                                                import InsertDatabase                   as idb                      # Function to connect to database.
from    docopt                                                  import docopt                           as doc                      # Import docopt, the "user interface" library for CLI application.
from    ir_receiver                                             import IRDetection                      as ird
from    ir_transmit                                             import IRSend                           as irs
from    mic                                                     import MicPVDetect                      as mpvd                     # Import the pitch and volume detection object.
from    sys                                                     import platform
from    timer_second_change                                     import GetDateTime                      as gdt                      # Function to get date, time, and time zone as well.

import  configparser    as cfgp     # Import library to managing config.
import  datetime        as dt       # To know operating system current time.
import  io                          # Import io library to deal with opening/writing config file.
import  os                          # Import os Python library to deal with file management.
import  rethinkdb       as r        # RethinkDB controller for Python.
import  subprocess      as subp     # Getting access to subp to run command into command prompt or terminal.
import  tzlocal                     # For getting information about time zone.

class Main(object):

    def __init__(self, _docArgs):

        # Codes to clear the terminal screen before launching this application.
        if   platform == "darwin" or platform == "linux" or platform == "linux2": subp.call(["reset"])
        elif platform == "cygwin" or platform == "win32"                        : subp.call(["cls"])

        print("sociometric client\n")

        #print(_docArgs)

        docArgs                     = _docArgs                                          # Arguments supplied from Docopt.

        CASCADE_FRONT_FACE_DEF_NAME = "cascade_face_front_default.xml"                  # Cascade file name.
        CONFIG_FILE_NAME            = "config.ini"                                      # File name for the configuration file.
        LOG_FOLDER_NAME             = "log"

        cascAbsPath                 = os.path.join("./", CASCADE_FRONT_FACE_DEF_NAME)
        config                      = conf()                                            # Configuration variable.
        configAbsPath               = os.path.join("./", CONFIG_FILE_NAME)              # Absolute path to the configuration file exist or not.
        conn                        = None                                              # For holding information about the connection between this application and the database.
        connDB                      = None                                              # Return value from `cdb()`.
        db                          = None                                              # For holding information about the database.
        docoptControl               = None                                              # For holding CLI Docopt control.
        logAbsPath                  = None                                              # Absolute path into current `log.txt`.
        logFolderAbsPath            = os.path.join("./", LOG_FOLDER_NAME)               # Absolute path into the `log` folder.
        threads                     = []                                                # An empty array to hold all threading.Thread object.

        # Threads variables. You may ask on why I am not putting this directly
        # into the `threads` variable. The answer is because not every thread
        # will be put into `threads`. In case `config.withoutPVD[2]`
        # is True then `mPVD` will not be in the `threads`.
        cFD     = None
        iDB     = None
        iRD     = None
        iRS     = None
        mPVD    = None

        # Generate the cascade .xml for front face detection.
        if not os.path.exists(cascAbsPath):
            io.FileIO(cascAbsPath, "w")
            with open(cascAbsPath, "a") as cascXML:
                cascXML.write(ccfd)
            print("cascade file created")

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
        if not os.path.exists(configAbsPath): cc(config, configAbsPath)

        # Assign all value into run - time variables.
        # Use `try` and except. If there is an error
        # delete the current config.ini and make a new
        # one.
        try: assignallrtvconfig(config, configAbsPath)
        except cfgp.NoOptionError as error:
            print("there is missing parameter(s) in current configuration file")
            print("deleting config.ini")
            os.remove(configAbsPath)
            print("creating new config.ini")
            cc(config, configAbsPath)

        # Docopt arguments handlers.
        docoptControl = self.DocoptControl(docArgs, config, configAbsPath, logFolderAbsPath)
        if not docoptControl[0] and not docoptControl[2]: showcf(config, configAbsPath)

        # Terminate the program right here if there is no start command
        # issued in CLI.
        if docoptControl[1]:

            # Show run time variables.
            showcr(config)

            # Create log folder here. Check if there something
            # in the `logFolderAbsPath`.
            if os.path.exists(logFolderAbsPath):

                # If there is something exists then check if the
                # thing is a folder or not. If the thing is not
                # a folder then create new folder in `logFolderAbsPath`
                if not os.path.isdir(logFolderAbsPath):
                    os.makedirs(logFolderAbsPath)
                    print("log folder created")

            else:

                    os.makedirs(logFolderAbsPath)
                    print("log folder created")

            # Create log file for this session.
            gDT = gdt()
            logName = (
                config.clientName[2] + "-" +
                gDT[0] + gDT[1] + gDT[2] + "-" +
                gDT[3] + gDT[4] + gDT[5] + "-" +
                gDT[6].replace("/", "-") + ".txt")
            logAbsPath = os.path.join(logFolderAbsPath, logName)
            if os.path.exists(logAbsPath):

                if os.path.isdir(logAbsPath):
                    io.FileIO(logAbsPath, "w")
                    print(logName + " log created")

            else:

                    io.FileIO(logAbsPath, "w")
                    print(logName + " log created")

            # First I need to check if database will be used or not.
            if not config.withoutDB[2]: connDB = cdb(config, True)
            # `connDB[0]` returns `True` if database connection is successful.
            if connDB != None:
                if connDB[0]:
                    db      = connDB[1]
                    conn    = connDB[2]

            # In any case `iDB` will still be instantiated.
            # Only the database connection will not be used
            # in case of `config.withoutDB[2]` is `True.`
            iDB = idb("IDB_1", threads, config, config.withoutDB[2], db, conn, logAbsPath)

            # `docoptControl[3]` is a variable that states if user choose to run this
            # application in Raspberry PI's Raspbian Jessie environment.
            #
            # The cam face detection only care if the user uses PiCamera or normal USB
            # web cam. Hence, `docoptControl[3][1]` will return `True` if Docopt argument
            # `--picam` is used.
            #
            # While the pitch and volume detection need to know the operating system it
            # runs because it need to detect default sound card. Hence, `docoptControl[3][0]`
            # refer to Docopt argument `--rpi`. User need to choose this if this application
            # runs in Raspberry PI' Raspbian Jessie. I do not make any programming for other
            # Raspberry compatible OS but Raspbian Jessie.
            if not stb(config.withoutFaceD  [2]): cFD     = cfd   ("CFD_1"    , threads, iDB, docoptControl[3][1], config)   # Camera face detection.
            if not stb(config.withoutPVD    [2]): mPVD    = mpvd  ("MPVD_1"   , threads, iDB, docoptControl[3][0])           # Microphone pitch and volume detection.
            if not stb(config.withoutIRD    [2]):
                iRD = ird("IRD_1", threads, iDB)
                iRS = irs("IRS_1", threads, config)

            # Then run all available threads.
            for t in threads: t.start()

            #Infinite loop.
            while True:

                self.Update(threads)

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
            for t in _threads:

                t.killMe = True
                # This is dangerous better find another
                # method on exiting the program. Preferably
                # when all threads are finished then
                # close this program. However, I do not
                # know yet how.
                os._exit(1)

    # Function to control Docopt arguments.
    def DocoptControl(self, _docArgs, _config, _configAbsPath, _logFolderAbsPath):

        # This variable need to be here so that `show --config`
        # will not return twice `showcf(_config, _configAbsPath)`.
        configFileShown             = False
        # This variable is to indicate if this application will
        # continued into main infinite loop after Docopt CLI.
        continueProgramToMainLoop   = False
        # If `config.ini` is deleted or not.
        deletedConfig               = False
        # Check if user choose to start with Raspberry PI Raspbian.
        raspberryPI                 = [False, False]

        # Get `first_run` value from `config.ini`.
        firstRun                    = stb(gvfc(_configAbsPath, _config.iniSections[1], _config.firstRun[0]))

        if _docArgs.get("reset"):
            # For reset we need to get connection to database to delete all table
            # and also to delete the config.ini file in the root of this project
            # directory.
            if _docArgs.get("--dbl"): ddl(_config, _configAbsPath, _logFolderAbsPath)
            # Delete the `config.ini` and then give `True` into the `deletedConfig`.
            deletedConfig = dc(_configAbsPath)
        if _docArgs.get("set"):
            # Set to all default variables.
            if _docArgs.get("all-default"): assignallconfigdefault(_docArgs, _config, _configAbsPath)
            # Set everything manually.
            else: ss(_docArgs, _config, _configAbsPath)
            # If user ever once set something than prevent
            # wizard from appearing when `start` command
            # inputted
            sv(_config, _configAbsPath, _docArgs, 1, _config.firstRun[0], False)
            _config.firstRun[2] = False
        if _docArgs.get("show") and _docArgs.get("--config"):
            configFileShown = True
            showcf(_config, _configAbsPath)
        if _docArgs.get("start"):
            if firstRun:
                # Start the wizard.
                sWI = swi(_docArgs, _config, _configAbsPath)
                raspberryPI = [sWI[0], sWI[1]]
                sv(_config, _configAbsPath, _docArgs, 1, _config.firstRun[0], False)
                _config.firstRun[2] = False
            else:
                # `start all-default` let user to
                # use default components (using all
                # inputs and detections). And as well
                # as database setting variables.
                if _docArgs.get("all-default"): raspberryPI = sad(_docArgs, _config, _configAbsPath)
                # `start without` command let user specify
                # which components to use and which ones not
                # to use. The rest is taken from the `config.ini`.
                elif _docArgs.get("without"): raspberryPI = sw(_docArgs, _config, _configAbsPath)
                # If this is first run then every time
                # this application launches go to here.
                elif _docArgs.get("wizard"):
                    sWI = swi(_docArgs, _config, _configAbsPath)
                    raspberryPI = [sWI[0], sWI[1]]
                    sv(_config, _configAbsPath, _docArgs, 1, _config.firstRun[0], False)
                    _config.firstRun[2] = False
                # If there is no other parameters support the `start` command
                # check if user want to start this in Raspberry PI or normal
                # operating system.
                else: raspberryPI = srpi(_docArgs)

            # If `start` is used this application will go into main loop.
            continueProgramToMainLoop = True

        return [configFileShown, continueProgramToMainLoop, deletedConfig, raspberryPI]

def main(_docArgs): main = Main(_docArgs)
if __name__ == "__main__":
    docArgs = doc(__doc__, version="0.0.1")
    main(docArgs)
