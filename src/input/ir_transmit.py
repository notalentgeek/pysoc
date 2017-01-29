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
        subp.call(["irsend SEND_START pysoc " + self.config.irCode[2]], shell=True)