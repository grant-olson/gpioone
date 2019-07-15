from gpioone import * 
from time import sleep
from datetime import datetime
            
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    
    s = SetupExample(help="""Drive a motor such as the infamous 28BYJ-48 hooked up via a ULN2003.""")

    s.rv("M1", "First Pin")
    s.rv("M2", "Second Pin")
    s.rv("M3", "Third Pin")
    s.rv("M4", "Fourth Pin")

    s.rv("STEPS", "Number of steps per revolution. The internet is all over the place for the 28BYJ-48, listing 4096,2038/etc, but mine takes 513")
    s.setup()
    

    stepper = Stepper(s.STEPS,s.M1,s.M2,s.M3,s.M4, rpm=15)

    try:
        print("15 RPM")
        print("Starting 90 degrees: %s" % datetime.now())
        stepper.degrees(90)
        print("Done with 90 degrees: %s" % datetime.now())
        sleep(1)
        print("Starting 360 degrees ccw: %s" % datetime.now())
        stepper.degrees(-360)
        print("Done with 360 degrees ccw: %s" % datetime.now())
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
