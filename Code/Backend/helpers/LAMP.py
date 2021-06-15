from RPi import GPIO
from werkzeug import datastructures
from repositories.DataRepository import DataRepository
from datetime import datetime

class Lamp:
    def __init__(self,pin):
        self.light = 0
        self.pin = pin
        self.setup()
        self.oldstatus = 0
        self.status = DataRepository.read_status_lamp()[0].get("changedState")
        self.overwrite()

    def setup(self):
        GPIO.setup(self.pin,GPIO.OUT)

    def overwrite(self):
        value = str(DataRepository.read_settings_row("lamp")[0].get('lamp'))
        if value == "Auto":
            self.auto = True
        elif value == "Off":
            self.auto = False
            self.status = 0
        elif value == "On":
            self.auto = False
            self.status = 1

    def checkTime(self):
        minTime = int(str(DataRepository.read_settings_row("startTime")[0].get("startTime")).replace(':',''))
        maxTime = int(str(DataRepository.read_settings_row("endTime")[0].get("endTime")).replace(':',''))
        timeAtm = int(str(datetime.now())[11:16].replace(':',''))+ 100
        if self.auto == True:
            if timeAtm in range(minTime,maxTime):
                self.hyst()
            else:
                self.force_lamp()

    def hyst(self):
        self.min = DataRepository.read_settings_row("minLight")[0].get("minLight")
        if self.auto == True:
            if self.light < self.min:
                self.status = 1
            elif self.light > (self.min + 10):
                self.status = 0
        self.lamp_toggle()

    def force_lamp(self):
        self.status = 0
        self.lamp_toggle()  

    def lamp_toggle(self):
        if self.status == 1:
            GPIO.output(self.pin,GPIO.LOW)
        elif self.status == 0:
            GPIO.output(self.pin,GPIO.HIGH)
        self.send_status()

    def send_status(self):
        if self.status != self.oldstatus:
            self.oldstatus = self.status
            DataRepository.change_status(datetime.now().replace(microsecond=0),self.status,2)




