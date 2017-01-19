import sys
sys.path.append("./src")

# Import some necessary libraries.
# Modified thread class.
from mod_thread import ModThread as mt

# This is a class to execute codes per one second.
# However, these codes are not accurate. In case
# that the one tick of code execution takes more than
# one second. At least work for now.
from timer_second_change import TimerSecondChange as tsc

# Before using PyAudio I was using AlsaAudio to stream data
# from microphone. However, now I know how to use PyAudio,
# a higher level audio framework that works in most desktop
# operating system (Linux, MacOS, Windows).
import pyaudio

# Aubio has built - in pitch detection object.
import aubio

# NumPy is used to convert PyAudio format into
# numbers that Aubio can understand.
import numpy as num

# Class for pitch and volume detection.
# Make this as a thread class extended
# from ModThread (modified Thread class).
class MicPVDetect(mt):

    # Constructor.
    # _threadName is this object thread name.
    # _arrau is the main array in the main
    # thread that manages array.
    # _iDB is the database insertion object.
    # _iDB is a specific database object in
    # separate thread that handles database
    # insertion. Thus, data from every other
    # input device are queued beautifully into
    # the database.
    def __init__(self, _threadName, _array, _iDB, _useRPI):

        # Append this object into the array
        # that holds all thread (excluding the
        # main thread) in the main thread.
        _array.append(self)

        # Java's super! The second and the
        # third parameter is the index and
        # the count. I honestly do not
        # know why count and index variable
        # are necessary in Thread object and
        # why are those not a built - in
        # variables.
        mt.__init__(self,
            _array.index(self) + 1,
            _array.index(self) + 1,
            _threadName)

        # Database object.
        self.iDB = _iDB
        # Whether user stated to run this application in
        # Raspberry PI's Raspbian Jessie or not.
        self.useRPI = _useRPI

        # Some constants. I honestly not sure what does
        # what. I get this number from issue I post in
        # Aubio GitHub. However, these constant below are
        # for PyAudio streaming and Aubio pitch processing.
        self.BUFFER_SIZE = 2048
        self.CHANNELS = 1
        self.FORMAT = pyaudio.paFloat32
        self.METHOD = "default"
        self.SAMPLE_RATE = 44100
        self.HOP_SIZE = self.BUFFER_SIZE//2
        self.PERIOD_SIZE_IN_FRAME = self.HOP_SIZE

        # Constant for database table name.
        self.MODULE_NAME = "mic"

        # Initiating PyAudio object.
        pA = pyaudio.PyAudio()

        # In Raspberry PI's Raspbian I need to determine
        # the default card manually. Hence, `input_device_index=2`.
        if self.useRPI:
            # Open the microphone stream.
            self.mic = pA.open(
                channels=self.CHANNELS,
                format=self.FORMAT,
                frames_per_buffer=self.PERIOD_SIZE_IN_FRAME,
                input=True,
                input_device_index=2,
                rate=self.SAMPLE_RATE)
        else:
            # Open the microphone stream.
            self.mic = pA.open(
                channels=self.CHANNELS,
                format=self.FORMAT,
                frames_per_buffer=self.PERIOD_SIZE_IN_FRAME,
                input=True,
                rate=self.SAMPLE_RATE)

        # Finally create the main pitch detection object.
        # This object is from Aubio library.
        self.pitchDetector = aubio.pitch(self.METHOD,
            self.BUFFER_SIZE, self.HOP_SIZE,
            self.SAMPLE_RATE)
        # Set the output unit. This can be "cent",
        # "midi", "Hz".
        self.pitchDetector.set_unit("Hz")
        # Ignore frames under this level.
        self.pitchDetector.set_silence(-40)

        # Object wide known variable that hold
        # data gathered from the microphone.
        self.data = None

        # Set up a timer object. To make sure that the audio
        # calculation only happen once every second.
        # However, although the calculation only happen once
        # every second, the microphone stream need to still
        # open.
        self.tSC = tsc()

    def run(self):

        #print("test")

        # The self.killMe variable is from the ModThread
        # class that is mt in this class. ModThread is
        # the super class of this class.
        while self.killMe == False:

            # Update the timer.
            self.tSC.Update()
            # Keep the microphone stream open.
            self.Stream()

            # Execute only if a second passed since last
            # tick. The pitch and volume calculation only
            # happen once every second. self.tSC.changeSecond
            # will return True if a second is passed.
            if self.tSC.changeSecond: self.PVDetect()

    # String array to be inputted into database.
    # I can put this into shared function file actually.
    def SetupStringForDatabase(self, _pitch, _volume):

        # The first element in the array is this module
        # name. For this case the module name is "mic"
        # from microphone.
        theArrayThatWillBeReturned = [self.MODULE_NAME]

        # Get all the date and time elements from
        # TimerSecondChange dateTime variable. dateTime
        # variable will be always updated to current date and time
        # in sync Thread wide.
        theArrayThatWillBeReturned.extend(self.tSC.dateTime)

        # Append the pitch and the volume parameter.
        # There will be two elements per one variable.
        # The first element would be the document name.
        # While, the second element would be the value.
        theArrayThatWillBeReturned.extend([
            "pitch", str(_pitch),
            "volume", str(_volume)])

        #print(theArrayThatWillBeReturned)

        return theArrayThatWillBeReturned

    # Function for pitch and volume detection.
    def PVDetect(self):

        print("test")

        # Convert data from the microphone of
        # AlsaAudio library into Aubio format samples.
        samples = num.fromstring(self.data,
            dtype=aubio.float_type)

        # Pitch of the current frame.
        pitch = self.pitchDetector(samples)[0]

        # Compute the energy (volume) of the
        # current frame.
        volume = num.sum(samples**2)/len(samples)
        # Format the volume output so that at most
        # it has six decimal numbers.
        volume = "{:.6f}".format(volume)

        # Append the data that I want to put into database.
        # I need to append the data into insert database
        # object mainArray. Every elements in the mainArray
        # in the insert database object will automatically
        # popped and then put into the database.
        if self.iDB != None:
            self.iDB.mainArray.append(
                self.SetupStringForDatabase(pitch,
                    volume))

        #print(pitch)
        #print(volume)

    # This is the function that is executed for every
    # tick. The program should not stop streaming data
    # from the input device (in this case it is the
    # microphone). If there is a tick when this program
    # stopped streaming information from microphone, the
    # microphone will need to be re - initialized again in
    # the next tick.
    def Stream(self):

        # Keep reading data from the audio input.
        # `exception_on_overflow=False` to prevent this
        # application stuck in Raspberry PI's Raspbian
        # Jessie.
        self.data = self.mic.read(self.PERIOD_SIZE_IN_FRAME,
            exception_on_overflow=False)
