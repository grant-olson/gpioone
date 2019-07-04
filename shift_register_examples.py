import RPi.GPIO as gpio
from gpioone import *

def led_strip_example(shift_register):
    # Example is hooked up to 8 LEDs with 220 Ohm resistors between
    # anode and Shift Register pins.

    sleep_time = 0.025
    # Count to 255 displaying binary
    for i in range(0,256):
        shift_register.number(i)
        sleep(sleep_time)
    
    # As a demonstration of actual shifting, we only load one bit at a time
    # and trigger the latch. One out of every seven bits is high, so
    # it looks like the light moves down the line of LEDs
    while 1:
        shift_register.high()
        shift_register.clock_tick()
        shift_register.trigger_latch()
        sleep(sleep_time)
        shift_register.low()
        for i in range(0,7):
            shift_register.clock_tick()
            shift_register.trigger_latch()
            sleep(sleep_time)

def segment_example(shift_register):
    for i in range(0,10):
        if i % 2:
            shift_register.number(SegmentDisplay.value(str(i)))
        else:
            shift_register.number(SegmentDisplay.value(str(i), decimal_point=True))
        sleep(0.5)

    counter = 0
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXZY":
        counter += 1
        shift_register.character(c, decimal_point=(counter / 2))
        sleep(0.5)

    shift_register.number(0)


def multi_segment_example(shift_register):
    """
    Use four IO pins to control a 4 digit seven segment display.

    TODO: Chain two shift registers together for the slot control
    logic to free the pins back up.
    """
    first = 18
    second = 19
    third = 23
    fourth = 24

    #19, 18 ,23, 25
    GPIO.setup(first, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(second, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(third, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(fourth, GPIO.OUT, initial=GPIO.HIGH)

    sleep_time = 0.001

    text = "DANGER!!! DO NOT EAT... "
    while True:
        for i in range(100):
            shift_register.character(text[0])
            GPIO.output(first, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(first, GPIO.HIGH)

            shift_register.character(text[1])
            GPIO.output(second, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(second, GPIO.HIGH)#

            shift_register.character(text[2])
            GPIO.output(third, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(third, GPIO.HIGH)

            shift_register.character(text[3])
            GPIO.output(fourth, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(fourth, GPIO.HIGH)

        text = text[1:] + text[0]
    
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    latch = 20 # 21
    clock = 16 # 20
    data = 21 # 16
    
    shift_register = ShiftRegister(data, clock, latch)
    multi_segment_example(shift_register)
    GPIO.cleanup()
