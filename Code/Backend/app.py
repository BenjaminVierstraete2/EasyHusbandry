#imports
from logging import LogRecord
from repositories.DataRepository import DataRepository
import time
from RPi import GPIO
import threading
from datetime import datetime
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, json, jsonify, request
from helpers.DS18B20 import DS18B20
from helpers.MCP3008 import Mcp
from helpers.DH11 import DHT11
from helpers.FAN import FAN
from helpers.LAMP import Lamp
from helpers.LCD import LCD

#setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
humidity = DHT11(16)
oneWire = DS18B20('28-0300a279b15a')
mcp = Mcp()
fan = FAN(19)
lamp = Lamp(22)
lcd = LCD()

#FLASK SOCKETIO
endpoint='/api/v1'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sd64gg4dg64'

socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)
CORS(app)

@socketio.on_error()        
def error_handler(e):
    print(e)

@app.route('/')
def index():
    return "not api"

@app.route(endpoint+'/')
def api():
    return "API"

@app.route(endpoint + '/settings' , methods=['GET','POST'])
def settings():
    data = DataRepository.read_settings()
    if request.method == 'GET':
        if data is not None:
            return jsonify(settings=data),200
        else:
            return jsonify(status="error"),404
    elif request.method == 'POST':
        formdata = DataRepository.json_or_formdata(request)
        if formdata['tempMet'] == "°c":
            met = "c"
        elif formdata['tempMet'] == "°f":
            met = "f"
        
        
        if formdata['tempMin'] != "":
            tmin = formdata['tempMin']
        elif formdata['tempMin'] == "":
            tmin = DataRepository.read_settings_row("minTemp")[0].get('minTemp')

        if formdata['brightMin'] != "":
            lmin = formdata['brightMin']
        elif formdata['brightMin'] == "":
            lmin = DataRepository.read_settings_row("minLight")[0].get('minLight')

        if formdata['humMin'] != "":
            hmin = formdata['humMin']
        elif formdata['humMin'] =="":
            hmin = DataRepository.read_settings_row("minHum")[0].get('minHum')

        if formdata['tempMax'] != "":
            tmax = formdata['tempMax']
        elif formdata['tempMax'] == "":
            tmax = DataRepository.read_settings_row("maxTemp")[0].get('maxTemp')

        if formdata['humMax'] != "":
            hmax = formdata['humMax']
        elif formdata['humMax'] == "":
            hmax = DataRepository.read_settings_row("maxHum")[0].get('maxHum')
        
        f = formdata['fan']
        l = formdata['lamp']

        if formdata['from'] != "":
            strt = formdata['from']
        elif formdata['from'] == "":
            strt = DataRepository.read_settings_row("startTime")[0].get('startTime')

        if formdata['to'] != "":
            end = formdata['to']
        elif formdata['to'] == "":
            end = DataRepository.read_settings_row("endTime")[0].get('endTime')

        nieuwSetting = DataRepository.create_settings(met,tmin,lmin,hmin,tmax,hmax,f,l,strt,end)
        return jsonify(nieuwSetting),201
    else:
        return jsonify(message="wrong method")


#functions
def sensor_read_temp():
    threading.Timer(3,sensor_read_temp).start()
    temp = oneWire.give_temp()
    DataRepository.create_read(1, datetime.now().replace(microsecond=0),temp)

def sensor_read_light():
    threading.Timer(3,sensor_read_light).start()
    light = mcp.read_light()
    DataRepository.create_read(2, datetime.now().replace(microsecond=0),light)

def sensor_read_hum():
    threading.Timer(3,sensor_read_hum).start()
    hum = humidity.read_humidity()
    if hum > 0:
        DataRepository.create_read(3, datetime.now().replace(microsecond=0),hum)


def fan_func():
    threading.Timer(3,fan_func).start()
    fan.temp = oneWire.give_temp()
    fan.overwrite()
    fan.hyst()
    
    

def lamp_func():
    threading.Timer(3,lamp_func).start()
    lamp.light = mcp.read_light()
    lamp.overwrite()
    lamp.checkTime()

def tempcalc(): 
    if DataRepository.read_settings_row('tempMet')[0].get('tempMet') == "c":
            temp = str(round(oneWire.give_temp())) + "C"
    elif DataRepository.read_settings_row('tempMet')[0].get('tempMet') == "f":
        temp = str(round(oneWire.give_temp() * 1.8 + 32)) + "F" 
    return temp
   
def real_time_lcd():
    threading.Timer(6,real_time_lcd).start()
    lcd.clear()
    temp = tempcalc()
    light = mcp.read_light()
    hum = round(DataRepository.read_last_sensors_hum()[0].get('value'))
    lcd.toggle()
    if lcd.lcdStatus == 0:
        lcd.set_cursor(0,0)
        lcd.write_message(f"Temp: {temp}")
        lcd.set_cursor(1,0)
        lcd.write_message(f"Light: {light}%")
    elif lcd.lcdStatus == 1:
        lcd.set_cursor(0,0)
        lcd.write_message(f"Light: {light}%")
        lcd.set_cursor(1,0)
        lcd.write_message(f"Humidity: {hum}%")
    elif lcd.lcdStatus == 2:
        lcd.set_cursor(0,0)
        lcd.write_message(f"Humidity: {hum}%")
        lcd.set_cursor(1,0)
        lcd.write_message(f"Temp: {temp}")
    




#SOCKET IO

@socketio.on("connect")
def connect_message():
    time.sleep(0.1)
    socketio.emit("B2F_client_connected", broadcast=False)

