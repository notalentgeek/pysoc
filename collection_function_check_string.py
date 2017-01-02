# This Python file is a collection of functions
# for checking string.

import configparser as cfgp

# Function to check if a string is blank
# string or not.
def CheckIfStringIsBlank(_string): return not (str(_string) and str(_string).strip())

# Function to check if a string is only
# alpha numeric or not.
def CheckIfStringIsAlphaNumeric(_string):
    returnBool = True
    for l in _string:
        if l.isalnum(): returnBool = True
        else:
            returnBool = False
            break
    return returnBool

# Function to check if a string is only
# alpha numeric and dot "." or not.
def CheckIfStringIsAlphaNumericDot(_string):
    returnBool = True
    for l in _string:
        if l == "." or l.isalnum(): returnBool = True
        else:
            returnBool = False
            break
    return returnBool

# Function to check if a string is only
# alpha numeric and under score "_" or not.
def CheckIfStringIsAlphaNumericUScore(_string):
    returnBool = True
    for l in _string:
        if l == "_" or l.isalnum(): returnBool = True
        else:
            returnBool = False
            break
    return returnBool

# Check if a string is only numeric.
def CheckIfStringIsNumeric(_string):
    returnBool = True
    for l in _string:
        if l.isnumeric(): returnBool = True
        else:
            returnBool = False
            break
    return returnBool