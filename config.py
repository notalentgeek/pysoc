# This is specific Python class that manages
# configuration variables.

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
        self.clientName             = ["client_name"            , "clientTest"          , None]
        self.dbAddress              = ["db_address"             , "127.0.0.1"           , None]
        self.dbName                 = ["db_name"                , "sociometric_server"  , None]
        self.dbPort                 = ["db_port"                , "28015"               , None]
        self.firstRun               = ["first_run"              , "True"                , None]
        self.withoutDB              = ["without_db"             , "False"               , None]
        self.withoutFaceDetection   = ["without_face_detection" , "False"               , None]
        self.withoutIRDetection     = ["without_ir_detection"   , "False"               , None]
        self.withoutLog             = ["without_log"            , "False"               , None]
        self.withoutPVDetection     = ["without_pv_detection"   , "False"               , None]