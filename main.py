from microphone import MicPVDetection
from text_collection import textCollection
from webcam import WebcamFaceDetection
import atexit
import cv2
import sys
import text_collection
import thread


# Initiate
#micPVDetection = MicPVDetection()
# Initiate webcam face detection.
#webcamFaceDetection = WebcamFaceDetection()


# Create new threads
thread1 = MicPVDetection(1, "MicPVDetection", 1)
thread2 = WebcamFaceDetection(2, "WebcamFaceDetection", 2)

# Start new Threads
thread1.start()
thread2.start()


#def Quit():
#
#
#    print(textCollection.quitProgram)
#    webcamFaceDetection.Quit()
#
#
## Register exit handler.
#atexit.register(Quit)


#while True:
#
#
#    micPVDetection.PVDetect()
#    webcamFaceDetection.FaceDetect()
#
#
#    #Print the update text.
#    print(text_collection.textUpdate)
#    text_collection.textUpdate = ""