#conditions page
@socketio.on("F2B_conditions_connected")
def post_temp():
    print("Conditions page loaded")
    if DataRepository.read_settings_row('tempMet')[0].get('tempMet') == "c":
        temp_atm = DataRepository.read_last_sensors_temp()[0].get("value")
    elif DataRepository.read_settings_row('tempMet')[0].get('tempMet') == "f":
        temp_atm = DataRepository.read_last_sensors_temp()[0].get("value") * 1.8 + 32
    metric = "°" + DataRepository.read_settings_row("tempMet")[0].get("tempMet")
    socketio.emit("B2F_temp_data", {"data": temp_atm, "metric": metric}, broadcast=True)
 
@socketio.on("F2B_temp_recieved")
def post_light():
    light_atm = DataRepository.read_last_sensors_light()
    for date in light_atm:
        time_data = date['timeRead'] = f"{date['timeRead'].day}/{date['timeRead'].month}/{date['timeRead'].year} {date['timeRead'].hour}:{date['timeRead'].minute}:{date['timeRead'].second}"
    socketio.emit("B2F_light_data", {"data": light_atm}, broadcast=True)

@socketio.on("F2B_light_recieved")
def post_hum():
    hum_atm = DataRepository.read_last_sensors_hum()
    for date in hum_atm:
        time_data = date['timeRead'] = f"{date['timeRead'].day}/{date['timeRead'].month}/{date['timeRead'].year} {date['timeRead'].hour}:{date['timeRead'].minute}:{date['timeRead'].second}"
    socketio.emit("B2F_hum_data", {"data": hum_atm}, broadcast=True)
 
@socketio.on("F2B_hum_recieved")
def post_fan():
    data = "null" 
    state = DataRepository.read_status_fan()[0].get("changedState")
    if state == 1:
        data = "On"
    elif state == 0:
        data = "Off"
    socketio.emit("B2F_fan_data", {"data": data}, broadcast=True)

@socketio.on("F2B_fan_recieved")
def post_lamp():
    data = "null" 
    state = DataRepository.read_status_lamp()[0].get("changedState")
    if state == 1:
        data = "On"
    elif state == 0:
        data = "Off"
    socketio.emit("B2F_lamp_data", {"data": data}, broadcast=True)

@socketio.on('F2B_lamp_recieved')
def settimer():
    socketio.emit("B2F_settimer",broadcast=True)


#stats page
@socketio.on("F2B_stats_connected")
def temp():
    print("History page loaded")
    timestamps = []
    data = []
    sqldata = DataRepository.read_by_minute(1)
    for i in range(30):
        minute = str(sqldata[i].get('timeRead'))[11:16]
        val = sqldata[i].get('value')
        timestamps.append(minute)
        data.append(val)
    socketio.emit("B2F_tempchart",{"time":timestamps[::-1],"data":data},broadcast=True)

@socketio.on("F2B_tempchart_recieved")
def hum():
    timestamps = []
    data = []
    sqldata = DataRepository.read_by_minute(3)
    for i in range(30):
        minute = str(sqldata[i].get('timeRead'))[11:16]
        val = sqldata[i].get('value')
        timestamps.append(minute)
        data.append(val)
    socketio.emit("B2F_humchart",{"time":timestamps[::-1],"data":data},broadcast=True)

@socketio.on("F2B_humchart_recieved")
def light():
    timestamps = []
    data = []
    sqldata = DataRepository.read_by_minute(2)
    for i in range(30):
        minute = str(sqldata[i].get('timeRead'))[11:16]
        val = sqldata[i].get('value')
        timestamps.append(minute)
        data.append(val)
    socketio.emit("B2F_lightchart",{"time":timestamps[::-1],"data":data},broadcast=True)

@socketio.on('F2B_lightchart_recieved')
def settimer():
    socketio.emit("B2F_settimer",broadcast=True)

#configurationPage

@socketio.on("F2B_settings_connected")
def settings():
    print("settings page loaded")
    if DataRepository.read_settings_row('tempMet')[0].get('tempMet') == "c":
        metric = "°c"
    else : 
        metric = "°f"
    maxTemp = DataRepository.read_settings_row('maxTemp')[0].get('maxTemp')
    minTemp = DataRepository.read_settings_row('minTemp')[0].get('minTemp')
    maxHum = DataRepository.read_settings_row('maxHum')[0].get('maxHum')
    minhum = DataRepository.read_settings_row('minHum')[0].get('minHum')
    minLight = DataRepository.read_settings_row('minLight')[0].get('minLight')
    startTime = DataRepository.read_settings_row('startTime')[0].get('startTime')
    endtime = DataRepository.read_settings_row('endtime')[0].get('endtime')
    fan = DataRepository.read_settings_row('fan')[0].get('fan')
    lamp = DataRepository.read_settings_row('lamp')[0].get('lamp')
    settings = [metric,maxTemp,minTemp,maxHum,minhum,minLight,startTime,endtime,fan,lamp]
    socketio.emit("B2F_settings", {"settings": settings}, broadcast=True)

@socketio.on("F2B_settings_recieved")
def settimer():
    socketio.emit("B2F_settimer", broadcast=True)

if __name__ == '__main__':
    try:
        print("**** Program started ****")
        sensor_read_temp()
        sensor_read_light()
        sensor_read_hum()
        fan_func()
        lamp_func()
        real_time_lcd()
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt as e:
        print("\nProgram exit.")
    finally:
        fan.force_fan()
        lamp.force_lamp()
        lcd.clear()
        GPIO.cleanup()

    

