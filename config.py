#Output pins
from machine import Pin, PWM

left_motor_dir = 0
left_motor_pwm = 0
right_motor_dir = 0
right_motor_pwm = 0

#LEDS
red_pin = 0
yellow_pin = 0
green_pin = 0

#Servos
servo_1 = 0
servo_2 = 0

#Input pins

#Sensors
hall_pin = 0
crash_pin = 0
distance_pin = 0
IR_pin = 0


button = Pin(0, Pin.IN, Pin.PULL_DOWN)

#Track sensors
track_1 = 0
track_2 = 0
track_3 = 0
track_4 = 0