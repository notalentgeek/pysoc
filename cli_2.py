# A Python file for a CLI wizard function.

from    collection_function_check_string                        import CheckIfStringIsAlphaNumeric         as isanum
from    collection_function_check_string                        import CheckIfStringIsAlphaNumericDot      as isanumdot
from    collection_function_check_string                        import CheckIfStringIsAlphaNumericUScore   as isanumuscore
from    collection_function_check_string                        import CheckIfStringIsBlank                as isblank
from    collection_function_check_string                        import CheckIfStringIsNumeric              as isnum
from    collection_function_value_manipulation_and_conversion   import StringToBool                        as stb
from    collection_function_value_manipulation_and_conversion   import AssignAllRTVConfig                  as assignallrtvconfig

def StartWizard(_config, _configAbsPath):

    # A ton of fancy strings.
    defaultClientName       = "default                  : do not fill and just press enter to fill the default value of \"clientTest\""
    defaultDBAddress        = "default                  : do not fill and just press enter to fill the default value of \"127.0.0.1\""
    defaultDBName           = "default                  : do not fill and just press enter to fill the default value of \"sociometric_server\""
    defaultDBPort           = "default                  : do not fill and just press enter to fill the default value of \"28015\""
    defaultWithout          = "default                  : do not fill and just press enter to automatically response \"yes\""
    descriptionClientName   = "please input client name"
    descriptionDBAddress    = "please input rethinkdb database address"
    descriptionDBName       = "please input rethinkdb database name"
    descriptionDBPort       = "please input rethinkdb database port"
    descriptionWithout      = "please specify components you want to use"
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

    # Function to input value.
    def InputWizard(_description, _requirement, _example, _defaultValue,
        _input, _configVariable , _configDefaultValue, _legalityFunction):

        legal = False
        description = "\n" + _description
        while not legal:
            print(description)
            print(_requirement)
            print(_example)
            print(_defaultValue)

            description = _description

            _configVariable = input(_input)
            if isblank(_configVariable):
                _configVariable = _configDefaultValue
                legal = True
                break
            legal = _legalityFunction(_configVariable)
            if not legal: print("\ninput failed\n")
    def InputWizardModClientName(): InputWizard(
        descriptionClientName,
        requirementClientName,
        exampleClientName,
        defaultClientName,
        inputClientName,
        _config.clientName[2],
        _config.clientName[1],
        isanum)
    def InputWizardModDBAddress(): InputWizard(
        descriptionDBAddress,
        requirementDBAddress,
        exampleDBAddress,
        defaultDBAddress,
        inputDBAddress,
        _config.dbAddress[2],
        _config.dbAddress[1],
        isanumdot)
    def InputWizardModDBName(): InputWizard(
        descriptionDBName,
        requirementDBName,
        exampleDBName,
        defaultDBName,
        inputDBName,
        _config.dbName[2],
        _config.dbName[1],
        isanumuscore)
    def InputWizardModDBPort(): InputWizard(
        descriptionDBPort,
        requirementDBPort,
        exampleDBPort,
        defaultDBPort,
        inputDBPort,
        _config.dbPort[2],
        _config.dbPort[1],
        isnum)

    def InputBool(_input, _configVariable, _configDefault):

        legal = False
        while not legal:

            inspectThis = input(_input)

            if   isblank(inspectThis): _configVariable = _configDefault
            elif not stb(inspectThis): _configVariable = False
            elif     stb(inspectThis): _configVariable = True
            else: _configVariable = None

            if _configVariable != None: legal = True
    def InputBoolModDB      (): InputBool(inputDB    , _config.withoutDB     [2], _config.withoutDB      [1])
    def InputBoolModFaceD   (): InputBool(inputFaceD , _config.withoutFaceD  [2], _config.withoutFaceD   [1])
    def InputBoolModIRD     (): InputBool(inputIRD   , _config.withoutIRD    [2], _config.withoutIRD     [1])
    def InputBoolModLog     (): InputBool(inputLog   , _config.withoutLog    [2], _config.withoutLog     [1])
    def InputBoolModPVD     (): InputBool(inputPVD   , _config.withoutPVD    [2], _config.withoutPVD     [1])

    def InputSave():

        doYouWantToSave = None
        while doYouWantToSave == None:

            inspectThis = input("\n" + inputSave)

            if   isblank(inspectThis)   : doYouWantToSave = True
            elif not stb(inspectThis)   : doYouWantToSave = False
            elif     stb(inspectThis)   : doYouWantToSave = True
            else                        : doYouWantToSave = None

        if doYouWantToSave: assignallrtvconfig(_config, _configAbsPath)

    # Run the wizard.
    InputWizardModClientName    ()
    InputWizardModDBAddress     ()
    InputWizardModDBName        ()
    InputWizardModDBPort        ()
    print                       ("\n" + descriptionWithout)
    print                       (requirementWithout)
    print                       (exampleWithout)
    print                       (defaultWithout)
    InputBoolModDB              ()
    InputBoolModFaceD           ()
    InputBoolModIRD             ()
    InputBoolModLog             ()
    InputBoolModPVD             ()
    InputSave                   ()