from config import servo_1, servo_2

class servo:
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

servo_claw = Servo(Pin(servo_1))
servo_lift = Servo(Pin(servo_2))

def close_claw():
    #servo_claw.set_angle(0) or something
    pass

def lift():
    pass

def open_claw():
    pass

def lower():
    pass
