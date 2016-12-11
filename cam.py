from mod_thread import ModThread as mt
from shared import GetDateTime as gdt
from timer_second_change import TimerSecondChange as tms
import cv2

class CamFaceDetection(mt):

    def __init__(
        self,
        _threadName,
        _array,
        _iDB
    ):

        # Append this object into array.
        _array.append(self)

        mt.__init__(
            self,
            _array.index(self) + 1,
            _array.index(self) + 1,
            _threadName
        )

        # Insert database object.
        self.iDB = _iDB

        # Detection threshold to prevent "noise" face.
        # The value means that a face need to be detected
        # at least two seconds to be considered a face.
        self.FACE_DTCT_THRS = 2
        # Constant for database.
        self.MODULE_NAME = "cam"
        # Path to cascade pattern.
        CASC_PATH = "./cascade-face-front-default.xml"

        # Variables for better face detection.
        self.faceCnt = 0
        # The variable below is True if there
        # is at least one face.
        self.faceDtct = False

        # Assign to which camera this program should
        # listens. 0 means that this program will
        # listen to the default camera (the first
        # camera detected by the operating system
        # when it boots) attached to the computer.
        self.cam = cv2.VideoCapture(0)

        # Path to cascade. Cascade is a pattern to
        # detect something using OpenCV. In this scenario
        # I want to detect front facing face(s).
        self.casc = cv2.CascadeClassifier(CASC_PATH)

        # Frame captured from connected cam.
        self.frame = None

        # Set up timer object. To make sure that
        # the audio calculation only once for
        # every second.
        self.tMS = tms()


    def run(self):

        if self.killMe == True: self.Quit()
        while self.killMe == False:
            self.tMS.Update()
            self.FaceDetectStream()
            if self.tMS.chngSec:
                self.FaceDetect()

    def FaceDetect(self):

        # Convert the captured frame into greyscale.
        frameGrey = cv2.cvtColor(
            self.frame, cv2.COLOR_BGR2GRAY)

        # Face detection.
        faces = self.casc.detectMultiScale(
            frameGrey,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Sometimes there is a faces that is actually not
        # a face. For example, OpenCV can detect cardboard
        # as a face. Below is a simple code to remove those
        # noise face(s).
        if len(faces) <= 0:
            self.faceCnt = self.faceCnt - 1
            if self.faceCnt <= 0:
                self.faceCnt = 0
            self.faceDtct = False
        else: self.faceCnt = self.faceCnt + 1
        if self.faceCnt >= self.FACE_DTCT_THRS:
            self.faceCnt = self.FACE_DTCT_THRS
            self.faceDtct = True
        if self.faceDtct == True:
            self.iDB.mainArray.append(
                self.SetupStringForDB(str(len(faces)))
            )

            #print("faces = " + str(len(faces)))

        # Draw rectangle around the faces.
        #for(x, y, w, h) in faces:
        #    cv2.rectangle(
        #        frame,
        #        (x, y),
        #        (x + w, y + h),
        #        (0, 0, 255),
        #        2
        #    )


        # Display the resulting frame. Comment this line
        # of codes below if the program is going to be
        # headless.
        #cv2.imshow("CamFaceDetection", frame)

    def FaceDetectStream(self):

        # Capture the video frame by frame from the
        # self.cam.
        retVal, self.frame = self.cam.read()

    # Function that need to be executed when the program
    # is closing.
    def Quit(self):

        # When this program is terminated do not forget
        # to free the camera that previously used and destroy
        # all user interface and windows if there is any,
        cv2.destroyAllWindows()
        self.cam.release()

    # Function to format string before put in database.
    def SetupStringForDB(
        self,
        _facesLen
    ):

        arrayForDB = [self.MODULE_NAME]
        arrayForDB.extend(gdt())
        arrayForDB.extend(["faces", _facesLen])

        #print(arrayForDB)

        return arrayForDB