import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

print("SETTING UP!")

blue = 5
green = 6
red = 4

GPIO.setup(blue, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(red, GPIO.OUT, initial=GPIO.LOW)
sleep(1)

print("TURNING BLUE ON")
GPIO.output(blue, GPIO.HIGH)
sleep(1)
print("TURNING GREEN ON")

GPIO.output(blue, GPIO.LOW)
GPIO.output(green, GPIO.HIGH)
sleep(1)

print("TURNING RED ON")
GPIO.output(green, GPIO.LOW)
GPIO.output(red, GPIO.HIGH)
sleep(1)

print("TURNING BLUE ON 50%")
#GPIO.PWM(blue, 50)

blue_pwm = GPIO.PWM(blue, 100)
red_pwm = GPIO.PWM(red, 100)
green_pwm = GPIO.PWM(green, 100)

blue_pwm.start(100)
green_pwm.start(100)
red_pwm.start(100)

sleep(1)
try:
    while True:
        for x in range(0,100):
            blue_pwm.ChangeDutyCycle(x)
            red_pwm.ChangeDutyCycle(100-x)
            green_pwm.ChangeDutyCycle(x)
            sleep(0.010)
        for x in range(100,0,-1):
            blue_pwm.ChangeDutyCycle(x)
            red_pwm.ChangeDutyCycle(100-x)
            green_pwm.ChangeDutyCycle(x)
            sleep(0.010)
except KeyboardInterrupt:
    print("CAUGHT KEYBOARD INTERRUPT")
sleep(1)

# CLEANUP

blue_pwm.stop()
red_pwm.stop()
green_pwm.stop()

#blue_pwm.start(50)
#sleep(1)
#blue_pwm.start(25)
#sleep(1)

print("CLEANING UP")
GPIO.output(blue, GPIO.LOW)
GPIO.output(green, GPIO.LOW)
GPIO.output(red, GPIO.LOW)
