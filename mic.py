from mod_thread import ModThread as mt
from shared_thread_function import GetDateTime as gdt
from timer_second_change import TimerSecondChange as tms
from tzlocal import get_localzone
import alsaaudio as alsa
import aubio
import numpy as num

class MicPVDetect(mt):

    def __init__(
        self,
        _threadName,
        _array
    ):

        # Append this object into array.
        _array.append(this)

        mt.__init__(
            self,
            _array.index(self) + 1,
            _array.index(self) + 1,
            _threadName
        )

        # Constants.
        self.BUFFER_SIZE = 2048
        self.METHOD = "default"
        self.SAMPLE_RATE = 44100
        self.HOP_SIZE = self.BUFFER_SIZE//2
        self.PERIOD_SIZE_IN_FRAME = self.HOP_SIZE
        # Constant for database.
        self.MODULE_NAME = "mic"

        # Set up audio input. Determine the PCM device
        # (pulse code modulation). The default type is for
        # playback. Hence set the `type` into `alsaaudio.
        # PCM_CAPTURE` instead to capture voice. The
        # microphone is the one that is set in `alsamixer`
        # terminal command. Hence, this alsaaudio library is
        # only for Linux.
        self.recorder = alsaaudio.PCM(
            type = alsaaudio.PCM_CAPTURE
        )
        self.recorder.setchannels(1)
        self.recorder.setformat(
            alsaaudio.PCM_FORMAT_FLOAT_LE
        )
        self.recorder.setperiodsize(
            self.PERIOD_SIZE_IN_FRAME
        )
        self.recorder.setrate(self.SAMPLE_RATE)

        # Set up Aubio energy (volume) and pitch detection.
        self.pitchDetector = aubio.pitch(
            self.METHOD,
            self.BUFFER_SIZE,
            self.HOP_SIZE,
            self.SAMPLE_RATE
        )
        # Set the output unit, it can be "cent", "midi",
        # "Hz", ....t.
        self.pitchDetector.set_unit("Hz")
        # Ignore frames under this level (dB).
        self.pitchDetector.set_silence(-40)

        # Set up timer object. To make sure that
        # the audio calculation only once for
        # every second.
        tMS = tms()

    def run(self):

        while self.killMe == False:

            tMS.Update()
            if tMS.chngSec:
                self.PVDetect()

    def SetupStringForDB(
        self,
        _pitch,
        _volume
    ):

        arrayForDB = [self.MODULE_NAME]
        arrayForDB.extend(gdt())
        arrayForDB.extend([_pitch, _volume])

        return arrayForDB

    def PVDetect(self):

        # Read data from audio input.
        length, data = self.recorder.read()
        # Convert the data from alsaaudio library into Aubio
        # format samples.
        samples = numpy.fromstring(
            data,
            dtype = aubio.float_type
        )
        # Pith of the current frame.
        pitch = self.pitchDetector(samples)[0]
        # Compute the energy (volume) of current frame.
        volume = numpy.sum(samples**2)/len(samples)
        volume = "{:.6f}".format(volume)

        # Database!
        self.SetupStringForDB(pitch, volume)

        print("pitch = " + str(pitch) + " volume = " + str(volume))