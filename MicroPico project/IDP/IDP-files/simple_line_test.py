"""Standalone test loop for the four line-tracking sensors."""

import time
import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from machine import Pin
from config import track_1, track_2, track_3, track_4
from path import line_following

# Create each sensor input once rather than reconfiguring the pins per sample.
track_sensors = [
    Pin(track_1, Pin.IN),
    Pin(track_2, Pin.IN),
    Pin(track_3, Pin.IN),
    Pin(track_4, Pin.IN),
]


def read_line_sensors():
    """Return the current digital states in left-to-right sensor order."""
    return [sensor.value() for sensor in track_sensors]


# Monitor the sensor inputs and apply one line-following step per sample.
while True:
    readings = read_line_sensors()
    print(readings)
    line_following(readings, read_line_sensors)
    time.sleep_ms(50)
