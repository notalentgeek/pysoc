import datetime as dt


class Timer(object):


    def __init__(self):


        # The current second casted
        # to integer from string.
        self.currSecond = int(
            datetime.datetime.now().time().strftime("%S")
        )
        # Variable to detect change in second.
        self.storedSecond = None


    def CheckIfASecondHasPassed(self):


        self.aSecondPassed = True if self.currSecond != self.storedSecond else False
        if(self.aSecondPassed == True):

            self.storedSecond = self.currSecond
            return True

        return False
