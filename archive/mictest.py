#!/usr/bin/env python3

# from gpiozero import LED
# import sounddevice as sd

# from gpiozero import MCP3008
#
# print("gpiozero version:", MCP3008.gpiozero_version)
#
# mic = MCP3008(channel=0)
#
# try:
#     while True:
#         voltage = mic.value * mic.reference_voltage
#         print("Voltage:", voltage)
# except KeyboardInterrupt:
#     pass
#
#
#
# adc_channel = 0  # Adjust the channel based on your ADC configuration
# mic = MCP3008(channel=adc_channel)
#
# try:
#     while True:
#         voltage = mic.value * mic.reference_voltage
#         print("Voltage:", voltage)
#         time.sleep(0.5)
#
# except KeyboardInterrupt:
#     pass
#
# print("Hello World")


from gpiozero import InputDevice
import time

input_pin = InputDevice(9)

try:
    while True:
        voltage = input_pin.value
        print(voltage)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program terminated by user.")
