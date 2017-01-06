from        mod_thread          import ModThread            as mt
from        timer_second_change import TimerSecondChange    as tsc
import      cv2

class CamFaceDetect(mt):

    def __init__(
        self,
        _threadName,
        _array,
        _iDB,
        _usePiCamera,
        _config
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
        self.iDB            = _iDB
        # Flag if the user run this in Raspberry PI
        # Raspbian Jessie.
        self.usePiCamera    = _usePiCamera
        # Configuration object.
        self.config         = _config

        # If the user chooses to run this application in
        # Raspberry PI's Raspbian Jessie with PiCamera.
        # Then initiate PiCamera object instead of normal
        # webcam object.
        self.cam = None
        if self.usePiCamera:

            from picamera       import PiCamera
            from picamera.array import PiRGBArray

            # Assign PiCamera variable.
            self.cam                = PiCamera()
            self.cam.framerate      = 32
            self.cam.resolution     = (640, 480)
            self.rawCapture         = PiRGBArray(self.cam)

        # If not using PiCam it means that this application
        # will look into normal USB webcam.
        else:

            # Assign to which web camera this program should
            # listens. 0 means that this program will
            # listen to the default web camera (the first
            # web camera detected by the operating system
            # when it boots) attached to the computer.
            self.cam = cv2.VideoCapture(0)

        # Detection threshold to prevent "noise" face.
        # The value means that a face need to be detected
        # at least two seconds to be considered a face.
        self.FACE_DTCT_THRS = 2
        # Constant for database.
        self.MODULE_NAME = "cam"
        # Path to cascade pattern.
        CASC_PATH = "./cascade_face_front_default.xml"

        # Variables for better face detection.
        self.faceCnt = 0
        # The variable below is True if there
        # is at least one face.
        self.faceDtct = False



        # Path to cascade. Cascade is a pattern to
        # detect something using OpenCV. In this scenario
        # I want to detect front facing face(s).
        self.casc = cv2.CascadeClassifier(CASC_PATH)

        # All the properties of the face(s) detected.
        self.faces = []
        # Frame captured from connected cam.
        self.frame = None

        # Set up timer object. To make sure that
        # the audio calculation only once for
        # every second.
        self.tSC = tsc()


    def run(self):

        #print("Test.")

        if self.killMe == True:
            self.Quit()

        while self.killMe == False:

            #print("Test.")

            self.tSC.Update()
            self.FaceDetectStream()
            if self.tSC.changeSecond:
                self.FaceDetect()

    def FaceDetect(self):

        # Convert the captured frame into greyscale.
        frameGrey = cv2.cvtColor(
            self.frame, cv2.COLOR_BGR2GRAY)

        # Face detection.
        self.faces = self.casc.detectMultiScale(
            frameGrey,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        #print(self.faces)
        #print(len(self.faces))

        # Sometimes there is a faces that is actually not
        # a face. For example, OpenCV can detect cardboard
        # as a face. Below is a simple code to remove those
        # noise face(s).
        if len(self.faces) <= 0:
            self.faceCnt = self.faceCnt - 1
            if self.faceCnt <= 0:
                self.faceCnt = 0
            self.faceDtct = False
        else: self.faceCnt = self.faceCnt + 1
        if self.faceCnt >= self.FACE_DTCT_THRS:
            self.faceCnt = self.FACE_DTCT_THRS
            self.faceDtct = True
        if self.faceDtct == True:
            if self.iDB != None:
                self.iDB.mainArray.append(self.SetupStringForDB(str(len(self.faces))))
                #print("self.faces = " + str(len(self.faces)))

        # Draw rectangle around the faces.
        #for(x, y, w, h) in self.faces:
        #    cv2.rectangle(
        #        self.frame,
        #        (x, y),
        #        (x + w, y + h),
        #        (0, 0, 255),
        #        2
        #    )


        # Display the resulting frame. Comment this line
        # of codes below if the program is going to be
        # headless.
        #cv2.imshow("CamFaceDetection", self.frame)

    def FaceDetectStream(self):

        # If using ribbon PiCamera.
        if self.usePiCamera:

            self.cam.capture(self.rawCapture, format="bgr")
            self.frame = self.rawCapture.array

        else:

            # Capture the video frame by frame from the
            # self.cam. This is from normal USB based
            # web cam.
            retVal, self.frame = self.cam.read()

        #print(len(self.faces))

        # Draw rectangle around the faces.
        if len(self.faces) > 0:
            for(x, y, w, h) in self.faces:
                cv2.rectangle(
                    self.frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 0, 255),
                    2
                )

        if not self.config.withoutOCVGUI[2]:

            # Display the resulting frame. Comment this line
            # of codes below if the program is going to be
            # headless. It is necessary to start the window
            # in the new thread. Otherwise it will not updated
            # (static image).
            cv2.startWindowThread()
            cv2.namedWindow("CamFaceDetection")
            cv2.imshow("CamFaceDetection", self.frame)

        # Do not for get to clear the PiCamera "cache"
        # so that it can start taking new image. It is
        # not necessary to do is when using USB web cam.
        if self.usePiCamera: self.rawCapture.truncate(0)

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
        arrayForDB.extend(self.tSC.dateTime)
        arrayForDB.extend(["faces", _facesLen])

        #print(arrayForDB)

        return arrayForDB
