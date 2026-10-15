"""Low-level motor drivers and the two-motor robot controller."""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from machine import Pin, PWM # type: ignore
from config import left_motor_dir, left_motor_pwm, right_motor_dir, right_motor_pwm


class Motor:
    """Control one DC motor using a direction pin and a PWM speed signal."""

    def __init__(self, dirPin, PWMPin):
        # Configure the motor's direction output and PWM output.
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.off()
        
    def off(self):
        """Stop the motor by setting both pins low to remove potential difference."""
        self.mDir.value(0) # Ensure the direction pin is low[cite: 6]
        self.pwm.duty_u16(0) 
        
    def Forward(self, speed):
        """Run the motor forward at a percentage speed from 0 through 100."""
        if speed == 0:
            self.off()
            return

        # This controller uses direction level 0 for forward operation.
        self.mDir.value(0)                     
        # Convert the requested percentage to the 16-bit PWM duty range.
        self.pwm.duty_u16(int(65535 * speed / 100))

    def Reverse(self, speed):
        """Run the motor in reverse at a percentage speed from 0 through 100."""
        if speed == 0:
            self.off()
            return

        # This controller uses direction level 1 for reverse operation.
        self.mDir.value(1)
        # Invert the PWM duty cycle because the direction pin is driven high.
        inverted_duty = 65535 - int(65535 * speed / 100)
        self.pwm.duty_u16(inverted_duty)


class Bot:
    """Coordinate the left and right motors for basic robot movement."""

    def __init__(self):
        # Use the board pin assignments defined in config.py.
        self.left_motor = Motor(left_motor_dir, left_motor_pwm)
        self.right_motor = Motor(right_motor_dir, right_motor_pwm)

    def stop(self):
        """Stop both wheels."""
        self.left_motor.off()
        self.right_motor.off()

    # Added default speed arguments so test.py and path.py can run without errors
    def forward(self, speed=100):
        """Drive both wheels forward at the same speed."""
        self.left_motor.Forward(speed)
        self.right_motor.Forward(speed)

    def reverse(self, speed=30):
        """Drive both wheels backward at the same speed."""
        self.left_motor.Reverse(speed)
        self.right_motor.Reverse(speed)

    def turn(self, direction, speed=50):
        """Turn in place by driving the wheels in opposite directions."""
        if direction == "left":
            self.left_motor.Reverse(speed)
            self.right_motor.Forward(speed)
        elif direction == "right":
            self.left_motor.Forward(speed)
            self.right_motor.Reverse(speed)
        else:
            raise ValueError("Direction must be 'left' or 'right'.")

    def turn_around(self, speed=50):
        """Rotate approximately 180 degrees using opposite wheel motion."""
        self.left_motor.Reverse(speed)
        self.right_motor.Forward(speed)

# Create the shared robot controller used by path-following code.
bot = Bot()