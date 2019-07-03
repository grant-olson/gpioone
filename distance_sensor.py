import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
import rgb_led
from time import sleep

GPIO.setmode(GPIO.BCM)

ultrasonic = DistanceSensor(echo=21,trigger=20,max_distance=2)

led = rgb_led.RgbLed(4,5,6)

led.set_green_state(GPIO.HIGH)
sleep(2)
led.set_green_state(GPIO.LOW)


led.start_intensity_mode()

red = 0
green = 0
blue = 0

count = 0

def get_inverse_percent(min, max, actual):
    ip =  100.0 - ((actual - min) / (max - min) * 100.0)
    if ip < 20:
        ip = 20
    return ip

while True:
    
    distance = ultrasonic.distance
    red = 0
    green = 0
    blue = 0
    
    if distance <= 0.5:
        red = get_inverse_percent(0.0, 0.5, distance)
    elif distance <= 1.0:
        blue = get_inverse_percent(0.5, 1.0, distance)
    else:
        green = get_inverse_percent(1.0, 2.0, distance)
    led.set_red_intensity(red)
    led.set_green_intensity(green)
    led.set_blue_intensity(blue)

    count += 1

    # Print value every second
    if count % 20 == 0:
        print(distance)
    sleep(0.05)



GPIO.cleanup()
