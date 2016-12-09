from datetime import datetime
from tzlocal import get_localzone
import threading
import rethinkdb as r

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
        _threadName,
        _connection,
        _database
    ):


        # "Super".
        threading.Thread.__init__(self)
        self.clientName = _clientName
        self.counter = _counter
        self.threadID = _threadID
        self.threadName = _threadName


        self.connection = _connection
        self.database = _database


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


        # Check if table is exist.
        try:


            self.database.table(self.clientName + "_mic").run(self.connection)
            self.table = self.database.table(self.clientName + "_mic")


        except r.ReqlOpFailedError as error:


            print("Table for " + self.clientName + " to store microphone data does not exist.")
            print("Creating " + self.clientName + "_mic table.")
            self.database.table_create(self.clientName + "_mic").run(self.connection)
            self.table = self.database.table_create(self.clientName + "_mic")


    def run(self):


        while(self.killMe == False):

            showText = ""
            for text in self.FixString():
                showText = showText + text + " "
            #print(showText)


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


        pitchStr = "p*" + str(_pitch)
        volumeStr = "v*" + str(_volume)
        dtStr = str(datetime.utcnow()).split(".")[0]
        dateStr = str(dtStr).split(" ")[0]
        timeStr = str(dtStr).split(" ")[1]
        yearStr = str(dateStr).split("-")[0]
        monthStr = str(dateStr).split("-")[1]
        dayStr = str(dateStr).split("-")[2]
        hourStr = str(timeStr).split(":")[0]
        minStr = str(timeStr).split(":")[1]
        secStr = str(timeStr).split(":")[2]
        utc = str(get_localzone()).lower()

        volumeEdit = "{:.4f}".format(_volume)

        self.table.insert({


            "year": yearStr,
            "month": monthStr,
            "day": dayStr,
            "hour": hourStr,
            "min": minStr,
            "sec": secStr,
            "timeZone": utc,
            "pitch": str(_pitch),
            "volume": volumeEdit


        }).run(self.connection)


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