from datetime import datetime
from tzlocal import get_localzone
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
        _threadName,
        _connection,
        _mainTable
    ):


        # "Super".
        threading.Thread.__init__(self)
        self.clientName = _clientName
        self.counter = _counter
        self.threadID = _threadID
        self.threadName = _threadName


        self.connection = _connection
        self.mainTable = _mainTable


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
        timeFrmt = (
            yearStr + "*" +
            monthStr + "*" +
            dayStr + "*" +
            hourStr + "*" +
            minStr + "*" +
            secStr + "*" +
            utc
        )
        databaseStr = pitchStr + "_" + volumeStr + "_" + timeFrmt
        #print(databaseStr)


        # Before sending the string into database
        # I need to find out if there is a field
        # for microphone for this client. If there
        # is not then make one. But first I need
        # access to the table then to the document
        # of this specific client.
        clientDoc = self.mainTable.get_all(self.clientName, index="clientName")
        # Check if the document has a "mic" column/field.
        # If the list length is 0 then there is no "mic"
        # column/field yet. Hence, we need to create one.
        hasMicField = True if (len(list(clientDoc.has_fields("mic").run(self.connection))) > 0) else False
        # If hasMicField returns False then create the field.
        # And insert the initial value.
        print(databaseStr)
        clientDoc.update({"mic": databaseStr}).run(self.connection)


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