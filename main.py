"""Sociometric Application

Usage:
    main.py (--help | -h)
    main.py (--version | -v)
    main.py reset [--db]
    main.py set (--cname=<cnamev>|--dba=<dbav>|--dbn=<dbnv>|--dbp=<dbpv>|--db|--faced|--ird|--log|--pvd)...
    main.py set all-default
    main.py show (--config)
    main.py start
    main.py start all-default [--save]
    main.py start without (--db|--faced|--ird|--log|--pvd)... [--save]
    main.py start wizard

Options:
    --help -h           Refer to help manual.
    --version -v        Refer to this version of application.

    --cname=<cnamev>    Refer to client/this device name. Value is
                        a must, [default: clientTest].
    --dba=<dbav>        Refer to RethinkDB database address. Value
                        is a must, [default: 127.0.0.1].
    --dbn=<dbnv>        Refer to RethinkDB database name. Value is
                        a must, [default: sociometric_server].
    --dbp=<dbpv>        Refer to RethinkDB database port. Value is
                        a must, [default: 28015].

    --config            Refer to `config.ini` in the root of this
                        application.
    --db                Refer to RethinkDB database.
    --log               Refer to log that sends JSON document to
                        database.

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

from    cam                                                     import CamFaceDetect                    as cfd                      # Import the face detection object.
from    cli_1                                                   import StartAllDefault                  as sad                      # Function for CLI `start all-deafult`
from    cli_1                                                   import StartSet                         as ss                       # Function for CLI `start set`.
from    cli_1                                                   import StartWithout                     as sw                       # Function for CLI `start set`.
from    cli_2                                                   import StartWizard                      as swi                      # Function for CLI `start wizard`.
from    collection_function_value_manipulation_and_conversion   import AssignAllConfigDefault           as assignallconfigdefault   # Function that convert string into boolean.
from    collection_function_value_manipulation_and_conversion   import AssignAllRTVConfig               as assignallrtvconfig       # Function that convert string into boolean.
from    collection_function_value_manipulation_and_conversion   import GetValueFromConfig               as gvfc                     # Function to get value from `config.ini`.
from    collection_function_value_manipulation_and_conversion   import StringToBool                     as stb                      # Function that convert string into boolean.
from    config                                                  import Config                           as conf                     # Get access to the variables in shared.py.
from    config                                                  import CreateConfig                     as cc                       # Function to create `config.ini` file.
from    config                                                  import ShowConfigFile                   as showcf                   # Function to see `config.ini`.
from    config                                                  import ShowConfigRuntime                as showcr                   # Function to see run time variables.
from    database                                                import ConnDB                           as cdb                      # Import the database inserter.
from    database                                                import InsertDatabase                   as idb                      # Function to connect to database.
from    docopt                                                  import docopt                           as doc                      # Import docopt, the "user interface" library for CLI application.
from    mic                                                     import MicPVDetect                      as mpvd                     # Import the pitch and volume detection object.

import  configparser    as cfgp     # Import library to managing config.
import  io                          # Import io library to deal with opening/writing config file.
import  os                          # Import os Python library to deal with file management.
import  rethinkdb       as r
import  subprocess
import  sys

class Main(object):

    def __init__(self, _docArgs):

        subprocess.call(["reset"])
        print("sociometric client\n")

        #print(_docArgs)

        docArgs                     = _docArgs                              # Arguments supplied from Docopt.

        CONFIG_FILE_NAME            = "config.ini"                          # File name for the configuration file.

        config                      = conf()                                # Configuration variable.
        configAbsPath               = os.path.join("./", CONFIG_FILE_NAME)  # Absolute path to the configuration file exist or not.
        configFileShown             = False                                 # Variable to indicates if `config.ini` file has been shown or not.
        conn                        = None                                  # For holding information about the connection between this application and the database.
        connDB                      = None                                  # Return value from `cdb()`.
        db                          = None                                  # For holding information about the database.
        docoptControl               = None                                  # For holding CLI Docopt control.
        firstRun                    = False                                 # Check if this application on its first time run (after reset).
        continueProgramToMainLoop   = False                                 # If this is `True` then the program will go beyond CLI into main loop.
        threads                     = []                                    # An empty array to hold all threading.Thread object.

        # Threads variables. You may ask on why I am not putting this directly
        # into the `threads` variable. The answer is because not every thread
        # will be put into `threads`. In case `config.withoutPVD[2]`
        # is True then `mPVD` will not be in the `threads`.
        cFD     = None
        iDB     = None
        mPVD    = None

        # PENDING - 1, if this application `reset` but then the first run
        # is using `set` command then do not forget to set `first_run`
        # parameter in the ``config.ini`` to False, because the setting had
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
        if not os.path.exists(configAbsPath): cc(config, configAbsPath)

        # Assign all value into run - time variables.
        assignallrtvconfig(config, configAbsPath)

        # Docopt arguments handlers.
        docoptControl = self.DocoptControl(docArgs, config, configAbsPath)
        if not docoptControl[0] and not docoptControl[2]: showcf(config, configAbsPath)

        # Terminate the program right here if there is no start command
        # issued in CLI.
        if docoptControl[1]:

            # Show run time variables.
            showcr(config)

            # First I need to check if database will be used or not.
            if config.withoutDB[0]: connDB = cdb(config, True)
            # `connDB[0]` returns `True` if database connection is successful.
            if connDB != None:
                if connDB[0]:
                    db      = connDB[1]
                    conn    = connDB[2]

            #print(config.withoutDB         [2])
            #print(config.withoutFaceD      [2])
            #print(config.withoutPVD        [2])
            #print(stb(config.withoutDB     [2]))
            #print(stb(config.withoutFaceD  [2]))
            #print(stb(config.withoutPVD    [2]))
            #
            # In any case `iDB` will still be instantiated.
            # Only the database connection will not be used
            # in case of `config.withoutDB[2]` is `True.`
            iDB = idb("IDB_1", threads, config, config.withoutDB[2], db, conn)

            if not stb(config.withoutFaceD  [2]): cFD     = cfd   ("CFD_1"    , threads, iDB)
            if not stb(config.withoutPVD    [2]): mPVD    = mpvd  ("MPVD_1"   , threads, iDB)

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
    def DocoptControl(self, _docArgs, _config, _configAbsPath):

        # This variable need to be here so that `show --config`
        # will not return twice `showcf(_config, _configAbsPath)`.
        configFileShown             = False
        # This variable is to indicate if this application will
        # continued into main infinite loop after Docopt CLI.
        continueProgramToMainLoop   = False
        # If `config.ini` is deleted or not.
        deletedConfig               = False

        if _docArgs.get("reset"):

            if _docArgs.get("--db"):
                # Try to connect to database.
                connDB = cdb(_config, False)
                if connDB != None:
                    if connDB[0]:

                        conn = connDB[2]
                        # Delete all tables. But first get all table list.
                        dbNameFromConfig = str(gvfc(_configAbsPath, _config.iniSections[0], _config.dbName[0]))
                        try:
                            r.db_drop(dbNameFromConfig).run(conn)
                            print("database deleted")
                        except r.errors.ReqlOpFailedError as error: print("database does not exists")


            # For reset we need to get connection to database to delete all table
            # and also to delete the config.ini file in the root of this project
            # directory.
            #
            # Delete config.ini file.
            os.remove(_configAbsPath)
            deletedConfig = True
            print("config.ini deleted")

        if _docArgs.get("set"):
            if _docArgs.get("all-default"): assignallconfigdefault(_docArgs, _config, _configAbsPath)
            else: ss(_docArgs, _config, _configAbsPath)
        if _docArgs.get("show") and _docArgs.get("--config"):
            configFileShown = True
            showcf(_config, _configAbsPath)
        if _docArgs.get("start"):
            # `start all-default` let user to
            # use default components (using all
            # inputs and detections). And as well
            # as database setting variables.
            if _docArgs.get("all-default"): sad(_docArgs, _config, _configAbsPath)
            # `start without` command let user specify
            # which components to use and which ones not
            # to use. The rest is taken from the `config.ini`.
            elif _docArgs.get("without"): sw(_docArgs, _config, _configAbsPath)
            # If this is first run then every time
            # this application launches go to here.
            elif _docArgs.get("wizard"): swi(_config, _configAbsPath)

            # If `start` is used this application will go into main loop.
            continueProgramToMainLoop = True

        return [configFileShown, continueProgramToMainLoop, deletedConfig]

def main(_docArgs): main = Main(_docArgs)
if __name__ == "__main__":
    docArgs = doc(__doc__, version="0.0.1")
    main(docArgs)
