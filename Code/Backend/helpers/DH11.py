from RPi import GPIO
import time

class DHT11:
    def __init__(self, DHT11_pin):
        self.DHT11_pin = DHT11_pin
        self.humidity = 0
        self.temperature = 0
        self.error_DHT = False
        self.data_count = 43
        self.data_count_found = 0
        self.data = [0] * self.data_count
        self.result_bytes = [0] * 5

    def reset_values(self):
        self.humidity = 0
        self.temperature = 0
        self.error_DHT = False 
        self.data = [0] * self.data_count
        self.result_bytes = [0] * 5
        self.data_count_found = 0

    def read_pin(self):
        return GPIO.input(self.DHT11_pin)


    def init_DHT11(self):
        GPIO.setup(self.DHT11_pin, GPIO.OUT)
        GPIO.output(self.DHT11_pin,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(self.DHT11_pin,GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(self.DHT11_pin,GPIO.HIGH)
        GPIO.setup(self.DHT11_pin, GPIO.IN, GPIO.PUD_UP)

    def read_bits_DHT11(self):
        last_time = time.time()
        current_time = last_time
        can_DHT = True
        count = 0
        while count < self.data_count and (current_time - last_time) < 0.1:
            current_time = time.time()
            is_high = self.read_pin()
            if is_high == 0 and can_DHT == True:
                can_DHT = False
                current_time = time.time()
                self.data[count]=(current_time - last_time)
                count += 1
                last_time=time.time()
            if is_high == 1:
                can_DHT = True
        self.data_count_found = count

    def time_to_bits(self):
        for i in range(0, 40):
            index = i + 3
            if self.data[index] <= 0.0001:
                self.data[index] = 0
            else:
                self.data[index] = 1

    def bits_to_bytes(self):
        for byte_count in range(0, 5):
            byte = 0
            for index in range(0, 8): 
                if index < 7:
                    byte = byte << 1
                bit = int(self.data[index + byte_count * 8 + 3])
                byte = byte | bit
            self.result_bytes[byte_count] = byte

    def check_sum(self):
        sum_bytes = self.result_bytes[0] + self.result_bytes[1] + self.result_bytes[2] + self.result_bytes[3]
        sum_bytes = sum_bytes & 255
        check_sum = self.result_bytes[4]
        if sum_bytes == check_sum and self.data_count_found > 0:
            self.error_DHT = False
            self.humidity = int(self.result_bytes[0]) + int(self.result_bytes[1]) / 100
            self.temperature = int(self.result_bytes[2]) + int(self.result_bytes[3]) / 100
        else:
            self.error_DHT = True


   
    def read_humidity(self):
        self.init_DHT11()
        self.read_bits_DHT11()
        self.time_to_bits()
        self.bits_to_bytes()
        self.check_sum()
        hum = 0
        if self.error_DHT == False:
            hum = self.humidity
        self.reset_values()
        return hum
