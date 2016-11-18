from text import textCollection
import cv2


class WebcamFaceDetection(object):


    def __init__(self):


        #Whether or not a face is detected.
        self.faceCounter = 0
        self.faceDetected = False
        self.faceDetectedThreshold = 5
        # Assign to which camera this program should listen
        ## 0 means the default camera attached in the
        ## computer.
        self.webcam = cv2.VideoCapture(0)


    def FaceDetect(self):


        # Capture from web cam frame by frame.
        vidCapRetVal, vidCapFrame = self.webcam.read()


        #Convert the captured frame into grayscale.
        vidCapGray = cv2.cvtColor(
            vidCapFrame,
            cv2.COLOR_BGR2GRAY
        )

        #Path to the cascade.
        #Cascade is a pattern to detect something.
        #In this case I want to detect faces.
        cascadeFrontFaceDefaultPath = (
            "./cascade-face-front-default.xml"
        )
        cascadeFaceFrontDefault = cv2.CascadeClassifier(
            cascadeFrontFaceDefaultPath
        )
        #Detect faces.
        faces = cascadeFaceFrontDefault.detectMultiScale(
            vidCapGray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30, 30),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )


        #Sometimes there are faces that is not a human face.
        #This is what I called the noise faces.
        #Below are the codes to remove those noise faces.
        if(len(faces) == 0):
            self.faceCounter -= 1
            self.faceDetected = False
        elif(len(faces) > 0):
            self.faceCounter += 1
        if(self.faceCounter > self.faceDetectedThreshold):
            self.faceCounter = self.faceDetectedThreshold
            self.faceDetected = True
        if(self.faceCounter < 0):
            self.faceCounter = 0


        #Print if there is a face detected or into terminal.
        print(textCollection.faceDetected % self.faceDetected)


        #Draw rectangle around the faces.
        for(x, y, w, h) in faces:
            cv2.rectangle(
                vidCapFrame,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )


        #Display the resulting frame. Comment this line
        ## of codes below if the program is going to be
        ## headless.
        #cv2.imshow("main.py", var_capture_video_frame.


    #Function that need to be executed when the program
    ## close.
    def Quit(self):


        # When this program is terminated do not forget to
        ## free the camera that was previously used and
        ## destroy all user interface window if there is
        ## any.
        print(textCollection.closeWindows)
        cv2.destroyAllWindows()
        print(textCollection.releaseWebcam)
        self.webcam.release()