import threading


class TextCollection(object):


    applicationName = "Sociometric Client"
    closeWindows = "Closing all window(s)."
    quitProgram = "\nQuitting program."
    releaseWebcam = "Releasing webcam."


class TextUpdate(threading.Thread):


    def __init__(
        self,
        _array,
        _counter,
        _name,
        _threadID
    ):


        # "Super".
        threading.Thread.__init__(self)
        self.counter = _counter
        self.name = _name
        self.threadID = _threadID


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
            showTextArray = [
                self.micPVDetection,
                self.webcamFaceDetection
            ]
            for text in showTextArray:
                showText = showText + text + " "
            print(showText)


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