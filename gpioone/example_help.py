from os import environ
from collections import OrderedDict
import sys

class SetupExample:
    def __init__(self, help=None):
        self.required_vars = OrderedDict()
        self.optional_vars = OrderedDict()
        self.help = help

    def required_var(self, var, desc):
        self.required_vars[var] = desc

    def rv(self, var, desc):
        self.required_var(var, desc)

    def optional_var(self, var, desc):
        self.optional_vars[var] = desc

    def ov(self, var, desc):
        self.optional_var(var, desc)

    def has_var(self, var):
        return hasattr(self, var)
        
    def setup(self):
        for var in self.optional_vars.keys():
            if var in environ:
                value = environ[var]
                setattr(self, var, int(value))
        for var in self.required_vars.keys():
            if var in environ:
                value = environ[var]
                setattr(self, var, int(value))
            else:
                print("Couldn't find required environment setting fo %s pin." % var)
                print("")
                if self.help:
                    print(self.help)
                print("These are the required settings which should correspond to pins on devices:")
                print("")
                for var, desc in self.required_vars.items():
                    print("    %s - %s" % (var, desc))
                for var, desc in self.optional_vars.items():
                    print("    %s - %s [OPTIONAL]" % (var, desc))
                print("")
                print("Example Usage:")
                print("")
                example_string = "    "
                for i, v in enumerate(self.required_vars.keys()):
                    example_string += "%s=%d " % (v, i + 1)
                example_string += "%s" % sys.argv[0]
                print(example_string)
                print("")
                sys.exit(1)
