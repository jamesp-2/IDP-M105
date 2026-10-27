"""Servo setup and explicit placeholders for claw/lift movements."""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from config import servo_1, servo_2
from machine import Pin, PWM #type: ignore
import time

class Servo:
    """Drive a servo with a 50 Hz PWM signal and a 0-270 degree command."""

    # PWM duty values used for the supported servo travel range.
    MIN_DUTY = 1638 # 0°
    MID_DUTY = 4915 # 135°
    MAX_DUTY = 8192 # 270°

    def __init__(self, ServoPin):
        # Configure the servo control signal at the standard 50 Hz rate.
        self.servo = PWM(ServoPin)
        self.servo.freq(50)  # 50 Hz for servo

    def set_angle(self, angle):
        """Set the servo angle, clamping requests to its defined travel."""
        if angle < 163:
            angle = 163
        if angle > 215:
            angle = 215

        # Linearly interpolate a PWM duty value between the endpoint duties.
        duty = int(Servo.MIN_DUTY + (angle / 270) * (Servo.MAX_DUTY - Servo.MIN_DUTY))
        self.servo.duty_u16(duty)

# Instantiate the two servos using their configured GPIO pins.
servo_claw = Servo(Pin(servo_1))
servo_lift = Servo(Pin(servo_2))

def close_claw():
    servo_claw.set_angle(163)

def lift():
    servo_lift.set_angle(215)
    return

def lift_small():
    servo_lift.set_angle(205)
    return

def open_claw():
    servo_claw.set_angle(200)
    return

def open_claw_small():
    servo_claw.set_angle(187)
    return

def lower():
    servo_lift.set_angle(195)
    return

