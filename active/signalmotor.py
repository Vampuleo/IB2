import sys
import busio
import digitalio
import board
import numpy as np
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
# import matplotlib.pyplot as plt
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep  # Imports sleep (aka wait or pause) into the program

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
# specify which channel of the MCP3008 we are using
channel = AnalogIn(mcp, MCP.P0)

GPIO.setmode(GPIO.BCM)  # Sets the pin numbering system to use the physical layout
GPIO.setwarnings(False)
# Set up pin 11 for PWM
GPIO.setup(11, GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(11, 50)  # Sets up pin 11 as a PWM pin
p.start(0)  # Starts running PWM on the pin and sets it to 0

flagOn = True
flagTurn = True


def getFrequency():
    # total number of samples you want to collect
    num_samples = 500

    # number of samples acquired per second
    sample_rate = 1000
    # time step
    time_step = 1 / sample_rate
    # signal duration
    signal_duration = num_samples / sample_rate

    i = 0

    j = 0
    voltage_samples = []

    start_time = time.time()  # Record the start time

    while i < num_samples:
        voltage = channel.voltage
        voltage_samples.append(voltage)
        # making sure we collect at desired rate
        time.sleep(time_step)
        i += 1

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time

    # Generate the time axis on graph
    time_axis = np.linspace(0, total_time, num_samples)

    while j < len(voltage_samples):
        #print(voltage_samples[j])
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
    answer = abs(peak_freq / 1.55)
    return answer


def turnMotor(freq, time):
    if getFrequency() < freq - 2:
        p.ChangeDutyCycle(3)  # Changes the pulse width to 3 (so moves the servo)
        sleep(time)
        p.ChangeDutyCycle(0)

    elif getFrequency() > freq + 2:
        p.ChangeDutyCycle(12)
        sleep(time)
        p.ChangeDutyCycle(0)

    else:
        print("success")


user_input = input("Please enter desired Freq: ")
print(f"You entered: {user_input}")
user_input_int = int(user_input)
current_freq = getFrequency()
while current_freq < user_input_int - 2 or current_freq > user_input_int + 2:
    turnMotor(user_input_int, 0.3)
    current_freq = getFrequency()
    print("current freq: ", current_freq)

