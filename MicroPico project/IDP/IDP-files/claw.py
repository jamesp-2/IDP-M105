"""Servo setup and explicit placeholders for claw/lift movements."""

from config import servo_1, servo_2
from machine import Pin, PWM #type: ignore

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
        if angle < 0:
            angle = 0
        if angle > 270:
            angle = 270

        # Linearly interpolate a PWM duty value between the endpoint duties.
        duty = int(Servo.MIN_DUTY + (angle / 270) * (Servo.MAX_DUTY - Servo.MIN_DUTY))
        self.servo.duty_u16(duty)

# Instantiate the two servos using their configured GPIO pins.
servo_claw = Servo(Pin(servo_1))
servo_lift = Servo(Pin(servo_2))

def close_claw():
    """Placeholder until the correct closed angle is known for the claw."""
    raise NotImplementedError("Set the claw's close angle for the installed mechanism.")

def lift():
    """Placeholder until the correct raised angle is known for the lift."""
    raise NotImplementedError("Set the lift's raised angle for the installed mechanism.")

def open_claw():
    """Placeholder until the correct open angle is known for the claw."""
    raise NotImplementedError("Set the claw's open angle for the installed mechanism.")

def lower():
    """Placeholder until the correct lowered angle is known for the lift."""
    raise NotImplementedError("Set the lift's lowered angle for the installed mechanism.")
