import RPi.GPIO as GPIO
try:
    from gpioone import *
except ImportError:
    import os, sys
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "../")
    sys.path.append(path)
    from gpioone import *

