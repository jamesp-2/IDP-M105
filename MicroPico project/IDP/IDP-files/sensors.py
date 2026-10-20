"""Distance-sensor integration placeholder."""

from machine import Pin
from config import track_1, track_2, track_3, track_4

# Create each sensor input once rather than reconfiguring the pins per sample.
track_sensors = [
    Pin(track_1, Pin.IN),
    Pin(track_2, Pin.IN),
    Pin(track_3, Pin.IN),
    Pin(track_4, Pin.IN),
]


def read_line_sensors():
    readings = [sensor.value() for sensor in track_sensors]


def get_distance():
    """Read a distance once the installed driver's API has been identified."""
    pass

