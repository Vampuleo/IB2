import busio
import digitalio
import board


import mcp3008 as MCP
import time
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(8,  GPIO.OUT)
#motor GPIO
GPIO.setup(17, GPIO.OUT)
GPIO.setup(17,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(17, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               #

while True:
    # print('Raw ADC Value: ', channel.value)
    # print('ADC Voltage: ' + str(channel.voltage))
    if channel.voltage > 1.8:
        print('ADC Voltage: ' + str(channel.voltage))
        GPIO.output(8, True)
        #if voltage > 2, set to HIGH state, means that voltage applied to output
        p.ChangeDutyCycle(3)
        time.sleep(0.5)# Changes the pulse width to 3 (so moves the servo)
        p.ChangeDutyCycle(12)
        time.sleep(0.5)
    else:
        GPIO.output(8, False)
        #means voltage not applied to pin 8

    time.sleep(0.01)