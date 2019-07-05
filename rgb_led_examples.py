import RPi.GPIO as GPIO
from gpioone import *

if __name__ == "__main__":
    s = SetupExample(help="""Simple examples with RGB LEDs.

It will first turn on the LEDs one by one, then enter a color cycle mode that uses software PWM to create a glowing light.
""")
    s.rv("RED", "Red Pin")
    s.rv("GREEN", "Green Pin")
    s.rv("BLUE", "Blue Pin")

    s.setup()
    
    GPIO.setmode(GPIO.BCM)
    rgb_led = RgbLed(s.RED,s.GREEN,s.BLUE)
    
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

