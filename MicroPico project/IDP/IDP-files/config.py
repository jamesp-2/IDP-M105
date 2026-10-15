"""Central GPIO assignments for robot motors, indicators, servos, and sensors."""

# Motor direction and PWM output pins.
from machine import Pin, PWM #type: ignore

left_motor_dir = 4
left_motor_pwm = 5
right_motor_dir = 7
right_motor_pwm = 6

# Status LED output pins.
red_pin = 10
yellow_pin = 9
green_pin = 8

# Servo control pins.
servo_1 = 15
servo_2 = 28

# Sensor input pins.
hall_pin = 26 #Analogue
crash_pin = 14
IR_pin = 27 #Analogue

# I2C pins used by the distance sensor.
sda_pin = 12
scl_pin = 13

# Start button input with a pull-down resistor enabled.
button = Pin(15, Pin.IN, Pin.PULL_DOWN)

# Four line-tracking sensor input pins.
track_1 = 0
track_2 = 1
track_3 = 2
track_4 = 3