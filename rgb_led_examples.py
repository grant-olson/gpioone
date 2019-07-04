import RPi.GPIO as GPIO
from gpioone import *

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    rgb_led = RgbLed(4,5,6)
    
    sleep(1)

    print("TURNING BLUE ON")
    rgb_led.set_blue_state(GPIO.HIGH)
    sleep(1)
    
    print("TURNING GREEN ON")

    rgb_led.set_blue_state(GPIO.LOW)
    rgb_led.set_green_state(GPIO.HIGH)
    sleep(1)

    print("TURNING RED ON")
    rgb_led.set_green_state(GPIO.LOW)
    rgb_led.set_red_state(GPIO.HIGH)
    sleep(1)

    rgb_led.set_red_state(GPIO.LOW)

    rgb_led.start_intensity_mode()
    print("Starting intensity cycle mode. Press Ctrl-C to stop...")
    sleep(1)

    try:
        while True:
            rgb_led.cycle_intensity()
            sleep(0.01)
    except KeyboardInterrupt:
        print("Stopping and cleaning up.")

    rgb_led.stop_intensity_mode()

    GPIO.cleanup()

