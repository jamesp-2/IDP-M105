"""Line-sensor validation, line following, and basic junction response."""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from mapping import *
import time
from motors import *
from sensors import *


def line_correction(line_sensor_readings, direction = "F"):
    """Apply one steering correction based on the two center sensors."""

    # Sensors 1 and 2 are the inner pair; 1 means that sensor sees the line.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    # Pivot toward the side whose inner sensor still detects the line.
    if inner_sensors == [0, 1]:
        bot.turn("right", 60)
    elif inner_sensors == [1, 0]:
        bot.turn("left", 60)
    elif inner_sensors == [0, 0]:
        # Neither inner sensor sees the line, so reverse to search for it.
        if direction == "R":
            bot.forward(30)
        else:
            bot.reverse(30)

