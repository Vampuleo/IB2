# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout
GPIO.setwarnings(False)

# Set up pin 11 for PWM
GPIO.setup(11,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(11, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               # Starts running PWM on the pin and sets it to 0

flagOn = True
flagTurn = True
def getFrequency():
    frequency = int(input('Enter Frequency:'))
    flagTurn = True
    time = abs((frequency-80)/20)
    turnMotor(frequency, time)

def turnMotor(freq, time):
    if freq < 75:
        p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
        sleep(time)
        p.ChangeDutyCycle(0)
        getFrequency()
    elif freq > 85:
        p.ChangeDutyCycle(12)
        sleep(time)
        p.ChangeDutyCycle(0)
        getFrequency()
    else:
        getFrequency()

getFrequency()


# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults