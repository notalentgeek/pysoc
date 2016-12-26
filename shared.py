# This file is a collection of shared functions and variables
# those are used a lot within classes and thread. However,
# (CMIIW) due to potential of threads modifying same variable
# in the same time, all variables those are in here are all
# read only.one.

class Config(object):

    def __init__(self):

        # TLDR, please make client name using camel case letter
        # because "_" is used for string splitting while "-" is
        # not allowed to be used as name in database and table.
        #
        # I put the client name here so that every other files
        # that import this file has access to clientName variable.
        # Make sure the client name is using camel case. Because
        # there is a split string operation that is based on "_"
        # and "-" is not allowed for table and database name.
        #
        # Perhaps I could as well put here the database connection
        # setting variable.
        #
        # Configuration variables. Here I want to
        # make variables that can be altered. Before
        # and during this program running. There are
        # 4 variables those are in the configuration
        # files. Those are these.
        # cfgClientName.
        # cfgDBAddress.
        # cfgDBName.
        # cfgDBPort.
        # Some default constants.
        # If there is no client name provided in
        # arguments nor configuration file.
        self.DEFAULT_CLIENT_NAME = "clientTest"
        # Some constants for database connection.
        # I think I can put this into separate configuration file.
        self.DEFAULT_DB_ADDRESS = "198.211.123.92"
        self.DEFAULT_DB_NAME = "sociometric_server"
        self.DEFAULT_DB_PORT = 28015

        #print(type(DEFAULT_DB_PORT))

        # The variable that is used in the configuration files.
        self.cfgClientName = None
        self.cfgDBAddress = None
        self.cfgDBName = None
        self.cfgDBPort = None