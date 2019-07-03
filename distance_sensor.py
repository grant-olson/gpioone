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

while True:
    
    distance = ultrasonic.distance
    if distance <= 0.5:
        percent = distance / 0.5
        red = 100 - (percent * 100)
        if red < 20:
            red = 20
        green = 0
        blue = 0
    elif distance <= 1.0:
        red = 0
        blue = 100 - (distance / 1.0 * 100)
        if blue < 20:
            blue = 20
        green = 0
    else:
        red = 0
        blue = 0
        green = 100 - (distance / 2.0 * 100)
        if green < 20:
            green = 20
    led.set_red_intensity(red)
    led.set_green_intensity(green)
    led.set_blue_intensity(blue)

    count += 1

    if count % 20 == 0:
        print(distance)
    sleep(0.05)



GPIO.cleanup()
