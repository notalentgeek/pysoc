# A Python file for a CLI wizard function.

from    collection_function_check_string                        import CheckIfStringIsAlphaNumeric         as isanum
from    collection_function_check_string                        import CheckIfStringIsAlphaNumericDot      as isanumdot
from    collection_function_check_string                        import CheckIfStringIsAlphaNumericUScore   as isanumuscore
from    collection_function_check_string                        import CheckIfStringIsBlank                as isblank
from    collection_function_check_string                        import CheckIfStringIsNumeric              as isnum
from    collection_function_value_manipulation_and_conversion   import AssignAllConfigRTV                  as assignallconfigrtv
from    collection_function_value_manipulation_and_conversion   import StringToBool                        as stb

def StartWizard(_docArgs, _config, _configAbsPath):

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
    inputOCVGUI             = "do you want to turn off opencv gui for face detection? "
    inputPiCam              = "do you use picam (choosing no means you are using USB web cam)? "
    inputPVD                = "do you want to use pitch and volume detection? "
    inputRPI                = "do you use raspberry pi with raspbian jessie? "
    inputSave               = "do you want to save this setting? "
    requirementClientName   = "requirement              : no space, case sensitive, alpha - numeric, camelCase"
    requirementDBAddress    = "requirement              : no space, not case sensitive, alpha - numeric"
    requirementDBName       = "requirement              : no space, lower case, alpha - numeric, underscore_case"
    requirementDBPort       = "requirement              : no space, numeric"
    requirementWithout      = "requirement              : no space, not case sensitive"

    # Function to input value.
    def InputWizard(_description, _requirement, _example, _defaultValue,
        _input, _confVar, _legalityFunction):

        description = "\n" + _description
        while True:
            print(description)
            print(_requirement)
            print(_example)
            print(_defaultValue)

            description = _description

            inspectThis = input(_input)

            if isblank(inspectThis):
                _confVar[2] = _confVar[1]
                break

            elif _legalityFunction(inspectThis):
                _confVar[2] = inspectThis
                break

            print("\ninput failed\n")
    def InputWizardModClientName(): InputWizard(
        descriptionClientName,
        requirementClientName,
        exampleClientName,
        defaultClientName,
        inputClientName,
        _config.clientName,
        isanum)
    def InputWizardModDBAddress(): InputWizard(
        descriptionDBAddress,
        requirementDBAddress,
        exampleDBAddress,
        defaultDBAddress,
        inputDBAddress,
        _config.dbAddress,
        isanumdot)
    def InputWizardModDBName(): InputWizard(
        descriptionDBName,
        requirementDBName,
        exampleDBName,
        defaultDBName,
        inputDBName,
        _config.dbName,
        isanumuscore)
    def InputWizardModDBPort(): InputWizard(
        descriptionDBPort,
        requirementDBPort,
        exampleDBPort,
        defaultDBPort,
        inputDBPort,
        _config.dbPort,
        isnum)

    def InputBool(_input, _confVar):

        legal = False
        while not legal:

            inspectThis = input(_input)

            if   isblank(inspectThis): _confVar[2] = False
            elif not stb(inspectThis): _confVar[2] = True
            elif     stb(inspectThis): _confVar[2] = False
            else: _confVar[2] = None

            if _confVar[2] != None: legal = True
    def InputBoolReverse(_input, _confVar):

        legal = False
        while not legal:

            inspectThis = input(_input)

            if   isblank(inspectThis): _confVar[2] = True
            elif not stb(inspectThis): _confVar[2] = False
            elif     stb(inspectThis): _confVar[2] = True
            else: _confVar[2] = None

            if _confVar[2] != None: legal = True
    def InputBoolModDB      (): InputBool       (inputDB       , _config.withoutDB     )
    def InputBoolModFaceD   (): InputBool       (inputFaceD    , _config.withoutFaceD  )
    def InputBoolModIRD     (): InputBool       (inputIRD      , _config.withoutIRD    )
    def InputBoolModLog     (): InputBool       (inputLog      , _config.withoutLog    )
    def InputBoolModOCVGUI  (): InputBoolReverse(inputOCVGUI   , _config.withoutOCVGUI )
    def InputBoolModPVD     (): InputBool       (inputPVD      , _config.withoutPVD    )

    def InputSave(_docArgs):

        doYouWantToSave = None
        while doYouWantToSave == None:

            inspectThis = input("\n" + inputSave)

            if   isblank(inspectThis)   : doYouWantToSave = True
            elif not stb(inspectThis)   : doYouWantToSave = False
            elif     stb(inspectThis)   : doYouWantToSave = True
            else                        : doYouWantToSave = None

        if doYouWantToSave: assignallconfigrtv(_docArgs, _config, _configAbsPath)

    def InputRPI():

        usePiCam = None
        useRPI   = None
        while useRPI == None:

            inspectThisRPI = input(inputRPI)

            if   isblank(inspectThisRPI)    : useRPI = True
            elif not stb(inspectThisRPI)    : useRPI = False
            elif     stb(inspectThisRPI)    : useRPI = True
            else                            : useRPI = None

            # If user stated that they will use Raspbery PI
            # ask them again if they are using PiCamera or
            # USB camera.
            if useRPI:

                while usePiCam == None:

                    inspectThisPiCam = input(inputPiCam)

                    if   isblank(inspectThisPiCam)  : usePiCam = True
                    elif not stb(inspectThisPiCam)  : usePiCam = False
                    elif     stb(inspectThisPiCam)  : usePiCam = True
                    else                            : usePiCam = None

            else: usePiCam = False

        return [useRPI, usePiCam]


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
    InputBoolModOCVGUI          ()
    InputBoolModPVD             ()
    InputSave                   (_docArgs)

    inputRPI    = InputRPI()
    useRPI      = inputRPI[0]
    usePiCam    = inputRPI[1]

    # Set `firstRun` variable into `False`.
    return [False, useRPI, usePiCam]