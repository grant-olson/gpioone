import RPi.GPIO as GPIO
from time import sleep

class Stepper:
    """
    Drive a bipolar stepper via a ULN2003. The ULN2003 chip takes the low power from GPIO
    pins and turns it in to high power that drives the motor, while keeping the power isolated.
    Note that it acts as an Inverter, so when we set a GPIO pin to HIGH, it actually goes
    LOW to the motor driver.
    """
    def __init__(self,steps_per_revolution,one,two,three,four,rpm=1):
        self.steps_per_revolution = float(steps_per_revolution)
        self.pins = [one, two, three, four]

        # Half Step
        self.states = [(1,0,0,0),
          (1,1,0,0),
          (0,1,0,0),
          (0,1,1,0),
          (0,0,1,0),
          (0,0,1,1),
          (0,0,0,1),
          (1,0,0,1)]

        self.reverse_states = self.states[:]
        self.reverse_states.reverse()

        self.rpm = rpm
        
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def sleep_time(self):
        seconds_per_revolution = 60.0 / self.rpm
        microsteps_per_revolution = self.steps_per_revolution * len(self.states)
        return seconds_per_revolution / microsteps_per_revolution

    def steps(self,total_steps,clockwise=True):
        if clockwise:
            current_states = self.states
        else:
            current_states = self.reverse_states

        for i in range(total_steps):
            for state in current_states:
                for pin,state in zip(self.pins, state):
                    GPIO.output(pin, state)
                sleep(self.sleep_time())
    
    def degrees(self, degrees, clockwise=True):
        if degrees < 0:
            degrees = - degrees
            clockwise = not clockwise
            
        step_angle = 360.0 / self.steps_per_revolution
        angle_steps = float(degrees) / step_angle
        
        self.steps(int(angle_steps))

