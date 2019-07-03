"""
Create a primitive range finder. We use a ultrasonic distance sensor to
find distance and then use a RGB LED to show approximately how close things 
are:

Bright Red - very close
Not so Bright Red - close
Bright Blue - Medium Close
Bright Green - Far

Brightness dims for each category as we get further away.
"""
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
import rgb_led
from time import sleep

GPIO.setmode(GPIO.BCM)

near_threshold = 1.0
medium_threshold = 3.0
max_distance = 10.0


r_io_pin = 4
g_io_pin = 5
b_io_pin = 6

ultrasonic_echo = 21
ultrasonic_trigger = 20

ultrasonic = DistanceSensor(echo=ultrasonic_echo,trigger=ultrasonic_trigger,max_distance=10.0)

led = rgb_led.RgbLed(r_io_pin,g_io_pin,b_io_pin)

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
