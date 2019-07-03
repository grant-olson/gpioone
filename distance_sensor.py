import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
import rgb_led
from time import sleep

GPIO.setmode(GPIO.BCM)

near_threshold = 1.0
medium_threshold = 3.0
max_distance = 10.0

ultrasonic = DistanceSensor(echo=21,trigger=20,max_distance=10.0)

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
    
    if distance <= near_threshold:
        red = get_inverse_percent(0.0, near_threshold, distance)
    elif distance <= medium_threshold:
        blue = get_inverse_percent(near_threshold, medium_threshold, distance)
    else:
        green = get_inverse_percent(medium_threshold, max_distance, distance)
    led.set_red_intensity(red)
    led.set_green_intensity(green)
    led.set_blue_intensity(blue)

    count += 1

    # Print value every second
    if count % 20 == 0:
        print(distance)
    sleep(0.05)



GPIO.cleanup()
