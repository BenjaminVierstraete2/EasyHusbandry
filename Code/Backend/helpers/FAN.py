from RPi import GPIO
from repositories.DataRepository import DataRepository
from datetime import datetime

class FAN:
    def __init__(self,pin):
        self.temp = 0
        self.pin = pin
        self.setup()
        self.oldstatus = 0
        self.status = DataRepository.read_status_fan()[0].get("changedState")
        self.overwrite()
        

    def setup(self):
        GPIO.setup(self.pin,GPIO.OUT)
        

    def overwrite(self):
        value = str(DataRepository.read_settings_row("fan")[0].get('fan'))
        if value == "Auto":
            self.auto = True
        elif value == "Off":
            self.auto = False
            self.status = 0
        elif value == "On":
            self.auto = False
            self.status = 1


    def hyst(self):
        if DataRepository.read_settings_row('tempMet')[0].get('tempMet') == "c":
            self.max = DataRepository.read_settings_row("maxTemp")[0].get("maxTemp")
            if self.auto == True:
                if self.temp > self.max:
                    self.status = 1
                elif self.temp < (self.max -3):
                    self.status = 0
            self.fan_toggle()
        elif DataRepository.read_settings_row('tempMet')[0].get('tempMet') == "f":
            self.max = (DataRepository.read_settings_row("maxTemp")[0].get("maxTemp") -32)/1.8
            if self.auto == True:
                if self.temp > self.max:
                    self.status = 1
                elif self.temp < (self.max -3):
                    self.status = 0
            self.fan_toggle()

    def force_fan(self):
        self.status = 0
        self.fan_toggle()  

    def fan_toggle(self):
        if self.status == 0:
            GPIO.output(self.pin,GPIO.LOW)
        elif self.status == 1:
            GPIO.output(self.pin,GPIO.HIGH)
        self.send_status()

    def send_status(self):
        if self.status != self.oldstatus:
            self.oldstatus = self.status
            DataRepository.change_status(datetime.now().replace(microsecond=0),self.status,1)




