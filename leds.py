from machine import Pin
import time
from config import red_pin, yellow_pin, green_pin
 
On = 1
Off = 0

#Flash frequency in ms -> 2Hz half time
flash_period = 250

class LED:
    def __init__(self):
        self.red = Pin(red_pin, Pin.OUT)
        self.yellow = Pin(yellow_pin, Pin.OUT)
        self.green = Pin(green_pin, Pin.OUT)

        self.flashing = False

        self.red.value(Off)
        self.yellow.value(Off)
        self.green.value(Off)

        self.operating = False

        self.flash = Off
        self.last_toggle = time.ticks_ms()


def start(self):
    self.operating = True

def stop(self):
    self.operating = False
    self.red.value(Off)
    self.yellow.value(Off)
    self.green.value(Off)
    self.flashing = False

#Green or red light from polarity 

def polarity(self,pole):
    if pole =="N":
        self.red.value(On)
        self.yellow.value(Off)
        self.green.value(Off)
    elif pole =="S":
        self.red.value(Off)
        self.yellow.value(Off)
        self.green.value(On)

#Flashing yellow light to indicate that the system is in operation

def flash(self):

    now = time.ticks_ms()
    if time.ticks_diff(now, self.last_toggle) >= flash_period:
        self.last_toggle = now

        self.yellow.value(if self.value == On else Off)

        
        
    

