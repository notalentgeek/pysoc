"""Sociometric Application

Usage:
    main.py (--help | -h)
    main.py (--version | -v)
    main.py reset
    main.py set (--cname=<cnamev>|--dba=<dbav>|--dbn=<dbnv>|--dbp=<dbpv>|--db|--faced|--ird|--log|--pvd)...
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

    --config            Refer to config.ini in the root of this
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
                        delete all database log and tables.
    set                 Command to set client name, database
                        configurations variables and component flags.
                        The component flags will reverse between
                        True to False for each `set`.
    show                To show something :D.
    start               Start this application with values from
                        the configuration file.
    start all-default   Start this application with default values.
    start without       Start this application without component(s).
                        Additional argument(s) is necessary.
    start wizard        Start this application with wizard.

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
import  subprocess
import  sys

class Main(object):

    def __init__(self, _docArgs):

        subprocess.call(["reset"])
        print("sociometric client")

        #print(_docArgs)

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
        # will be put into `threads`. In case `config.withoutPVD[2]`
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
        self.DocoptControl(docArgs, config, configAbsPath)

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

        #if not config.withoutFaceD[3]:
        #    cFD = cfd("CFD_1", threads, iDB)

        #if not config.withoutPVD[3]:
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

        cfgRaw.set(_config.iniSections[2], _config.withoutFaceD [0], _config.withoutFaceD   [1])
        cfgRaw.set(_config.iniSections[2], _config.withoutDB            [0], _config.withoutDB              [1])
        cfgRaw.set(_config.iniSections[2], _config.withoutIRD   [0], _config.withoutIRD     [1])
        cfgRaw.set(_config.iniSections[2], _config.withoutLog           [0], _config.withoutLog             [1])
        cfgRaw.set(_config.iniSections[2], _config.withoutPVD   [0], _config.withoutPVD     [1])

        cfgRaw.write(cfg)
        cfg.close()

    # Function to assign value from configuration file (config.ini) into
    # the run - time configuration variables.
    def AssignConfig(self, _config, _configAbsPath):

        # Read the configuration file.
        cfg = cfgp.ConfigParser()
        cfg.read(_configAbsPath)

        # These are variable value taken from the configuration file.
        clientName      = cfg.get(_config.iniSections[0], _config.clientName[0])
        dbAddress       = cfg.get(_config.iniSections[0], _config.dbAddress[0])
        dbName          = cfg.get(_config.iniSections[0], _config.dbName[0])
        dbPort          = cfg.get(_config.iniSections[0], _config.dbPort[0])
        firstRun        = cfg.get(_config.iniSections[1], _config.firstRun[0])
        withoutDB       = cfg.get(_config.iniSections[2], _config.withoutDB[0])
        withoutFaceD    = cfg.get(_config.iniSections[2], _config.withoutFaceD[0])
        withoutIRD      = cfg.get(_config.iniSections[2], _config.withoutIRD[0])
        withoutLog      = cfg.get(_config.iniSections[2], _config.withoutLog[0])
        withoutPVD      = cfg.get(_config.iniSections[2], _config.withoutPVD[0])

        # Assign the variables from the configuration file into
        # run - time configuration variables.
        _config.clientName[2]       = clientName
        _config.dbAddress[2]        = dbAddress
        _config.dbName[2]           = dbName
        _config.dbPort[2]           = dbPort
        _config.firstRun[2]         = firstRun
        _config.withoutDB[2]        = self.StringToBool(withoutDB)
        _config.withoutFaceD[2]     = self.StringToBool(withoutFaceD)
        _config.withoutIRD[2]       = self.StringToBool(withoutIRD)
        _config.withoutLog[2]       = self.StringToBool(withoutLog)
        _config.withoutPVD[2]       = self.StringToBool(withoutPVD)

    # Function to simply print real - time configuration values.
    def ShowConfig(self, _config):

        print("client name                              : " + str(_config.clientName[2]))
        print("database address                         : " + str(_config.dbAddress[2]))
        print("database name                            : " + str(_config.dbName[2]))
        print("database port                            : " + str(_config.dbPort[2]))
        print("first time run                           : " + str(_config.firstRun[2]))
        print("start without face detection             : " + str(_config.withoutFaceD[2]))
        print("start without database                   : " + str(_config.withoutDB[2]))
        print("start without ir detection               : " + str(_config.withoutIRD[2]))
        print("start without log                        : " + str(_config.withoutLog[2]))
        print("start without pitch and volume detection : " + str(_config.withoutPVD[2]))

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
    def DocoptControl(self, _docArgs, _config, _configAbsPath):

        # Function to get value from config.ini.
        def GetValueFromConfig(_configAbsPath,
            _sectionName, _variableName):

            cfg = cfgp.ConfigParser()
            cfg.read(_configAbsPath)
            returnValue = cfg.get(_sectionName, _variableName)

            return returnValue

        # This function is used to write value into
        # the configuration file.
        def SaveValue(_config, _configAbsPath, _docArgs,
            _iniSectionsIndex, _variableNameInConfigFile,
            _value):

            # If there is a save parameter then
            # write the setting into configuration
            # .ini file as well.
            print(_docArgs.get("set"))

            if _docArgs.get("--save") or (
                _docArgs.get("set")):

                #print("--save")

                # Create the parser object.
                cfgRaw = cfgp.ConfigParser()
                # Read the configuration configuration path.
                cfgRaw.read(_configAbsPath)
                # Set the value!
                cfgRaw.set(_config.iniSections[_iniSectionsIndex],
                    _variableNameInConfigFile, str(_value))

                #print("==========")
                #print(str(value))
                #print("==========")

                # Write the value.
                with open(_configAbsPath, "w") as cfg:
                    cfgRaw.write(cfg)

        if _docArgs.get("reset"):

            print("reset")





        if _docArgs.get("set"):
            #print("set")
            if _docArgs.get("--cname"):
                value = _docArgs.get("--cname")[0]
                SaveValue(_config, _configAbsPath, _docArgs, 0,
                    _config.clientName[0], value)
                print("--cname")
            if _docArgs.get("--dba"):
                value = _docArgs.get("--dba")[0]
                SaveValue(_config, _configAbsPath, _docArgs, 0,
                    _config.dbAddress[0], value)
                print("--dba")
            if _docArgs.get("--dbn"):
                value = _docArgs.get("--dbn")[0]
                SaveValue(_config, _configAbsPath, _docArgs, 0,
                    _config.dbName[0], value)
                print("--dbn")
            if _docArgs.get("--dbp"):
                value = _docArgs.get("--dbp")[0]
                SaveValue(_config, _configAbsPath, _docArgs, 0,
                    _config.dbPort[0], value)
                print("--dbp")
            if _docArgs.get("--db"):
                # I need to get the value first.
                currentValueInConfigFile = self.StringToBool(GetValueFromConfig(_configAbsPath,
                     _config.iniSections[2], _config.withoutDB[0]))
                # After I get the boolean value then I need
                # to invert the value.
                changedValue = not currentValueInConfigFile
                print(currentValueInConfigFile)
                print(changedValue)
                # After I invert the value I need to write the value
                # back into config.ini file.
                SaveValue(_config, _configAbsPath, _docArgs, 2,
                    _config.withoutDB[0], changedValue)
                print("--db")
            if _docArgs.get("--faced"):
                currentValueInConfigFile = self.StringToBool(GetValueFromConfig(_configAbsPath,
                     _config.iniSections[2], _config.withoutFaceD[0]))
                changedValue = not currentValueInConfigFile
                print(currentValueInConfigFile)
                print(changedValue)
                SaveValue(_config, _configAbsPath, _docArgs, 2,
                    _config.withoutFaceD[0], changedValue)
                print("--faced")
            if _docArgs.get("--ird"):
                currentValueInConfigFile = self.StringToBool(GetValueFromConfig(_configAbsPath,
                     _config.iniSections[2], _config.withoutIRD[0]))
                changedValue = not currentValueInConfigFile
                print(currentValueInConfigFile)
                print(changedValue)
                SaveValue(_config, _configAbsPath, _docArgs, 2,
                    _config.withoutIRD[0], changedValue)
                print("--ird")
            if _docArgs.get("--log"):
                currentValueInConfigFile = self.StringToBool(GetValueFromConfig(_configAbsPath,
                     _config.iniSections[2], _config.withoutLog[0]))
                changedValue = not currentValueInConfigFile
                print(currentValueInConfigFile)
                print(changedValue)
                SaveValue(_config, _configAbsPath, _docArgs, 2,
                    _config.withoutLog[0], changedValue)
                print("--log")
            if _docArgs.get("--pvd"):
                currentValueInConfigFile = self.StringToBool(GetValueFromConfig(_configAbsPath,
                     _config.iniSections[2], _config.withoutPVD[0]))
                changedValue = not currentValueInConfigFile
                print(currentValueInConfigFile)
                print(changedValue)
                SaveValue(_config, _configAbsPath, _docArgs, 2,
                    _config.withoutPVD[0], changedValue)
                print("--pvd")





        # The command `show` is to show something.
        # However, until now there is no other
        # implementation other than to `show --config`
        if _docArgs.get("show"):
            #print("show")
            if _docArgs.get("--config"):
                #print("--config")
                self.ShowConfig(_config)






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





            # `start all-default` let user to
            # use default components (all inputs
            # detections are set to True).
            #
            # However, database settings and
            # this application client name will
            # be the same.
            if _docArgs.get("all-default"):

                #print("start all-default")

                # The index no `2` is the runtime value.
                # While the index no `1` is the default
                # value. The index `0` is the config.ini
                # sub - section entry name.
                _config.withoutDB[2]    = _config.withoutDB[1]
                _config.withoutFaceD[2] = _config.withoutFaceD[1]
                _config.withoutIRD[2]   = _config.withoutIRD[1]
                _config.withoutLog[2]   = _config.withoutLog[1]
                _config.withoutPVD[2]   = _config.withoutPVD[1]

                if _docArgs.get("--save"):

                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutDB[0], _config.withoutDB[1])
                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutFaceD[0], _config.withoutFaceD[1])
                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutIRD[0], _config.withoutIRD[1])
                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutLog[0], _config.withoutLog[1])
                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutPVD[0], _config.withoutPVD[1])




            # `start without` command let user specify
            # which components to use and which ones not
            # to use. The rest is taken from the config.ini.
            elif _docArgs.get("without"):

                #print("start without")

                # Whether or not this application run with
                # RethinkDB database or not.
                if _docArgs.get("--db"):
                    #print("--db")
                    # Change the value in the configuration
                    # run - time variable so that this
                    # application does not use database.
                    _config.withoutDB[2] = True
                    # Save the value if _docArgs.("save")
                    # returns True.
                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutDB[0], True)

                # Whether this application is using face
                # detection or not.
                if _docArgs.get("--faced"):
                    #print("--faced")
                    _config.withoutFaceD[2] = True
                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutFaceD[0], True)

                # Whether this application is using IR
                # detection or not.
                if _docArgs.get("--ird"):
                    #print("--ird")
                    _config.withoutIRD[2] = True
                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutIRD[0], True)

                # Whether this application will show
                # JSON log or not. JSON logs are those
                # who will put into RethinkDB database.
                if _docArgs.get("--log"):
                    #print("--log")
                    _config.withoutLog[2] = True
                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutLog[0], True)

                # Whether this application is using pitch
                # and volume detection or not.
                if _docArgs.get("--pvd"):
                    #print("--pvd")
                    _config.withoutPVD[2] = True
                    SaveValue(_config, _configAbsPath, _docArgs,
                        2, _config.withoutPVD[0], True)





            # If this is first run then every time
            # this application launches go to here.
            elif _docArgs.get("wizard"):

                #print("start wizard")

                # Starting the application wizard
                # here. But first please the
                # `run_first` parameter in the
                # config.ini. If it is `True`
                # then display additional message.
                firstRun = GetValueFromConfig(_configAbsPath,
                    _config.iniSections[1],
                    _config.firstRun[0])

                #print(firstRun)

                # PENDING - 1,  variable naming convention change all into
                # positive variable name. For example change `_config.withoutDB`
                # to `_config.withDB` or `_config.useDB`.
                defaultClientName       = "default                  : do not fill and just press enter to fill the default value of \"clientTest\""
                defaultDBAddress        = "default                  : do not fill and just press enter to fill the default value of \"127.0.0.1\""
                defaultDBName           = "default                  : do not fill and just press enter to fill the default value of \"sociometric_server\""
                defaultDBPort           = "default                  : do not fill and just press enter to fill the default value of \"28015\""
                defaultWithout          = "default                  : do not fill and just press enter to automatically response \"yes\""
                exampleClientName       = "example                  : \"richardDawkins\""
                exampleDBAddress        = "example                  : \"127.0.0.1\""
                exampleDBName           = "example                  : \"sociometric_badge\""
                exampleDBPort           = "example                  : \"28015\""
                exampleWithout          = "example                  : \"no\"/\"n\" for not using this features or \"yes\"/\"y\" for using this features"
                inputClientName         = "client name              : "
                inputDBAddress          = "database address         : "
                inputDBName             = "database name            : "
                inputDBPort             = "database port            : "
                inputDB                 = "do you want to use database? "
                inputFaceD              = "do you want to use face detection? "
                inputIRD                = "do you want to use infrared detection? "
                inputLog                = "do you want to use log? "
                inputPVD                = "do you want to use pitch and volume detection? "
                inputSave               = "do you want to save this setting? "
                requirementClientName   = "requirement              : no space, case sensitive, alpha - numeric, camelCase"
                requirementDBAddress    = "requirement              : no space, not case sensitive, alpha - numeric"
                requirementDBName       = "requirement              : no space, lower case, alpha - numeric, underscore_case"
                requirementDBPort       = "requirement              : no space, numeric"
                requirementWithout      = "requirement              : no space, not case sensitive"





                # PENDING - 1, there are definitely a lot to be tweak
                # here. I was very lazy to think at the time I was
                # writing this codes.
                def InputClientName(_requirement, _example,
                    _defaultString, _input):

                    illegal = True

                    #print("\n")

                    # If the string inputted illegal keep
                    # asking the user to input it.
                    description = "\nplease input client name"
                    while illegal:
                        print(description)
                        print(_requirement)
                        print(_example)
                        print(_defaultString)
                        _config.clientName[2] = input(_input)

                        description = "please input client name"

                        # If empty "" give the `_config.clientName[2]`
                        # a default value and then break this
                        # loop by `illegal = False`.
                        if CheckIfStringIsBlank(_config.clientName[2]):
                            _config.clientName[2] = _config.clientName[1]
                            illegal = False

                        illegal = CheckIfStringIsAlphaNumeric(
                            _config.clientName[2])
                        if illegal: print("\ninput failed\n")





                def InputDBAddress(_requirement, _example,
                    _defaultString, _input):

                    illegal = True

                    description = "\nplease input rethinkdb database address"
                    while illegal:
                        print(description)
                        print(_requirement)
                        print(_example)
                        print(_defaultString)
                        _config.dbAddress[2] = input(_input)

                        description = "please input rethinkdb database address"

                        if CheckIfStringIsBlank(_config.dbAddress[2]):
                            _config.dbAddress[2] = _config.dbAddress[1]
                            illegal = False

                        illegal = CheckIfStringIsAlphaNumericDot(
                            _config.dbAddress[2])
                        if illegal: print("\ninput failed\n")





                def InputDBName(_requirement, _example,
                    _defaultString, _input):

                    illegal = True

                    description = "\nplease input rethinkdb database name"
                    while illegal:
                        print(description)
                        print(_requirement)
                        print(_example)
                        print(_defaultString)
                        _config.dbName[2] = input(_input).lower()

                        description = "please input rethinkdb database name"

                        if CheckIfStringIsBlank(_config.dbName[2]):
                            _config.dbName[2] = _config.dbName[1]
                            illegal = False

                        illegal = CheckIfStringIsAlphaNumericUScore(
                            _config.dbName[2])
                        if illegal: print("\ninput failed\n")





                def InputDBPort(_requirement, _example,
                    _defaultString, _input):

                    illegal = True

                    description = "\nplease input rethinkdb database port"
                    while illegal:
                        print(description)
                        print(_requirement)
                        print(_example)
                        print(_defaultString)
                        _config.dbPort[2] = input(_input)

                        description = "please input rethinkdb database port"

                        if CheckIfStringIsBlank(_config.dbPort[2]):
                            _config.dbPort[2] = _config.dbPort[1]
                            illegal = False

                        illegal = CheckIfStringIsNumeric(
                            _config.dbPort[2])
                        if illegal: print("\ninput failed\n")





                def InputSave(_input):

                    noStatement = ["0", "f", "false", "n","no"]
                    yesStatement = ["", "1", "t", "true", "y", "yes"]

                    illegal = True

                    while illegal:

                        inpectThis = input("\n" + _input)

                        if inpectThis.lower() in noStatement:
                            _configVariable = True
                        elif inpectThis.lower() in yesStatement:
                            _configVariable = False
                        else: _configVariable = None

                        if _configVariable != None: illegal = False
                        if CheckIfStringIsBlank(_configVariable):
                            _configVariable = False





                def InputWithoutComponent(_input, _configVariable,
                    _configDefault):

                    noStatement = ["0", "f", "false", "n","no"]
                    yesStatement = ["", "1", "t", "true", "y", "yes"]

                    illegal = True

                    while illegal:

                        inpectThis = input(_input)

                        #print(inpectThis.lower())
                        #print(inpectThis.lower() in noStatement)
                        #print(inpectThis.lower() in yesStatement)

                        if inpectThis.lower() in noStatement:
                            _configVariable = True
                            #print(_configVariable)
                        elif inpectThis.lower() in yesStatement:
                            _configVariable = False
                            #print(_configVariable)
                        else: _configVariable = None

                        #print(_configVariable)

                        if _configVariable != None: illegal = False
                        if CheckIfStringIsBlank(_configVariable):
                            _configVariable = _configDefault





                # Function to check if a string is blank
                # string or not.
                def CheckIfStringIsBlank(_string):
                    return not (str(_string) and str(_string).strip())
                # Function to check if a string is only
                # alpha numeric or not.
                def CheckIfStringIsAlphaNumeric(_string):
                    returnBool = False
                    for l in _string:
                        if l.isalnum(): returnBool = False
                        else:
                            returnBool = True
                            break
                    return returnBool
                # Function to check if a string is only
                # alpha numeric and dot "." or not.
                def CheckIfStringIsAlphaNumericDot(_string):
                    returnBool = False
                    for l in _string:
                        if l == "." or l.isalnum():
                            returnBool = False
                        else:
                            returnBool = True
                            break
                    return returnBool
                # Function to check if a string is only
                # alpha numeric and under score "_" or not.
                def CheckIfStringIsAlphaNumericUScore(_string):
                    returnBool = False
                    for l in _string:
                        if l == "_" or l.isalnum():
                            returnBool = False
                        else:
                            returnBool = True
                            break
                    return returnBool
                # Check if a string is only numeric.
                def CheckIfStringIsNumeric(_string):
                    returnBool = False
                    for l in _string:
                        if l.isnumeric(): returnBool = False
                        else:
                            returnBool = True
                            break
                    return returnBool






                if firstRun:

                    InputClientName         (requirementClientName  , exampleClientName , defaultClientName , inputClientName)
                    InputDBAddress          (requirementDBAddress   , exampleDBAddress  , defaultDBAddress  , inputDBAddress)
                    InputDBName             (requirementDBName      , exampleDBName     , defaultDBName     , inputDBName)
                    InputDBPort             (requirementDBPort      , exampleDBPort     , defaultDBPort     , inputDBPort)
                    print                   ("\nother components")
                    print                   (requirementWithout)
                    print                   (exampleWithout)
                    print                   (defaultWithout)
                    InputWithoutComponent   (inputDB    , _config.withoutDB     [2], _config.withoutDB      [1])
                    InputWithoutComponent   (inputFaceD , _config.withoutFaceD  [2], _config.withoutFaceD   [1])
                    InputWithoutComponent   (inputIRD   , _config.withoutIRD    [2], _config.withoutIRD     [1])
                    InputWithoutComponent   (inputLog   , _config.withoutLog    [2], _config.withoutLog     [1])
                    InputWithoutComponent   (inputPVD   , _config.withoutPVD    [2], _config.withoutPVD     [1])
                    InputSave               (inputSave)





            # If only `start` then this application
            # will take value directly from the
            # config.ini file. Actually nothing
            # need to be done here, because all
            # values have already assigned in the
            # `AssignConfig()`.
            #else:

                #print("start")

                # No bullshit here, just assign those
                # values :D

                #cfg = cfgp.ConfigParser()
                #cfg.read(_configAbsPath)

                # Actually I need to make a function to convert
                # string into boolean here. `boolean(put_your_string_here)`
                # will actually do validation on the string. So,
                # `bool("True")` or `bool("False")` will return
                # `True`. While, `bool("")` will return false.
                #_config.withoutDB[2]    = self.StringToBool(cfg.get(_config.iniSections[2], _config.withoutDB    [0]))
                #_config.withoutFaceD[2] = self.StringToBool(cfg.get(_config.iniSections[2], _config.withoutFaceD [0]))
                #_config.withoutIRD[2]   = self.StringToBool(cfg.get(_config.iniSections[2], _config.withoutIRD   [0]))
                #_config.withoutLog[2]   = self.StringToBool(cfg.get(_config.iniSections[2], _config.withoutLog   [0]))
                #_config.withoutPVD[2]   = self.StringToBool(cfg.get(_config.iniSections[2], _config.withoutPVD   [0]))

                #self.ShowConfig(_config)

                #print("==========")
                #print(_config.withoutDB[2])
                #print(_config.withoutFaceD[2])
                #print(_config.withoutIRD[2])
                #print(_config.withoutLog[2])
                #print(_config.withoutPVD[2])
                #print("==========")
                #print(cfg.get(_config.iniSections[2], _config.withoutDB    [0]))
                #print(cfg.get(_config.iniSections[2], _config.withoutFaceD [0]))
                #print(cfg.get(_config.iniSections[2], _config.withoutIRD   [0]))
                #print(cfg.get(_config.iniSections[2], _config.withoutLog   [0]))
                #print(cfg.get(_config.iniSections[2], _config.withoutPVD   [0]))
                #print("==========")
                #print(bool(cfg.get(_config.iniSections[2], _config.withoutDB    [0])))
                #print(bool(cfg.get(_config.iniSections[2], _config.withoutFaceD [0])))
                #print(bool(cfg.get(_config.iniSections[2], _config.withoutIRD   [0])))
                #print(bool(cfg.get(_config.iniSections[2], _config.withoutLog   [0])))
                #print(bool(cfg.get(_config.iniSections[2], _config.withoutPVD   [0])))
                #print("==========")

    def StringToBool(self, _string):
        return str(_string).lower() in ("1", "t", "true", "yes")

def main(_docArgs): main = Main(_docArgs)
if __name__ == "__main__":
    docArgs = doc(__doc__, version="0.0.1")
    main(docArgs)