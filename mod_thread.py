from threading import Thread

class ModThread(Thread):

    def __init__(
        self,
        _counter,
        _threadID,
        _threadName
    ):

        Thread.__init__(self)

        self.counter = _counter
        self.threadID = _threadID
        self.threadName = _threadName

        self.killMe = False