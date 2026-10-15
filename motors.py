from machine import Pin, PWM # type: ignore
from config import left_motor_dir, left_motor_pwm, right_motor_dir, right_motor_pwm
import time


class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        self.off()
        
    def off(self):
        self.pwm.duty_u16(0) 
        
    def Forward(self, speed=100):
        self.mDir.value(0)                     
        self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

    def Reverse(self, speed=30):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))

class Bot:
    def __init__(self):
        self.left_motor = Motor(left_motor_dir, left_motor_pwm)
        self.right_motor = Motor(right_motor_dir, right_motor_pwm)

    def stop(self):
        self.left_motor.off()
        self.right_motor.off()

    def forward(self, speed=100):
        self.left_motor.Forward(speed)
        self.right_motor.Forward(speed)

    def reverse(self, speed=30):
        self.left_motor.Reverse(speed)
        self.right_motor.Reverse(speed)

    def turn(self, direction, speed=60):
        if direction == "left":
            self.left_motor.Reverse(speed)
            self.right_motor.Forward(speed)
        elif direction == "right":
            self.left_motor.Forward(speed)
            self.right_motor.Reverse(speed)

    def turn_around(self,speed=60):
        self.left_motor.Reverse(speed)
        self.right_motor.Forward(speed)

bot = Bot()
bot.forward()
time.sleep(5)
bot.stop()