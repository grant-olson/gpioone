import RPi.GPIO as GPIO
from time import sleep

class DcMotor:
    def __init__(self, enable, in_1, in_2):
        self.enable = enable
        self.in_1 = in_1
        self.in_2 = in_2

        GPIO.setup(self.enable, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in_1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in_2, GPIO.OUT, initial=GPIO.LOW)

        self.enable_pwm = GPIO.PWM(self.enable, 100)
        self.enable_duty_cycle = 0
        self.enable_pwm.start(self.enable_duty_cycle)
        
    def forward(self,duration=None):
        GPIO.output(self.in_2, GPIO.LOW)
        GPIO.output(self.in_1, GPIO.HIGH)

        if duration:
            sleep(duration)
            self.stop()
            
    def reverse(self, duration=None):
        GPIO.output(self.in_1, GPIO.LOW)
        GPIO.output(self.in_2, GPIO.HIGH)

        if duration:
            sleep(duration)
            self.stop()
            
    def stop(self):
        GPIO.output(self.in_1, GPIO.LOW)
        GPIO.output(self.in_2, GPIO.LOW)

    def speed(self,percent):
        self.enable_duty_cycle = percent
        self.enable_pwm.ChangeDutyCycle(self.enable_duty_cycle)

    def ramp_down(self,seconds):
        current_duty_cycle = self.enable_duty_cycle
        for i in range(current_duty_cycle, 0, -(current_duty_cycle / 10)):
            self.speed(i)
            sleep(float(seconds) / 10)
            
    def ramp_up(self,percent,seconds):
        current_duty_cycle = self.enable_duty_cycle
        for i in range(current_duty_cycle, percent, ((percent - current_duty_cycle) / 10)):
            self.speed(i)
            sleep(float(seconds) / 10)
