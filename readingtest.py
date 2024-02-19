import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# 初始化 SPI 总线
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# 选择通道
channel = AnalogIn(mcp, MCP.P0)

# 读取频率
frequency = 40  # Hz
interval = 1.0 / frequency
num_samples = 1000

print("Start sampling")

# 读取数据
for i in range(num_samples):
    value = channel.value
    print(value)
    time.sleep(interval)

print("Sampling complete")