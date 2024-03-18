import busio
import digitalio
import board
import numpy as np
import time
import socket
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program


# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
#
# GPIO.setup(11,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
# GPIO.setup(16, GPIO.OUT)
# p = GPIO.PWM(11, 50)     # Sets up pin 11 as a PWM pin
# p.start(0)


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
# specify which channel of the MCP3008 we are using
channel = AnalogIn(mcp, MCP.P0)
print("start")

# total number of samples you want to collect
num_samples = 500

# number of samples acquired per second
sample_rate = 1000
# time step
time_step = 1 / sample_rate
# signal duration
signal_duration = num_samples / sample_rate


import time
import numpy as np
# Make sure to import or define 'channel' and other necessary modules and variables here

def infiniteLoop():
    i = 0
    j = 0
    voltage_samples = []

    start_time = time.time()  # Record the start time

    while i < num_samples:
        voltage = channel.voltage
        voltage_samples.append(voltage)
        # making sure we collect at the desired rate
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
    print(answer)

    return answer

host = '0.0.0.0'  # Allows connections from other computers
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print("Server listening on port:", port)

    while True:  # Continuously listen for connections
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            try:
                while True:  # Loop to continuously send data
                    answer = infiniteLoop()
                    message = str(answer) + '\n'  # Ensure the message ends with a newline character
                    message = message.encode()  # Encode the message as bytes
                    conn.sendall(message)
                    # Optional: Wait for an acknowledgment if necessary
                    # ack = conn.recv(1024)
            except Exception as e:
                print('Connection closed or error occurred:', e)
            finally:
                conn.close()