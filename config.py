#Output pins
from machine import Pin, PWM #type: ignore

left_motor_dir = 4
left_motor_pwm = 5
right_motor_dir = 7
right_motor_pwm = 6

#LEDS
red_pin = 10
yellow_pin = 9
green_pin = 8

#Servos
servo_1 = 15
servo_2 = 28

#Input pins

#Sensors
hall_pin = 26 #Analogue
crash_pin = 14
IR_pin = 27 #Analogue

#Distance pins
sda_pin = 12
scl_pin = 13


button = Pin(15, Pin.IN, Pin.PULL_DOWN)

#Track sensors
track_1 = 0
track_2 = 1
track_3 = 2
track_4 = 3