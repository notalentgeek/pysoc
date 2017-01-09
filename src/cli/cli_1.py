# A python file for CLI.
import sys
sys.path.append("./src/collection_function")

from    collection_function_check_string                        import  CheckIfStringIsAlphaNumeric         as isanum
from    collection_function_check_string                        import  CheckIfStringIsAlphaNumericDot      as isanumdot
from    collection_function_check_string                        import  CheckIfStringIsAlphaNumericUScore   as isanumuscore
from    collection_function_check_string                        import  CheckIfStringIsBlank                as isblank
from    collection_function_check_string                        import  CheckIfStringIsNumeric              as isnum
from    collection_function_value_manipulation_and_conversion   import  GetValueFromConfig                  as getvaluefromconfig
from    collection_function_value_manipulation_and_conversion   import  SaveValue                           as sv
from    collection_function_value_manipulation_and_conversion   import  StringToBool                        as stb
from    collection_function_value_manipulation_and_conversion   import  AssignAllRTVDefault                 as assignallrtvdefault
from    collection_function_value_manipulation_and_conversion   import  AssignAllConfigDefault              as assignallconfigdefault
import  configparser                                            as      cfgp

# A Python function to set
def StartRPI(_docArgs):

    #print(_docArgs.get("--rpi"))
    #print(_docArgs.get("--picam"))

    useRPI      = _docArgs.get("--rpi")
    usePiCam    = _docArgs.get("--picam")

    return [useRPI, usePiCam]

# A Python function for `main.py start all-default`
def StartAllDefault(_docArgs, _config, _configAbsPath):

    assignallrtvdefault(_config)
    if _docArgs.get("--save"): assignallconfigdefault(_docArgs, _config, _configAbsPath)

    # Check if user wants to start this application in Raspberry PI's
    # Raspbian Jessie.
    return StartRPI(_docArgs)

# Docopt function to handle CLI command
# of `start without`.
def StartWithout(_docArgs, _config, _configAbsPath):

    def SaveValueMod2(_configEntryName, _value): sv(_config, _configAbsPath, _docArgs, 2, _configEntryName, _value)

    if _docArgs.get("--cvgui"):
        _config.withoutOCVGUI[2] = True
        SaveValueMod2(_config.withoutOCVGUI[0], True)
    if _docArgs.get("--db"):
        _config.withoutDB[2] = True
        SaveValueMod2(_config.withoutDB[0], True)
    if _docArgs.get("--faced"):
        _config.withoutFaceD[2] = True
        SaveValueMod2(_config.withoutFaceD[0], True)
    if _docArgs.get("--ird"):
        _config.withoutIRD[2] = True
        SaveValueMod2(_config.withoutIRD[0], True)
    if _docArgs.get("--log"):
        _config.withoutLog[2] = True
        SaveValueMod2(_config.withoutLog[0], True)
    if _docArgs.get("--pvd"):
        _config.withoutPVD[2] = True
        SaveValueMod2(_config.withoutPVD[0], True)

    # Check if user wants to start this application in Raspberry PI's
    # Raspbian Jessie.
    return StartRPI(_docArgs)

# A Python function for `main.py set` CLI interface.
def Set(_docArgs, _config, _configAbsPath):

    def SaveValueMod0(_configEntryName, _value): sv(_config, _configAbsPath, _docArgs, 0, _configEntryName, _value)
    def SaveValueMod2(_configEntryName, _value): sv(_config, _configAbsPath, _docArgs, 2, _configEntryName, _value)

    inputFailed = False

    if _docArgs.get("--cname"):
        value = _docArgs.get("--cname")[0]
        if isanum(value): SaveValueMod0(_config.clientName[0], value)
        else: inputFailed = True
        #print("--cname")
    if _docArgs.get("--dba"):
        value = _docArgs.get("--dba")[0]
        if isanumdot(value): SaveValueMod0(_config.dbAddress[0], value)
        else: inputFailed = True
        #print("--dba")
    if _docArgs.get("--dbn"):
        value = _docArgs.get("--dbn")[0]
        if isanumuscore(value): SaveValueMod0(_config.dbName[0], str(value).lower())
        else: inputFailed = True
        #print("--dbn")
    if _docArgs.get("--dbp"):
        value = _docArgs.get("--dbp")[0]
        if isnum(value): SaveValueMod0(_config.dbPort[0], value)
        else: inputFailed = True
        #print("--dbp")
    if _docArgs.get("--irc"):
        value = _docArgs.get("--irc")[0]
        if isnum(value): SaveValueMod0(_config.irCode[0], str(value).upper())
        else: inputFailed = True
        #print("--irc")

    if _docArgs.get("--cvgui"):
        currentValueInConfigFile = stb(getvaluefromconfig(_configAbsPath, _config.iniSections[2], _config.withoutOCVGUI[0]))
        changedValue = not currentValueInConfigFile
        SaveValueMod2(_config.withoutOCVGUI[0], changedValue)
        #print(currentValueInConfigFile)
        #print(changedValue)
        #print("--cvgui")
    if _docArgs.get("--db"):
        # I need to get the value first.
        currentValueInConfigFile = stb(getvaluefromconfig(_configAbsPath, _config.iniSections[2], _config.withoutDB[0]))
        # After I get the boolean value then I need
        # to invert the value.
        changedValue = not currentValueInConfigFile
        # After I invert the value I need to write the value
        # back into `config.ini` file.
        SaveValueMod2(_config.withoutDB[0], changedValue)
        #print(currentValueInConfigFile)
        #print(changedValue)
        #print("--db")
    if _docArgs.get("--faced"):
        currentValueInConfigFile = stb(getvaluefromconfig(_configAbsPath, _config.iniSections[2], _config.withoutFaceD[0]))
        changedValue = not currentValueInConfigFile
        SaveValueMod2(_config.withoutFaceD[0], changedValue)
        #print(currentValueInConfigFile)
        #print(changedValue)
        #print("--faced")
    if _docArgs.get("--ird"):
        currentValueInConfigFile = stb(getvaluefromconfig(_configAbsPath, _config.iniSections[2], _config.withoutIRD[0]))
        changedValue = not currentValueInConfigFile
        SaveValueMod2(_config.withoutIRD[0], changedValue)
        #print(currentValueInConfigFile)
        #print(changedValue)
        #print("--ird")
    if _docArgs.get("--log"):
        currentValueInConfigFile = stb(getvaluefromconfig(_configAbsPath, _config.iniSections[2], _config.withoutLog[0]))
        changedValue = not currentValueInConfigFile
        SaveValueMod2(_config.withoutLog[0], changedValue)
        #print(currentValueInConfigFile)
        #print(changedValue)
        #print("--log")
    if _docArgs.get("--pvd"):
        currentValueInConfigFile = stb(getvaluefromconfig(_configAbsPath, _config.iniSections[2], _config.withoutPVD[0]))
        changedValue = not currentValueInConfigFile
        SaveValueMod2(_config.withoutPVD[0], changedValue)
        #print(currentValueInConfigFile)
        #print(changedValue)
        #print("--pvd")

    if inputFailed: print("\ninput failed\n")