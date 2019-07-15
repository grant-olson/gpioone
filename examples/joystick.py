from gpioone import * 
from time import sleep

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    s = SetupExample(help="""Read an analog joystick via MCP300x chip.""")

    s.rv("CHIP_SELECT", "Chip select pin")
    s.rv("X_PIN", "Pin for X axis, on ADC NOT GPIO.")
    s.rv("Y_PIN", "Pin for X axis, on ADC NOT GPIO.")
    s.ov("BUTTON", "Joystick Button pin. GPIO BOARD NOT ADC.")
    
    s.setup()
    
    mcp = MCP3008(s.CHIP_SELECT)

    if s.has_var("BUTTON"):
        joystick = Joystick(mcp, s.X_PIN, s.Y_PIN, s.BUTTON)
    else:
        joystick = Joystick(mcp, s.X_PIN, s.Y_PIN)
        
        
    while 1:
        x = joystick.x()
        y = joystick.y()
        angle = joystick.angle()
        print("X: %f, Y: %f Angle: %s Dir: %s  Button: %s" % (x,y,angle, joystick.direction(), joystick.button()))
        sleep(1)
