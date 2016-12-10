from tzlocal import get_localzone
import datetime as dt

def GetDateTime():

    # Set up the strings.
    dt      = str(dt.utcnow()).split(".")[0] # Date and time.
    date    = str(dtStr).split(" ")[0]
    time    = str(dtStr).split(" ")[1]
    year    = str(dateStr).split("-")[0]
    month   = str(dateStr).split("-")[1]
    day     = str(dateStr).split("-")[2]
    hour    = str(timeStr).split(":")[0]
    minu    = str(timeStr).split(":")[1]
    sec     = str(timeStr).split(":")[2]
    utc     = str(get_localzone()).lower() # UTC time zone (without DST).

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