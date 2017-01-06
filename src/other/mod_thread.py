# This is a super class for Python's threading.Thread.
# With additional variables for counter, thread ID,
# thread name, and a termination flag.
from threading import Thread

class ModThread(Thread):

    def __init__(self, _counter,
        _threadID, _threadName):

        Thread.__init__(self)

        # I do not know what are these variable
        # mean. But every Python Threading tutorial always
        # have these variables. So, here are them :D :D :D.
        self.counter = _counter
        self.threadID = _threadID
        self.threadName = _threadName

        # Termination flag.
        self.killMe = False