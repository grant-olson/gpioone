# GPIO One

GPIO One is an unofficial user-created set of modules to allow you to
easily use various input/output devices on your Raspberry Pi when the
default library and GPIOzero don't have any useful code. It hopes to
fill in some of the blanks that keep you from getting your projects up
and running quickly and smoothly.

It currently provides interfaces to:

* Three colored RGB Leds.
* Seven Segement LED displays such as single-element 5161AS and 4-element SH5461AS
* LCD Displays such as the 1602A
* Shift registers such as 74HC595
* Analog-to-Digital via the MCP3008/4 chip line. And built on top of the raw ADC, interfaces for:
    * Analog Joystick

## Examples

The example files use environment variables to set pins so that we
will not accidentally send something down the wrong pin and damage
equipment. So for example, if you have a Common-cathode RGB LED set up
with the Cathode tied to ground, and the Red, Green, and Blue pins to
GPIO 4, 5, and 6 (with a 220 Ohm Resistor in between each connection!)
then you can simply go to the examples directory,  run
`RED=4 GREEN=5 BLUE=6 python3 rgb_led.py` and the LED should come to life.

Each example can be run without environment variables for instructions and a description:

```
pi@raspberrypi:~/src/gpioone/examples $ python3 rgb_led.py 
Couldn't find required environment setting fo RED pin.

Simple examples with RGB LEDs.

It will first turn on the LEDs one by one, then enter a color cycle mode that uses software PWM to create a glowing light.

These are the required settings which should correspond to pins on devices:

    RED - Red Pin
    GREEN - Green Pin
    BLUE - Blue Pin

Example Usage:

    RED=1 GREEN=2 BLUE=3 python3 /home/pi/src/gpioone/gpioone/example_help.py

pi@raspberrypi:~/src/gpioone $ 

```

## Thanks

Gpioone was primarily written to help the author learn more about
interfacing various hardware with the Raspberry Pi. I have made
attempts to write clear, easy-to-follow code that should be generally
reusable. How useful this is to anyone else remains to be seen. Let me
know if you find it helpful!

- Grant
