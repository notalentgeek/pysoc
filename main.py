from microphone import MicPVDetection
from text_collection import textCollection
from webcam import WebcamFaceDetection
import atexit
import cv2
import sys
import text_collection


# Initiate
micPVDetection = MicPVDetection()
# Initiate webcam face detection.
webcamFaceDetection = WebcamFaceDetection()


def Quit():


    print(textCollection.quitProgram)
    webcamFaceDetection.Quit()


# Register exit handler.
atexit.register(Quit)

counter = 0

while True:


    micPVDetection.PVDetect()

    if(counter == 10):
        webcamFaceDetection.FaceDetect()
        counter = 0
    counter += 1


    #Print the update text.
    print(text_collection.textUpdate)
    text_collection.textUpdate = ""