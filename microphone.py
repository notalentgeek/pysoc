import alsaaudio
import aubio
import numpy
import text_collection
import threading


class MicPVDetection(threading.Thread):


    def __init__(
        self,
        _array,
        _counter,
        _textUpdate,
        _threadID,
        _threadName
    ):


        # "Super".
        threading.Thread.__init__(self)
        self.counter = _counter
        self.textUpdate = _textUpdate
        self.threadID = _threadID
        self.threadName = _threadName


        # Append this into array.
        _array.append(self)


        # A trigger to kill this thread.
        self.killMe = False


        # Constants.
        self.BUFFER_SIZE = 2048
        self.METHOD = "default"
        self.SAMPLE_RATE = 44100
        self.HOP_SIZE = self.BUFFER_SIZE//2
        self.PERIOD_SIZE_IN_FRAME = self.HOP_SIZE


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


    def run(self):
        while(self.killMe == False):
            self.PVDetect()


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


        # Show the result into terminal.
        self.textUpdate.UpdateMicPVDetection(
            pitch, volume
        )