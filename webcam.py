from mod_thread import ModThread as mt
import cv2

class CamFaceDetection(mt):

    def __init__(
        self
        _threadName,
        _array,
    ):

        # Append this object into array.
        _array.append(self)

        mt.__init__(
            self,
            _array.index(self) + 1,
            _array.index(self) + 1,
            _threadName
        )

        # Detection threshold to prevent "noise" face.
        # The value means that a face need to be detected
        # at least two seconds to be considered a face.
        self.FACE_DTCT_THRS = 2
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


    def run(self):

        if self.killMe == True: self.Quit()
        while self.killMe == False: self.FaceDetect()

    def FaceDetect(self):

        # Capture the video frame by frame from the
        # self.cam.
        retVal, frame = self.cam.read()

        # Convert the captured frame into greyscale.
        frameGrey = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY)

        # Face detection.
        faces = casc.detectMultiScale(
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
            self.SetupStringForDB(len(faces))

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


    # Function that need to be executed when the program
    # is closing.
    def Quit(self):

        # When this program is terminated do not forget
        # to free the camera that previously used and destroy
        # all user interface and windows if there is any,
        cv2.destroyAllWindows()
        self.cam.release()

    def SetupStringForDB(
        self,
        _facesLen
    ):

        # Set up the strings.
        dt      = str(datetime.utcnow()).split(".")[0] # Date and time.
        date    = str(dtStr).split(" ")[0]
        time    = str(dtStr).split(" ")[1]
        year    = str(dateStr).split("-")[0]
        month   = str(dateStr).split("-")[1]
        day     = str(dateStr).split("-")[2]
        hour    = str(timeStr).split(":")[0]
        minu    = str(timeStr).split(":")[1]
        sec     = str(timeStr).split(":")[2]
        utc     = str(get_localzone()).lower() # UTC time zone (without DST).

        arrayForDB = [
            year,
            month,
            day,
            hour,
            minu,
            sec,
            utc,
            str(_facesLen)
        ]

        return arrayForDB