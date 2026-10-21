from machine import Pin, ADC
import time
import sys


hall_adc = ADC(26)
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

if __name__ == "__main__":
    get_magnetic_reading()
