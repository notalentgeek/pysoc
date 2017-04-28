from mod_thread import ModThread as mt
import subprocess as subp

class IRSend(mt):

    def __init__(self, _threadName, _array, _config):

        _array.append(self)
        mt.__init__(self,
            _array.index(self) + 1,
            _array.index(self) + 1,
            _threadName)

        self.config = _config

        self.TICK_INTERVAL  = 1000
        self.tickCounter    = 0

    def run(self):

        while self.killMe == False:

            # Do not transmit IR code so fast.
            # Do it per once per self.TICK_INTERVAL
            # ticks.
            self.tickCounter = self.tickCounter + 1

            if self.tickCounter >= self.TICK_INTERVAL:
                subp.call(["irsend SEND_ONCE pysoc " + self.config.irCode[2]], shell=True)
                self.tickCounter = 0