from   mod_thread          import ModThread         as mt
from   timer_second_change import TimerSecondChange as tsc
import lirc

class IRDetection(mt):

    def __init__(self, _threadName, _array, _iDB):

        _array.append(self)
        mt.__init__(self,
            _array.index(self) + 1,
            _array.index(self) + 1,
            _threadName)

        self.iDB = _iDB

        self.MODULE_NAME = "ir"

        self.irReceivedDuringInterval = []      # Array for buffering incoming IR within the specified interval (default 1 second).
        self.tSC                      = tsc()   # Timer for interval and database.

        lirc.init("pysoc")

    def run(self):

        while self.killMe == False:

            self.tSC.Update()
            self.Stream()
            if self.tSC.changeSecond:
                self.iDB.mainArray.append(
                    self.SetupStringForDatabase(
                        self.irReceivedDuringInterval))
                # After those IR recorded inputted into database,
                # clean the received IR array.
                self.irReceivedDuringInterval = []

    # Function to set database string.
    def SetupStringForDatabase(self, _irReceivedDuringInterval):

        theArrayThatWillBeReturned = [self.MODULE_NAME]
        theArrayThatWillBeReturned.extend(self.tSC.dateTime)
        theArrayThatWillBeReturned.extend(["ir_code", _irReceivedDuringInterval])

        return theArrayThatWillBeReturned

    def Update(self):

        # Take as many IR input as possible.
        irReceived = str(lirc.nextcode()).upper()

        # If the IR code is not in the received array yet
        # then put there. After a new element appended into
        # the IR received array `sort()` the array alphabetically.
        if not irReceived in irReceivedDuringInterval:
            irReceivedDuringInterval.append(irReceived)
            irReceivedDuringInterval.sort()