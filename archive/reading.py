

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
#specify which channel of the MCP3008 we are using
channel = AnalogIn(mcp, MCP.P0)
print("start")


signal_frequency = 80  #Hz
num_samples = 100

# Calculate the sleep duration based on the MCP sampling rate
sleep_duration = 0.000000005  #(1/(signal_frequency*num_samples))

i = 0
j = 0
voltage_samples = []

start_time = time.time()  # Record the start time

while i < num_samples:
    voltage = channel.voltage
    voltage_samples.append(voltage)
    time.sleep(sleep_duration)
    i += 1

end_time = time.time()  # Record the end time
total_time = end_time - start_time

while j < len(voltage_samples):  # Fix the loop condition
    print(voltage_samples[j])
    j += 1

print(f"Finished collecting data in {total_time:4f} seconds.")
num_period = (total_time/(1/signal_frequency))
print("number of periods is: ", num_period)


