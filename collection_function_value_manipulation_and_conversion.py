# This is a Python file to group functions those
# are used to value manipulation and conversion.

import configparser as cfgp

# Function to assign all default values into
# `config.ini`.
def AssignAllConfigDefault(_docArgs, _config, _configAbsPath):

    def SaveValueMod0(_configEntryName, _value): SaveValue(_config, _configAbsPath, _docArgs, 0, _configEntryName, _value)
    def SaveValueMod2(_configEntryName, _value): SaveValue(_config, _configAbsPath, _docArgs, 2, _configEntryName, _value)
    SaveValueMod0(_config.clientName    [0], _config.clientName     [1])
    SaveValueMod0(_config.dbAddress     [0], _config.dbAddress      [1])
    SaveValueMod0(_config.dbName        [0], _config.dbName         [1])
    SaveValueMod0(_config.dbPort        [0], _config.dbPort         [1])
    SaveValueMod2(_config.withoutDB     [0], _config.withoutDB      [1])
    SaveValueMod2(_config.withoutFaceD  [0], _config.withoutFaceD   [1])
    SaveValueMod2(_config.withoutIRD    [0], _config.withoutIRD     [1])
    SaveValueMod2(_config.withoutLog    [0], _config.withoutLog     [1])
    SaveValueMod2(_config.withoutOCVGUI [0], _config.withoutOCVGUI  [1])
    SaveValueMod2(_config.withoutPVD    [0], _config.withoutPVD     [1])

# Function to assign all configuration variables from
# `config.ini` into run time variables.
def AssignAllRTVConfig(_config, _configAbsPath):

    # Read the configuration file.
    cfg = cfgp.ConfigParser()
    cfg.read(_configAbsPath)

    # These are variable value taken from the configuration file.
    _config.clientName      [2] =              cfg.get(_config.iniSections[0], _config.clientName    [0])
    _config.dbAddress       [2] =              cfg.get(_config.iniSections[0], _config.dbAddress     [0])
    _config.dbName          [2] =              cfg.get(_config.iniSections[0], _config.dbName        [0])
    _config.dbPort          [2] =              cfg.get(_config.iniSections[0], _config.dbPort        [0])
    _config.firstRun        [2] =              cfg.get(_config.iniSections[1], _config.firstRun      [0])
    _config.withoutDB       [2] = StringToBool(cfg.get(_config.iniSections[2], _config.withoutDB     [0]))
    _config.withoutFaceD    [2] = StringToBool(cfg.get(_config.iniSections[2], _config.withoutFaceD  [0]))
    _config.withoutIRD      [2] = StringToBool(cfg.get(_config.iniSections[2], _config.withoutIRD    [0]))
    _config.withoutLog      [2] = StringToBool(cfg.get(_config.iniSections[2], _config.withoutLog    [0]))
    _config.withoutOCVGUI   [2] = StringToBool(cfg.get(_config.iniSections[2], _config.withoutOCVGUI [0]))
    _config.withoutPVD      [2] = StringToBool(cfg.get(_config.iniSections[2], _config.withoutPVD    [0]))

# Function to assign all default values into the
# run time variables.
def AssignAllRTVDefault(_config):

    # The index no `2` is the runtime value.
    # While the index no `1` is the default
    # value. The index `0` is the `config.ini`
    # sub - section entry name.
    _config.clientName[2]    = _config.clientName[1]
    _config.dbAddress[2]     = _config.dbAddress[1]
    _config.dbName[2]        = _config.dbName[1]
    _config.dbPort[2]        = _config.dbPort[1]
    _config.withoutDB[2]     = _config.withoutDB[1]
    _config.withoutFaceD[2]  = _config.withoutFaceD[1]
    _config.withoutIRD[2]    = _config.withoutIRD[1]
    _config.withoutLog[2]    = _config.withoutLog[1]
    _config.withoutOCVGUI[2] = _config.withoutOCVGUI[1]
    _config.withoutPVD[2]    = _config.withoutPVD[1]

# Function to get value from `config.ini`.
def GetValueFromConfig(_configAbsPath, _sectionName, _variableName):
    cfg = cfgp.ConfigParser()
    cfg.read(_configAbsPath)
    return cfg.get(_sectionName, _variableName)

# This function is used to write a value into
# the configuration file.
def SaveValue(_config, _configAbsPath, _docArgs,
    _iniSectionsIndex, _variableNameInConfigFile,
    _value):

    # If there is a save parameter then
    # write the setting into configuration
    # .ini file as well.
    #print(_docArgs.get("set"))
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
        with open(_configAbsPath, "w") as cfg: cfgRaw.write(cfg)

# Function to convert string into boolean.
def StringToBool(_string):
    if   str(_string).lower() in ["1", "t", "true", "y", "yes"]: return True
    elif str(_string).lower() in ["0", "f", "false", "n", "no"]: return False
    else                                                       : return None