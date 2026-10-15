"""Standalone test loop for the four line-tracking sensors."""

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


# Continuously sample the sensors and pass fresh readings to the line controller.
while True:
    line_following(read_line_sensors(), read_line_sensors)

