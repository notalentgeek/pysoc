# This is specific Python class that manages
# configuration variables.

from    collection_function_value_manipulation_and_conversion import GetValueFromConfig as gvfc

import  configparser as cfgp
import  io

class Config(object):

    def __init__(self):

        # Main section for the .ini
        # configuration file.
        self.iniSections = ["database", "flag", "setting"]

        # The first index is the entry name
        # (sub - section) in the .ini
        # configuration files. The second
        # index is the default value. The
        # third index is the value that can
        # be changed and modified.
        self.clientName     = ["client_name"                    , "clientTest"          , None]
        self.dbAddress      = ["db_address"                     , "127.0.0.1"           , None]
        self.dbName         = ["db_name"                        , "sociometric_server"  , None]
        self.dbPort         = ["db_port"                        , "28015"               , None]
        self.firstRun       = ["first_run"                      , "True"                , None]
        self.withoutDB      = ["without_db"                     , "False"               , None]
        self.withoutFaceD   = ["without_face_detection"         , "False"               , None]
        self.withoutIRD     = ["without_ir_detection"           , "False"               , None]
        self.withoutLog     = ["without_log"                    , "False"               , None]
        self.withoutPVD     = ["without_pitch_volume_detection" , "False"               , None]

# Function to create `config.ini` at this program root directory.
def CreateConfig(_config, _configAbsPath):

    # Create configuration file using FileIO.
    io.FileIO(_configAbsPath, "w")
    cfg     = open(_configAbsPath, "w")
    cfgRaw  = cfgp.ConfigParser()

    cfgRaw.add_section(_config.iniSections[0]) # Database.
    cfgRaw.add_section(_config.iniSections[1]) # Flag.
    cfgRaw.add_section(_config.iniSections[2]) # Setting.

    # Create the configuration value and then add its default value.
    cfgRaw.set(_config.iniSections[0], _config.clientName   [0], _config.clientName     [1])
    cfgRaw.set(_config.iniSections[0], _config.dbAddress    [0], _config.dbAddress      [1])
    cfgRaw.set(_config.iniSections[0], _config.dbName       [0], _config.dbName         [1])
    cfgRaw.set(_config.iniSections[0], _config.dbPort       [0], _config.dbPort         [1])

    cfgRaw.set(_config.iniSections[1], _config.firstRun     [0], _config.firstRun       [1])

    cfgRaw.set(_config.iniSections[2], _config.withoutFaceD [0], _config.withoutFaceD   [1])
    cfgRaw.set(_config.iniSections[2], _config.withoutDB    [0], _config.withoutDB      [1])
    cfgRaw.set(_config.iniSections[2], _config.withoutIRD   [0], _config.withoutIRD     [1])
    cfgRaw.set(_config.iniSections[2], _config.withoutLog   [0], _config.withoutLog     [1])
    cfgRaw.set(_config.iniSections[2], _config.withoutPVD   [0], _config.withoutPVD     [1])

    cfgRaw.write(cfg)
    cfg.close()

# Function to simply print real - time configuration values.
def ShowConfigFile(_config, _configAbsPath):

    def GetValueFromConfigMod(_sectionName, _variableName): return gvfc(_configAbsPath, _sectionName, _variableName)

    print("values from `config.ini`.")
    print("client name                              : " + str(GetValueFromConfigMod(_config.iniSections[0], _config.clientName      [0])))
    print("database address                         : " + str(GetValueFromConfigMod(_config.iniSections[0], _config.dbAddress       [0])))
    print("database name                            : " + str(GetValueFromConfigMod(_config.iniSections[0], _config.dbName          [0])))
    print("database port                            : " + str(GetValueFromConfigMod(_config.iniSections[0], _config.dbPort          [0])))
    print("first time run                           : " + str(GetValueFromConfigMod(_config.iniSections[1], _config.firstRun        [0])))
    print("start without face detection             : " + str(GetValueFromConfigMod(_config.iniSections[2], _config.withoutFaceD    [0])))
    print("start without database                   : " + str(GetValueFromConfigMod(_config.iniSections[2], _config.withoutDB       [0])))
    print("start without ir detection               : " + str(GetValueFromConfigMod(_config.iniSections[2], _config.withoutIRD      [0])))
    print("start without log                        : " + str(GetValueFromConfigMod(_config.iniSections[2], _config.withoutLog      [0])))
    print("start without pitch and volume detection : " + str(GetValueFromConfigMod(_config.iniSections[2], _config.withoutPVD      [0])))

# Function to simply print real - time configuration values.
def ShowConfigRuntime(_config):

    print("values from run - time")
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