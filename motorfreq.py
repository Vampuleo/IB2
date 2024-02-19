import busio
import digitalio
import board
import numpy as np


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
#motor GPIO 17
GPIO.setup(17, GPIO.OUT)
GPIO.setup(17,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(17, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               #
print("check")
i = 0
j = 0
num_samples = 10
voltage_samples = []
fft_result = []
fft_freq = []
average_frequency = 0
max_amplitude_index = []

while i <= 1000:
    if 2.8 >= channel.voltage >= 0.8:

        if j < 9:
            # Collecting samples
            voltage_samples.append(channel.voltage)
            j += 1
        else:
            # Performing FFT
            fft_result = np.fft.fft(voltage_samples)
            fft_freq = np.fft.fftfreq(num_samples, d=0.01)

            # Find the maximum amplitude index
            max_amplitude_index = np.argmax(np.abs(fft_result))
            # Get the dominant frequency
            dominant_frequency = fft_freq[max_amplitude_index]
            print(dominant_frequency)

            # Reset counters and clear the sample array
            j = 0
            voltage_samples.clear()

    time.sleep(0.01)
    i += 1

print("Finished")


# while True:
#     # print('Raw ADC Value: ', channel.value)
#     # print('ADC Voltage: ' + str(channel.voltage))
#     if channel.voltage > 1.8:
#         print('ADC Voltage: ' + str(channel.voltage))
#         GPIO.output(8, True)
#         #if voltage > 2, set to HIGH state, means that voltage applied to output
#         p.ChangeDutyCycle(3)
#         time.sleep(0.5)# Changes the pulse width to 3 (so moves the servo)
#         p.ChangeDutyCycle(12)
#         time.sleep(0.5)
#     else:
#         GPIO.output(8, False)
#         #means voltage not applied to pin 8
#
#     time.sleep(0.01)
#
# print("finished")