from RPi import GPIO
import time

class LCD:
    def __init__(self):
        self.bits = [18,12,25,24,23,26,17,13]
        self.setup()
        self.rs = 21
        self.enable = 20
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)
        time.sleep(0.1)
        self.init_LCD()
        self.lcdStatus = 0

    def setup(self):
        for i in self.bits:
            GPIO.setup(i, GPIO.OUT)

    def send_instruction(self, value):
        GPIO.output(self.rs, GPIO.LOW)
        GPIO.output(self.enable, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(self.enable, GPIO.LOW)
        time.sleep(0.01)


    def send_character(self, character):
        GPIO.output(self.rs, GPIO.HIGH)
        GPIO.output(self.enable, GPIO.HIGH)
        self.set_data_bits(character)
        GPIO.output(self.enable, GPIO.LOW)
        time.sleep(0.01)

    def set_data_bits(self, byte):
        mask = 0x80
        for i in range(8):
            GPIO.output(self.bits[i], byte & (mask >> i))

    def write_message(self, message):
        for char in message[0:16]:
            self.send_character(ord(char))
        for char in message[16:]:
            self.scroll_screen()
            self.send_character(ord(char))

    def init_LCD(self):
        self.send_instruction(0b00111000)
        self.send_instruction(0b00001100)
        self.send_instruction(0b00000001)

    def set_cursor(self, row, col):
        byte = row << 6 | col
        self.send_instruction(byte | 128)

    def scroll_screen(self):
        self.send_instruction(0b00011000)
        time.sleep(0.2)
    
    def clear(self):
        self.send_instruction(0b00000001)

    def toggle(self):
        if self.lcdStatus < 2:
            self.lcdStatus += 1
        elif self.lcdStatus >= 2:
            self.lcdStatus = 0



