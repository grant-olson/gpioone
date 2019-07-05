try:
    import gpioone
except ImportError:
    import os, sys
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "../")
    sys.path.append(path)
    import gpioone
