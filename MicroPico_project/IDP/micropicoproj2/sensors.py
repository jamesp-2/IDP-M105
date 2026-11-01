"""Distance-sensor integration placeholder."""

from machine import Pin, ADC, SoftI2C
from config import track_1, track_2, track_3, track_4, hall_pin, sda_pin, scl_pin
import time
import sys
from VL53L0X import VL53L0X
from utime import sleep



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
    i2c_bus = SoftI2C(sda=Pin(18), scl=Pin(19)) # I2C0 on GP8 & GP9
    
    # Setup vl53l0 object
    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)

    # Start device
    vl53l0.start()

    # Read ten samples
    distance = 0
    for i in range(10):
        distance += vl53l0.read()
        sleep(0.5)

    # Stop device
    vl53l0.stop()

    distance = (distance - 8191) / 10
    print(distance)
    if distance > 180:
        return 0 #Rack is empty
    else:
        return 1 #Rack is full
    

hall_adc = ADC(Pin(hall_pin, Pin.IN, Pin.PULL_DOWN))
zero_reading= 40000
threshold = 9000

def get_magnetic_reading():
    total = 0
    for i in range(10):
        total += (hall_adc.read_u16())
        print(hall_adc.read_u16())
    val = total/10

    print(val)

    #if val > 50000:
        #print("North")
        #return "N"

    #elif val < 30000:
        #print("South")
        #return"S"
    return "N"


