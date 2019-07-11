# This is a harness to run from source, if using the installed package use:
# from gpioone import *
from gpioone_setup import *

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


def multi_segment_example(shift_register, first, second, third, fourth):
    """
    Use four IO pins to control a 4 digit seven segment display.

    TODO: Chain two shift registers together for the slot control
    logic to free the pins back up.
    """
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

# This is a harness to run from source, if using the installed package use:
# from gpioone import *
from gpioone_setup import * 

if __name__ == "__main__":

    s = SetupExample(help="""This provides a few examples of using a shift register.

Don't forget to include resistors where appropriate on all LEDs!

Set LEDS to 1 to have the shift register display on 8 LEDs tied to outputs.

Set SEGMENT to 1 count up on a single seven-segment LED display.

Set MULTI_1 - MULTI_4 to display a multisegment LED Display with the GPIO pins
that toggle the active display.

Note on multi-segment setup, shift register outputs 0-6 map to LED outputs
A-G respectively. 7 maps to the DP LED. Consult a datasheet if you're not sure
which pins map to what segment.
""")

    s.rv("DATA", "Data Pin on Shift Register")
    s.rv("LATCH", "Latch Pin on Shift Register")
    s.rv("CLOCK", "Clock Pin on Shift Register")

    s.ov("LEDS", "Set to one to display binary count on 8 LEDs.")

    s.ov("SEGMENT", "Set to one to display on single digit seven segment LED.")
    
    s.ov("MULTI_1", "Multisegment LED Display Digit 1")
    s.ov("MULTI_2", "Multisegment LED Display Digit 2")
    s.ov("MULTI_3", "Multisegment LED Display Digit 3")
    s.ov("MULTI_4", "Multisegment LED Display Digit 4")
         
    
    s.setup()

    try:
        shift_register = ShiftRegister(s.DATA, s.CLOCK, s.LATCH)

        if s.has_var("MULTI_1"):
            multi_segment_example(shift_register, s.MULTI_1, s.MULTI_2, s.MULTI_3, s.MULTI_4)
        elif s.has_var("LEDS"):
            led_strip_example(shift_register)
        elif s.has_var("SEGMENT"):
            segment_example(shift_register)
        else:
            print("You didn't tell us where to send the Segment Register output!")
            
    except KeyboardInterrupt:
        pass

GPIO.cleanup()
