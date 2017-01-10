from   mod_thread          import ModThread         as mt
from   timer_second_change import TimerSecondChange as tsc

class IRDetection(mt):

    def __init__(self, _threadName, _array, _iDB):

        import lirc

        _array.append(self)
        mt.__init__(self,
            _array.index(self) + 1,
            _array.index(self) + 1,
            _threadName)

        self.iDB = _iDB

        self.MODULE_NAME = "ir"

        self.irReceivedDuringInterval = []      # Array for buffering incoming IR within the specified interval (default 1 second).
        self.tSC                      = tsc()   # Timer for interval and database.

        lirc.init("pysoc", blocking=False)

    def run(self):

        while self.killMe == False:

            self.tSC.Update()
            self.Update()
            if self.tSC.changeSecond:

                # Check the if there is at least an element
                # in `self.irReceivedDuringInterval` array.
                if len(self.irReceivedDuringInterval) > 0:
                    self.iDB.mainArray.append(
                        self.SetupStringForDatabase(self.irReceivedDuringInterval))
                    del self.irReceivedDuringInterval[:]

        if self.killMe == True: lirc.deinit()

    # Function to set database string.
    def SetupStringForDatabase(self, _irReceivedDuringInterval):

        theArrayThatWillBeReturned = [self.MODULE_NAME]
        theArrayThatWillBeReturned.extend(self.tSC.dateTime)

        # The `cleanString` will something like,
        # "KEY_1,KEY_2"
        cleanString = str(_irReceivedDuringInterval)\
            .replace(" ", "")\
            .replace("[", "")\
            .replace("]", "")\
            .replace("\'", "")\
            .replace("\"", "")
        theArrayThatWillBeReturned.extend(["ir_code", cleanString])

        return theArrayThatWillBeReturned

    def Update(self):

        # Take as many IR input as possible.
        irReceived = lirc.nextcode()

        for ir in irReceived:
            # If the IR code is not in the received array yet
            # then put there. After a new element appended into
            # the IR received array `sort()` the array alphabetically.
            irS = str(ir).upper()
            if irS != "[]" and not irS in self.irReceivedDuringInterval:
                self.irReceivedDuringInterval.append(irS)
                self.irReceivedDuringInterval.sort()