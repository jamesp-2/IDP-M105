"""Central GPIO assignments for robot motors, indicators, servos, and sensors."""

# Motor direction and PWM output pins.
from machine import Pin, PWM #type: ignore

left_motor_dir = 7
left_motor_pwm = 6
right_motor_dir = 4
right_motor_pwm = 5

# Status LED output pins.
red_pin = 22
yellow_pin = 21
green_pin = 20

# Servo control pins.
servo_1 = 15
servo_2 = 13 #Double check this works

# Sensor input pins.
hall_pin = 27 #Analogue
crash_pin_1 = 0
crash_pin_2 = 0
ir_pin = 26 #Analogue

# I2C pins used by the distance sensor.
sda_pin = 18
scl_pin = 19

# Start button input with a pull-down resistor enabled.
button = Pin(28, Pin.IN, Pin.PULL_DOWN)

# Four line-tracking sensor input pins.
track_1 = 1
track_2 = 10
track_3 = 11
track_4 = 12