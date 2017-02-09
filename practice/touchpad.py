#!/usr/bin/env python3

""" Enable or disable notebook touchpad """

import os

class Touchpad():

    def __init__(self):
    """ Initializes touchpad with current status: 0 (enable), 1 (disable) """
        self.state = self._getState()

    def _getState(self):
    """ Get status of touchpad
        req returns string like "TouchpadOff = n", n in (0, 1)
    """
        req = "synclient -l | grep TouchpadOff"
        SEP = "="
        data = os.popen(req).readline()
        return data.split(SEP)[1].strip()

    def isTurned(self, TP_STATE):
    """ Check whether touchpad is turned on or off """
        return self.state == TP_STATE

    def turn(self, STATE):
    """ Change touchpad state """
        req = "synclient TouchpadOff=%s" % (STATE)
        os.system(req)


def main():
    
    # Touchpad statuses in synclient request
    ON = "0"
    OFF = "1"

    tp = Touchpad()
    if tp.isTurned(OFF):
        tp.turn(ON)
    else:
        tp.turn(OFF)

if __name__ == "__main__":
    main()

