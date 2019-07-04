from gpiozero import DistanceSensor
from time import sleep

class Ultrasonic:
    """
    Simple interface. Get distance, send to reporter.
    """
    def __init__(self, echo_pin, trigger_pin, max_distance, reporter):
        self.ultrasonic = DistanceSensor(echo=echo_pin,trigger=trigger_pin,max_distance=max_distance)
        self.reporter = reporter

    def run(self):
        count = 0

        while True:
            distance = self.ultrasonic.distance
            self.reporter.report(distance)
            count += 1

            # Print value every second
            if count % 20 == 0:
                print("%0.2f meter" % distance)
            sleep(0.05)
