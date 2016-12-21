# This file is a collection of shared functions and variables
# those are used a lot within classes and thread. However,
# (CMIIW) due to potential of threads modifying same variable
# in the same time, all variables those are in here are all
# read only.one.
#
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
clientName = "client1"