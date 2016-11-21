from microphone import MicPVDetection
from text_collection import textCollection, TextUpdate
from webcam import WebcamFaceDetection
import os
import sys
import thread


def main(args):



    # Create an array to hold all threads.
    threads = []
    # Create new threads.
    textUpdate = TextUpdate(threads, 1, "textUpdate", 1)
    micPVDetection = MicPVDetection(
        threads, 2, "MicPVDetection", textUpdate, 2
    )
    webcamFaceDetection = WebcamFaceDetection(
        threads, 3, "WebcamFaceDetection", textUpdate, 3
    )


    # Start all threads.
    for thread in threads:
        thread.start()


    while(len(threads) > 0):



        try:


            # Join all threads using a timeout
            # so it does not block. Filter out
            # threads which have been joined or
            # are None.
            for thread in threads:
                if thread.isAlive() and thread != None:
                    thread.join(1)


        except KeyboardInterrupt:


            print(textCollection.quitProgram)
            for thread in threads:
                thread.killMe = True
                os._exit(1)


if __name__ == '__main__':
    main(sys.argv)