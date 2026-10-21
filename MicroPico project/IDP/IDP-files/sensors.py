"""Distance-sensor integration placeholder."""

from machine import Pin, ADC
from config import track_1, track_2, track_3, track_4, hall_pin
import time
import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

# Create each sensor input once rather than reconfiguring the pins per sample.
track_sensors = [
    Pin(track_1, Pin.IN),
    Pin(track_2, Pin.IN),
    Pin(track_3, Pin.IN),
    Pin(track_4, Pin.IN),
]


def read_line_sensors():
    readings = [sensor.value() for sensor in track_sensors]
    return readings


def get_distance():
    """Read a distance once the installed driver's API has been identified."""
    pass

hall_adc = ADC(hall_pin)
zero_reading= 400
threshold = 9000

def get_magentic_reading():
    total = 0
    for i in range(10):
        total += hall_adc.read_u16()
        print (hall_adc.read_u16())
    val = total/10

    print(val)

    if val > threshold:
        print("North")
        return "N"

    elif val < -threshold:
        print("South")
        return"S"

    return None

