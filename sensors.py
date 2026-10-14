#For the magent, IR light (traffic light) and crash sensors
from config import hall_pin, IR_pin, crash_pin, sda_pin, scl_pin
from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X

#Distance sensor
def get_distance():
    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9))

    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)
