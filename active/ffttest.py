import busio
import digitalio
import board
import numpy as np
from scipy import fftpack

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

#signal duration
signal_duration = num_samples/sample_rate

lower_frequency = 40
upper_frequency = 200

# Calculate the sleep duration based on the MCP sampling rate
sleep_duration = 1/sample_rate

i = 0

j = 0
voltage_samples = []

start_time = time.time()  # Record the start time

while i < num_samples:
    voltage = channel.voltage
    voltage_samples.append(voltage)
    time.sleep(1/sample_rate) #help pls
    i += 1

end_time = time.time()  # Record the end time
total_time = end_time - start_time

# Generate the time axis on graph
time_axis = np.linspace(0, total_time, num_samples)

while j < len(voltage_samples):
    print(voltage_samples[j])
    j += 1

# Find the indices corresponding to the lower and upper frequencies
lower_index = int(lower_frequency * num_samples / sample_rate)
upper_index = int(upper_frequency * num_samples / sample_rate)

X = np.fft.fft(voltage_samples)
X_mag = np.abs(X)/num_samples
# Calculate the frequency axis

# Filter the FFT result
X_filtered = np.zeros_like(X)
X_filtered[lower_index:upper_index] = X[lower_index:upper_index]


frequency_axis = np.fft.fftfreq(num_samples, d=1/sample_rate)

# Calculate the magnitude of the filtered FFT result
X_mag_filtered = np.abs(X_filtered) / num_samples

# Find the index corresponding to the maximum magnitude in the filtered result
dominant_frequency_index_filtered = np.argmax(X_mag_filtered[1:int(num_samples/2)])

dominant_frequency_index = np.argmax(X_mag[1:])

# Find the frequency corresponding to the maximum magnitude in the filtered result
dominant_frequency_filtered = np.abs(frequency_axis[dominant_frequency_index_filtered])
dominant_frequency = np.abs(frequency_axis[dominant_frequency_index])

print("Dominant Frequency: {} Hz".format(dominant_frequency))

print("Dominant Frequency (Filtered): {} Hz".format(dominant_frequency_filtered))

#
#Plotting
# fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
# ax1.plot(time_axis, voltage_samples)
# ax1.set_xlabel('Time (s)')
# ax1.set_ylabel('Voltage (V)')
# ax2.plot(X_mag)
# ax2.set_xlabel('Frequency')
# ax2.set_ylabel('Magnitude')
# plt.show()



