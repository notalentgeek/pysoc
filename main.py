from text import textCollection
from webcam import WebcamFaceDetection
import atexit
import cv2
import sys


#Initiate webcam face detection.
webcamFaceDetection = WebcamFaceDetection()

def Quit():


    print(textCollection.quitProgram)
    webcamFaceDetection.Quit()


#Register exit handler.
atexit.register(Quit)


while True:


    webcamFaceDetection.FaceDetect()