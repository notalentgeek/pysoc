from   timer_second_change import TimerSecondChange as tsc
import subprocess                                   as subp

tSC = tsc()

while True:

    tSC.Update()
    if tSC.chngSec:

        subp.call(["irsend SEND_ONCE pysoc KEY_1"], shell=True)
        print("KEY_1 has just pressed")