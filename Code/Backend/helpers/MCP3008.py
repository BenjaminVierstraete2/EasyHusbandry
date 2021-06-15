import spidev
import time

class Mcp:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 10 ** 5
        time.sleep(0.1)

    def read_channel(self, ch):
        channel = ch << 4 | 128
        bytes_out = [0b00000001, channel, 0b00000000]
        bytes_in = self.spi.xfer2(bytes_out)
        byte1 = bytes_in[1]
        byte2 = bytes_in[2]
        result = byte1 << 8 | byte2
        return result

    def read_sensor(self, value):
        if value == 0:
            return self.read_channel(0)
        if value == 1:
            return self.read_channel(1)

    def read_light(self):
        value = self.read_channel(0)
        brightness = round(100-(value *100/1023),2)
        return brightness

    def close_spi(self):
        self.spi.close()
mcp = Mcp()

