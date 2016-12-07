import threading


class TextCollection(object):


    applicationName = "Sociometric Client"
    closeWindows = "Closing all window(s)."
    quitProgram = "\nQuitting program."
    releaseWebcam = "Releasing webcam."
    dbConnRefused = "Database connection refused.\nPlease check database configuration"
    clientWithSameName = "There is a client with same name in the database."


class TextUpdate(threading.Thread):


    def __init__(
        self,
        _array,
        _clientName,
        _counter,
        _threadID,
        _threadName
    ):


        # "Super".
        threading.Thread.__init__(self)
        self.clientName = _clientName
        self.counter = _counter
        self.threadID = _threadID
        self.threadName = _threadName


        # Append this into array.
        _array.append(self)


        # A trigger to kill this thread.
        self.killMe = False


        # Initiates variables to be shown in terminal.
        self.micPVDetection = ""
        self.webcamFaceDetection = ""
        # These are the default value.
        self.faceAmountDefault = "face(s) amount = {:2d}"
        self.faceDetectedDefault = "face(s) detected = {:>5s}"
        self.pitchTextDefault = "pitch = {:>10.4f}"
        self.volumeTextDefault = "volume = {:>1.4f}"


    def run(self):


        while(self.killMe == False):

            showText = ""
            for text in self.FixString():
                showText = showText + text + " "
            print(showText)


    def FixString(self):


            # Fixing string.
            # Client name.
            clientNameMod = "client name = " + self.clientName + ", "
            # Values from microphone.
            micPVDetectionMod = self.micPVDetection + ", "
            # Values from web camera.
            if(
                (self.webcamFaceDetection == "") or
                (self.webcamFaceDetection == None)
            ):
                webcamFaceDetection = self.webcamFaceDetection
            else:
                webcamFaceDetection = self.webcamFaceDetection + ", "


            # Put everything into an array of string.
            showTextArray = [
                clientNameMod,
                micPVDetectionMod,
                webcamFaceDetection
            ]
            return showTextArray


    def UpdateMicPVDetection(self, _pitch, _volume):


        self.pitchText = self.pitchTextDefault.format(_pitch)
        self.volumeText = self.volumeTextDefault.format(_volume)
        self.micPVDetection = (
            self.pitchText + " " + self.volumeText
        )


    def UpdateWebcamFaceDetection(self, _faceAmount, _faceDetected):


        self.faceAmount = self.faceAmountDefault.format(_faceAmount)
        self.faceDetected = self.faceDetectedDefault.format(str(_faceDetected))
        self.webcamFaceDetection = (
            self.faceDetected + " " + self.faceAmount
        )


textCollection = TextCollection()