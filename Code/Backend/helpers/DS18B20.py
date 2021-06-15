from repositories.DataRepository import DataRepository

class DS18B20:

    def __init__(self, par_sensorid):
        self.filepath = f'/sys/bus/w1/devices/w1_bus_master1/{par_sensorid}/w1_slave'

    def give_temp(self):
        sensor_file = open(self.filepath, 'r') 
        for i,line in enumerate(sensor_file):
            if i ==1:
                templine = line.replace("\n","")[line.find("t=")+2:]
                temp = int(templine)/1000
        sensor_file.close()      
        return temp
            
            