# This file is a collection of shared functions
# and variables. Those are used a lot within
# classes and threads.
from tzlocal import get_localzone
import datetime as dt

# Put the client name here so that every other files
# that import this file has access to this variable.
clientName = "client-1"

def GetDateTime():

    # Set up the strings.
    dateTime    = str(dt.datetime.utcnow()).split(".")[0] # Date and time.
    date        = str(dateTime).split(" ")[0]
    time        = str(dateTime).split(" ")[1]
    year        = str(date).split("-")[0]
    month       = str(date).split("-")[1]
    day         = str(date).split("-")[2]
    hour        = str(time).split(":")[0]
    minu        = str(time).split(":")[1]
    sec         = str(time).split(":")[2]
    utc         = str(get_localzone()).lower() # UTC time zone (without DST).

    # Setup array for return.
    arrayForDB = [
        year,
        month,
        day,
        hour,
        minu,
        sec,
        utc
    ]

    return arrayForDB