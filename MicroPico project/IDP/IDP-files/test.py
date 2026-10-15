"""Run a short reverse test using the project motor controller."""

import sys
import time

# The MicroPico project root is the parent of IDP-files.
if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

import motors

# Use a positive speed so the reverse command actually drives the motors.
motors.bot.turn("right", 30)
time.sleep(2)
motors.bot.stop()