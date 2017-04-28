# tzlocal is a Python library to get UTC timezone.
from    tzlocal     import  get_localzone
import  datetime    as      dt

# TLDR, object to help executes codes once every
# second.
#
# This is a class to detect one second change.
# My first initial idea was to make codes
# execute for every second. The method here
# is actually quite simple, first I take the
# operating system current time using
# datetime.datetime.time() to extract the current
# second. Then, I check every tick with the same
# datetime.datetime.time() if the second change.
# If the second change then it means that at least
# one second is passed.
#
# You can make this into execute codes every x
# second with modulus (I think).
#
# This object will exist in every threads that
# need its codes to be executed once per second.
# Currently the microphone pitch and volume
# detection and the web cam face detection are using
# this class.
#
# I added/moved GetDateTime() to this class.
class TimerSecondChange(object):

    def __init__(self):

        # Current second is updated at every possible
        # tick.
        self.currentSecond = None
        # If the second change (a second is passed)
        # then update the stored second.
        self.storedSecond = None
        # TLDR, boolean that change into True if a second
        # passed.
        #
        # If the self.currentSecond is the same
        # with the stored second then change this back
        # to False.
        #
        # If the process in desired thread for one
        # tick exceed one second this still apply because
        # the checking will still be in the next tick of
        # this TimerSecondChange class. Hence, the
        # self.changeSecond will return True and
        # self.storedSecond still have different
        # value than self.currentSecond.
        self.changeSecond = False

        # The current date and time. I decided to move it
        # in the timer class to make sure every timer for
        # each Threads is the same.
        self.dateTime = self.GetDateTime()

    # Function to get current date and time in an array.
    # This function returns very useful array to be sent
    # into database. Only the sec part is useful to this class.
    def GetDateTime(self):

        # Set up those strings.
        #
        # Date and time.
        dateTime    = str(dt.datetime.utcnow()).split(".")[0]
        date        = str(dateTime).split(" ")[0]
        time        = str(dateTime).split(" ")[1]
        year        = str(date).split("-")[0]
        month       = str(date).split("-")[1]
        day         = str(date).split("-")[2]
        hour        = str(time).split(":")[0]
        minu        = str(time).split(":")[1]
        sec         = str(time).split(":")[2]

        #print(sec)

        # UTC time zone (without DST). This will return time zone.
        # Hence, all time mentioned here is without local
        # timezone (no DST, summer time, ...).
        utc = str(get_localzone()).lower()

        # Setup array to be returned.
        returnArray = [
            year,
            month,
            day,
            hour,
            minu,
            sec,
            utc
        ]

        return returnArray

    # Update this object every tick possible to detect
    # if one second is passed.
    def Update(self):

        # Always update the current date and time. This variable
        # will be taken into the Thread that is attached by this class
        # for database document entry.
        self.dateTime = GetDateTime()
        # Always check and update the current second.
        self.currentSecond = int(self.dateTime[5])

        #print(self.currentSecond)

        # Compare the previously stored second with the
        # current second.
        self.changeSecond = self.currentSecond != self.storedSecond

        # If a second just passed then change set back the self.storedSecond
        # to be equal with the current second.
        if self.changeSecond:
            self.storedSecond = self.currentSecond

# Function to get current date and time in an array.
# This function returns very useful array to be sent
# into database. Only the sec part is useful to this class.
def GetDateTime():

    # Set up those strings.
    #
    # Date and time.
    dateTime    = str(dt.datetime.utcnow()).split(".")[0]
    date        = str(dateTime).split(" ")[0]
    time        = str(dateTime).split(" ")[1]
    year        = str(date).split("-")[0]
    month       = str(date).split("-")[1]
    day         = str(date).split("-")[2]
    hour        = str(time).split(":")[0]
    minu        = str(time).split(":")[1]
    sec         = str(time).split(":")[2]

    #print(sec)

    # UTC time zone (without DST). This will return time zone.
    # Hence, all time mentioned here is without local
    # timezone (no DST, summer time, ...).
    utc = str(get_localzone()).lower()

    # Setup array to be returned.
    returnArray = [
        year,
        month,
        day,
        hour,
        minu,
        sec,
        utc
    ]

    return returnArray