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

class Servo:
    MIN_DUTY = 1638 # 0°
    MID_DUTY = 4915 # 135°
    MAX_DUTY = 8192 # 270°

    def __init__(self, ServoPin):
        self.servo = PWM(ServoPin)
        self.servo.freq(50)  # 50 Hz for servo
 
    # Convert angle (0–270) to duty
    def set_angle(self, angle):
       # Clamp angle
       if angle < 0:
           angle = 0
       if angle > 270:
           angle = 270
 
       duty = int(Servo.MIN_DUTY + (angle / 270) * (Servo.MAX_DUTY - Servo.MIN_DUTY))
       self.servo.duty_u16(duty)

servo_1 = Servo(Pin(0))
servo_2 = Servo(Pin(0))

#Input pins

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