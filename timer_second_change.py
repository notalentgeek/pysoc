import datetime as dt

# This is a class to detect change in second.
# My first initial idea was to make a codes
# those execute for every second passed.
# The method here is to take the current time
# from datetime.datetime.now().time(), extract
# the second and then execute something when
# the value changes (most of the time codes
# will be executed for every one second).
class TimerSecondChange(object):

    def __init__(self):

        self.currSec = 0        # Current second.
        self.storSec = None     # Previously stored second.
        self.chngSec = False    # If there is change in second.

    def Update(self):

        # Always check current second.
        self.currSec = int(dt.datetime.now().time().strftime("%S"))
        # Compare the current second with
        # previously stored second.
        self.chngSec = True if self.currSec != self.storSec else False
        if self.chngSec: self.storSec = self.currSec