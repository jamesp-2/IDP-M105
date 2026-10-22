"""Central GPIO assignments for robot motors, indicators, servos, and sensors."""

# Motor direction and PWM output pins.
from machine import Pin, PWM #type: ignore

left_motor_dir = 4
left_motor_pwm = 5
right_motor_dir = 7
right_motor_pwm = 6

# Status LED output pins.
red_pin = 20
yellow_pin = 21
green_pin = 22

# Servo control pins.
servo_1 = 15
servo_2 = 28

# Sensor input pins.
hall_pin = 27 #Analogue
crash_pin_1 = 17
crash_pin_2 = 18
IR_pin = 26 #Analogue

# I2C pins used by the distance sensor.
sda_pin = 12
scl_pin = 13

# Start button input with a pull-down resistor enabled.
button = Pin(28, Pin.IN, Pin.PULL_DOWN)

# Four line-tracking sensor input pins.
track_1 = 0
track_2 = 1
track_3 = 12
track_4 = 13