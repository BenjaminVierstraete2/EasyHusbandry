from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens
    @staticmethod
    def read_last_sensors_temp():
        sql = "SELECT * FROM tblreads Where sensorID = 1 ORDER BY readID DESC LIMIT 1"
        return Database.get_rows(sql)
    @staticmethod
    def read_last_sensors_light():
        sql = "SELECT * FROM tblreads Where sensorID = 2 ORDER BY readID DESC LIMIT 1"
        return Database.get_rows(sql)
    @staticmethod
    def read_last_sensors_hum():
        sql = "SELECT * FROM tblreads Where sensorID = 3 ORDER BY readID DESC LIMIT 1"
        return Database.get_rows(sql)
    @staticmethod
    def read_status_fan():
        sql = "SELECT changedState FROM tblstatus WHERE actuatorID = 1 ORDER BY statusID DESC LIMIT 1"
        return Database.get_rows(sql)
    @staticmethod
    def read_status_lamp():
        sql = "SELECT changedState FROM tblstatus WHERE actuatorID = 2 ORDER BY statusID DESC LIMIT 1"
        return Database.get_rows(sql)
    

    @staticmethod
    def create_read(sensorID, timeRead, value):
        sql = "INSERT INTO tblreads (readID, sensorID, timeRead, value) VALUES (NULL,%s,%s,%s)"
        params = [sensorID, timeRead, value]
        return Database.execute_sql(sql, params)
    @staticmethod
    def change_status(statusChange,changedState,actuatorID):
        sql = "INSERT INTO tblstatus (statusID, statusChange,changedState,actuatorID) VALUES (NULL,%s,%s,%s)"
        params = [statusChange,changedState,actuatorID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_settings():
        sql = "SELECT * FROM settings ORDER BY settingID DESC LIMIT 1"
        return Database.get_rows(sql)
    @staticmethod
    def read_settings_row(row):
        sql = f"SELECT {row} FROM settings ORDER BY settingID DESC LIMIT 1"
        return Database.get_rows(sql)
    

    @staticmethod
    def create_settings(tempMet,minTemp,minLight,minHum,maxTemp,maxHum,fan,lamp,start,end):
        sql = "INSERT INTO settings (settingID, tempMet,minTemp,minLight,minHum,maxTemp,maxHum,fan,lamp,startTime,endTime)VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = [tempMet,minTemp,minLight,minHum,maxTemp,maxHum,fan,lamp,start,end]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_by_minute(sensorId):
        sql = f"SELECT timeRead,value FROM tblreads where sensorID = {sensorId}  GROUP BY DATE_FORMAT(timeRead, '%Y-%m-%d %H:%i:00') ORDER BY readID desc LIMIT 30"
        return Database.get_rows(sql)