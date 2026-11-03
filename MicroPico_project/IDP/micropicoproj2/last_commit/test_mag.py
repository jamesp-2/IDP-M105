from machine import Pin, ADC
import config
import time
import sys


hall_adc = ADC(Pin(config.hall_pin, Pin.IN))
zero_reading= 400
threshold = 9000

def get_magentic_reading():
    total = 0
    for i in range(100):
        time.sleep_ms(1)
        total += hall_adc.read_u16()
    val = total/100

    print(val)

    if val > 50000:
        print("North")
        return "N"

    elif val < 30000:
        print("South")
        return"S"

    return None

while True:
    get_magentic_reading()
    time.sleep(0.2)