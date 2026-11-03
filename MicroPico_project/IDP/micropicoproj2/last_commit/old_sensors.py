"""Distance-sensor integration placeholder."""

from machine import Pin, ADC, SoftI2C
from old_config import track_1, track_2, track_3, track_4, hall_pin, sda_pin, scl_pin, ir_pin
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
ir_adc = ADC(Pin(ir_pin, Pin.IN))

def get_magnetic_reading():
    total = 0
    for i in range(10):
        total += (hall_adc.read_u16())
        print(hall_adc.read_u16())
    val = total/10

    print(val)

    if val > 41000:
        print("North")
        return "N"

    elif val < 38000:
        print("South")
        return"S"
    return "S"

def ir_sensor():
    print(ir_adc.read_u16())
    time.sleep_ms(5)
    
#while True:
    #ir_sensor()

#claw.open_claw()
#time.sleep(1)
#claw.lower()
#time.sleep(1.5)
#claw.close_claw()
#time.sleep(1)
#claw.lift()
#time.sleep(2)

#while True:
#    get_magnetic_reading()
#    time.sleep_ms(100)
    

    


