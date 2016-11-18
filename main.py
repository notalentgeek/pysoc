from text import textCollection
from webcam import WebcamFaceDetection
from microphone import MicPVDetection
import atexit
import cv2
import sys


# Initiate
micPVDetection = MicPVDetection()
# Initiate webcam face detection.
webcamFaceDetection = WebcamFaceDetection()

def Quit():


    print(textCollection.quitProgram)
    webcamFaceDetection.Quit()


# Register exit handler.
atexit.register(Quit)


while True:


    try:
        micPVDetection.PVDetect()
        webcamFaceDetection.FaceDetect()


    except KeyboardInterrupt:


        print(textCollection.quitProgram)
        break