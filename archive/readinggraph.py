import busio
import digitalio
import board
import time
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import matplotlib.pyplot as plt

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.OUT)

# Initialize MCP3008 ADC
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)

# Create lists to store data for plotting
timestamps = []
voltages = []

# Set up the plot
plt.ion()  # Enable interactive mode for real-time plotting
fig, ax = plt.subplots()
line, = ax.plot([], [], label='ADC Voltage')
ax.set_xlabel('Time')
ax.set_ylabel('ADC Voltage (V)')
ax.legend()

try:
    while True:
        # Read ADC values
        raw_value = channel.value
        voltage = channel.voltage

        # Update the lists
        timestamps.append(time.time())
        voltages.append(voltage)

        # Update the plot
        line.set_xdata(timestamps)
        line.set_ydata(voltages)
        plt.draw()
        plt.pause(0.1)  # Adjust the pause time as needed

        # Control GPIO based on ADC voltage
        if voltage > 2.0:
            GPIO.output(8, True)
        else:
            GPIO.output(8, False)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  # Clean up GPIO on script exit