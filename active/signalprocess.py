import busio
import digitalio
import board
import numpy as np
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
#import matplotlib.pyplot as plt

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
#specify which channel of the MCP3008 we are using
channel = AnalogIn(mcp, MCP.P0)
print("start")


# total number of samples you want to collect
num_samples = 500

# number of samples acquired per second
sample_rate = 1000
#time step
time_step = 1/sample_rate
#signal duration
signal_duration = num_samples/sample_rate

i = 0

j = 0
voltage_samples = []

start_time = time.time()  # Record the start time


while i < num_samples:
    voltage = channel.voltage
    voltage_samples.append(voltage)
    #making sure we collect at desired rate
    time.sleep(time_step)
    i += 1

end_time = time.time()  # Record the end time
total_time = end_time - start_time

# Generate the time axis on graph
time_axis = np.linspace(0, total_time, num_samples)

while j < len(voltage_samples):
    print(voltage_samples[j])
    j += 1

X = np.fft.fft(voltage_samples)
X_mag = np.abs(X)
frequency_axis = np.fft.fftfreq(num_samples, d=time_step)
# Exclude the DC component before finding the peak
DC_index = 0  # Index of DC component is 0
X_mag_no_DC = X_mag.copy()
X_mag_no_DC[DC_index] = 0  # Set the DC component to zero before finding the peak
Amp_Position = X_mag_no_DC.argmax()
peak_freq = frequency_axis[Amp_Position]
answer = abs(peak_freq/1.55)


print("end")
print("Dominant Freq: ", answer)
