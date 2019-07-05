from os import environ
from collections import OrderedDict
import sys

class SetupExample:
    def __init__(self, help=None):
        self.required_vars = OrderedDict()
        self.help = help

    def required_var(self, var, desc):
        self.required_vars[var] = desc

    def rv(self, var, desc):
        self.required_var(var, desc)
        
    def setup(self):
        for var in self.required_vars.keys():
            if var in environ:
                value = environ[var]
                globals()[var] = value
            else:
                print("Couldn't find required environment setting fo %s pin." % var)
                print("")
                if self.help:
                    print(self.help)
                print("These are the required settings which should correspond to pins on devices:")
                print("")
                for var, desc in self.required_vars.items():
                    print("    %s - %s" % (var, desc))
                print("")
                print("Example Usage:")
                print("")
                example_string = "    "
                for i, v in enumerate(self.required_vars.keys()):
                    example_string += "%s=%d " % (v, i + 1)
                example_string += "python3 %s" % __file__
                print(example_string)
                print("")
                sys.exit(1)
