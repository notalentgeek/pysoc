from datetime import datetime
from text_collection import textCollection
from tzlocal import get_localzone
import cv2
import rethinkdb as r
import text_collection
import threading


class WebcamFaceDetection(threading.Thread):


    def __init__(
        self,
        _array,
        _counter,
        _textUpdate,
        _threadID,
        _threadName
    ):


        # "Super".
        threading.Thread.__init__(self)
        self.counter = _counter
        self.textUpdate = _textUpdate
        self.threadID = _threadID
        self.threadName = _threadName


        # Append this into array.
        _array.append(self)


        # A trigger to kill this thread.
        self.killMe = False


        # Whether or not a face is detected.
        self.faceCounter = 0
        self.faceDetected = False
        self.faceDetectedThreshold = 10
        # Assign to which camera this program should listen
        # 0 means the default camera attached in the
        # computer.
        self.webcam = cv2.VideoCapture(0)


    def run(self):
        if(self.killMe == True):
            self.Quit()
        while(self.killMe == False):
            self.FaceDetect()


    def FaceDetect(self):


        # Capture from web cam frame by frame.
        vidCapRetVal, vidCapFrame = self.webcam.read()


        # Convert the captured frame into grayscale.
        vidCapGray = cv2.cvtColor(
            vidCapFrame,
            cv2.COLOR_BGR2GRAY
        )

        # Path to the cascade.
        # Cascade is a pattern to detect something.
        # In this case I want to detect faces.
        cascadeFrontFaceDefaultPath = (
            "./cascade-face-front-default.xml"
        )
        cascadeFaceFrontDefault = cv2.CascadeClassifier(
            cascadeFrontFaceDefaultPath
        )
        # Detect faces.
        faces = cascadeFaceFrontDefault.detectMultiScale(
            vidCapGray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30, 30),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )


        # Sometimes there are faces that is not a human face.
        # This is what I called the noise faces.
        # Below are the codes to remove those noise faces.
        if len(faces) == 0:
            self.faceCounter -= 1
            self.faceDetected = False
        elif len(faces) > 0:
            self.faceCounter += 1
        if self.faceCounter > self.faceDetectedThreshold:
            self.faceCounter = self.faceDetectedThreshold
            self.faceDetected = True
        if self.faceCounter < 0:
            self.faceCounter = 0


        # Print if there is a face detected or into terminal.
        self.textUpdate.UpdateWebcamFaceDetection(
            len(faces),
            self.faceDetected
        )


        # Draw rectangle around the faces.
        #for(x, y, w, h) in faces:
        #    cv2.rectangle(
        #        vidCapFrame,
        #        (x, y),
        #        (x + w, y + h),
        #        (0, 0, 255),
        #        2
        #    )


        # Display the resulting frame. Comment this line
        # of codes below if the program is going to be
        # headless.
        #cv2.imshow(textCollection.applicationName, frame)


    # Function that need to be executed when the program
    # close.
    def Quit(self):


        # When this program is terminated do not forget to
        # free the camera that was previously used and
        # destroy all user interface window if there is
        # any.
        print(textCollection.closeWindows)
        cv2.destroyAllWindows()
        print(textCollection.releaseWebcam)
        self.webcam.release()