# To run this server use
"""bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
"""
import json
import flask
import time
from flask import Flask, render_template, request
from sensor import sensor
from sensor.model.model import Sensor,SensorReading,Control,SensorData
from sensor.device_detect import connected as ct
app = Flask(__name__)

def innit_connected(I2C_dev):
    connected=ct()
    for sen in connected.devs:
        dev=sensor.I2C(name=sen[1],units=sen[2],address=sen[0],form=sen[3],request_message=sen[4],delay=sen[5],read_length=sen[6])
        I2C_dev.append(dev)
        #print('sen:{}'.format(sen))
        #print(dev.value)
        if not SensorReading.select().where(SensorReading.name==dev.name):
            print("Missing : {}".format(dev.name))
            dev.readEmpty()
            dev.store()

def innit_control():
    #print(Control.select())
    SensorData().define_control(name="System Toggle", target=-1,value=0)

I2C_dev=[]
innit_connected(I2C_dev)
print(I2C_dev)
innit_control()
toDisplay=[]
devices=[]
for dev in Sensor.select():
    devices.append(dev.name)
print("Loaded app.py")
Data=SensorData()
# Home page
@app.route("/")
def index():
    return render_template("index.html")

#graph update methods
@app.route("/update/graphs/<graphID>",methods=['GET','POST'])

def update(graphID):
        if request.method== 'GET':
                print(toDisplay)
                (time,values,title,toParse)=graphsUpdate(toDisplay[int(graphID)])
                return json.dumps({'Time':time,'Values':values,'Title':title, 'Parsed':toParse})
        if request.method == 'POST':
                data=request.json
                print(data[0])
                toDisplay[int(graphID)]=data[0]
                return flask.jsonify(data)

@app.route("/add",methods=['POST'])
def add():
        print(toDisplay)
        data=request.json[0]
        print(data)
        if data==0:
                toDisplay.clear()
        if (len(toDisplay))==data:
                toDisplay.append("-1")
        return flask.jsonify(data)
                
# Graphs page
@app.route("/graphs",methods=['GET','POST'])

def graphs():
    return render_template("graphs.html",Devices=devices)
    #(time1,values1,title1,toParse,time2,values2,title2,toParse2)=graphsUpdate()
    #return render_template("graphs.html", Time=time1, Values=values1, Title=title1,Parsed=toParse,Time2=time2,Values2=values2,Title2=title2,Parsed2=toParse2)
def graphsUpdate(toDisplay):
    print(toDisplay)
    if toDisplay=="-1":
        time1=[]
        values1=[]
        title1=[]
        toParse=[]
    else:
        title1 = toDisplay+" over time"
        dataTime=[]
        for Time in SensorReading.select().where(SensorReading.name==toDisplay).order_by(SensorReading.time):
            dataTime.append(Time.time.timestamp())
        dataData=[]
        
        for Data in SensorReading.select().where(SensorReading.name==toDisplay).order_by(SensorReading.time):
            dataData.append(Data.value)
        values1 = dataData
        #time1=[]
        time1=dataTime
        first=time.time()
        if len(time1)!=0:
            first=time1[0]
        for i in range(len(time1)):
            time1[i]=(time1[i]-first)/3600
        toParse=[]
        for i in range(len(dataTime)):
            toParse.append((dataTime[i],values1[i]))
        print('Fetched Data')
    return time1,values1,title1, toParse
# About page for project
@app.route("/about")
def about():
    return render_template("about.html")

# Page for controls
@app.route("/controls")
def controls():
    sensors = []
    values = []
    controls =[]
    targets = []
    controls_values=[]
    print(Control.select()[0].name)
    for dev in Sensor.select():
        sensors.append(dev.name)
        print("Name:{}".format(dev.name))
        #for i in SensorReading.select().where(SensorReading.name==dev.name):
        #    print("Reading:{}".format(i.value))
        length=len(SensorReading.select().where(SensorReading.name==dev.name))
        val=SensorReading.select().where(SensorReading.name==dev.name).order_by(SensorReading.time)[length-1].value
        print(val)
        values.append(val)
    for con in Control.select():
         controls.append(con.name)
         length=len(Control.select().where(Control.name==con.name).order_by(Control.name.desc()))
         valTar=Control.select().where(Control.name==con.name).order_by(Control.name.desc())[length-1].target
         targets.append(valTar)
         valCon=Control.select().where(Control.name==con.name).order_by(Control.name.desc())[length-1].value
         controls_values.append(valCon)
    return render_template("controls.html",Sensors=sensors,Values=values,Controls=controls,Targets=targets,ControlsValues=controls_values)
@app.route("/update/controls",methods=['GET','POST'])
def updateControls():
    if request.method== 'GET':
        sensors = []
        values = []
        controls = []
        targets = []
        controls_values = []
        for dev in Sensor.select():
            sensors.append(dev.name)
            print(dev.name)
            values.append(SensorReading.select().where(SensorReading.name==dev.name).order_by(SensorReading.time.desc())[0].value)
            for i, v in enumerate(values):
                values[i]=round(values[i],3)
        for con in Control.select():
            controls.append(con.name)
            length=len(Control.select().where(Control.name==con.name).order_by(Control.name.desc()))
            val=Control.select().where(Control.name==con.name).order_by(Control.name.desc())[length-1].target
            targets.append(val)
            val=Control.select().where(Control.name==con.name).order_by(Control.name.desc())[length-1].value
            controls_values.append(val)
        return json.dumps({'sen':sensors,'val':values,'con':controls,'tar':targets,'con_val':controls_values})

@app.route("/controls/measure/<side>",methods=['GET','POST'])
def measure(side):
    if request.method=='POST':
        if side == "sensor":
            sensor_measure=request.json
            print(sensor_measure)
            for dev in I2C_dev:
                if dev.name==sensor_measure:
                    dev.read()
                    dev.store()
                    dev.print_info()
        elif side == "control":
            print("Control Return:{}".format(request.json))
            control_return=request.json
            q = Control.update({Control.target:control_return[1]}).where(Control.name==control_return[0])
            q.execute()
    return flask.jsonify(side)