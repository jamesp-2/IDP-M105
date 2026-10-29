"""Control the status LEDs and provide a non-blocking yellow flash."""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from machine import Pin #type: ignore
import time
from config import red_pin, yellow_pin, green_pin
from sensors import get_magnetic_reading

# Digital output levels used for turning an LED on or off.
On = 1
Off = 0

# Toggle every 250 ms for a 2 Hz full on/off cycle.
flash_period = 250

class LED:
    """Manage red/green polarity indication and operating-status flashing."""

    def __init__(self):
        # Configure each status LED as a digital output.
        self.red = Pin(red_pin, Pin.OUT)
        self.yellow = Pin(yellow_pin, Pin.OUT)
        self.green = Pin(green_pin, Pin.OUT)

        # Start from a known state with all LEDs off.
        self.red.value(Off)
        self.yellow.value(Off)
        self.green.value(Off)

        # Track the operating state and timing of the yellow LED.
        self.operating = False
        self.yellow_on = False
        self.last_toggle = time.ticks_ms()

    def start(self):
        """Enable operation-status flashing and reset its timer."""
        self.operating = True
        self.last_toggle = time.ticks_ms()

    def stop(self):
        """Disable flashing and turn off every LED."""
        self.operating = False
        self.red.value(Off)
        self.yellow.value(Off)
        self.green.value(Off)
        self.yellow_on = False

    def set_polarity(self, pole):

        #pole = get_magnetic_reading()
        """Show north polarity in red or south polarity in green."""
        if pole == "N":
            self.red.value(On)
            self.yellow.value(Off)
            self.green.value(Off)
        elif pole == "S":
            self.red.value(Off)
            self.yellow.value(Off)
            self.green.value(On)
        else:
            raise ValueError("Pole must be 'N' or 'S'.")

    def flash(self):
        """Toggle yellow when its period elapses, without blocking."""
        if not self.operating:
            return

        # Use wrap-safe MicroPython tick functions to measure elapsed time.
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_toggle) >= flash_period:
            self.last_toggle = now
            self.yellow_on = not self.yellow_on
            self.yellow.value(On if self.yellow_on else Off)


# led = LED()
# led.start()
# time.sleep(0.5)
# start = time.time()
# while time.time() - start < 5:
#     led.flash()
# led.set_polarity("N")
# time.sleep(2)
# led.set_polarity("S")
# time.sleep(2)
# led.stop()
