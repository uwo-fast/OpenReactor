# To run this server use
"""bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
"""
import json
import flask
from flask import Flask, render_template, request
from sensor.model import Sensor,SensorReading,Control,SensorData
app = Flask(__name__)
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
        time1=[]
        time1=dataTime
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

# About page for project
@app.route("/controls")
def controls():
    sensors = []
    values = []
    controls =[]
    targets = []
    for dev in Sensor.select():
        sensors.append(dev.name)
        print(dev.name)
        values.append(SensorReading.select().where(SensorReading.name==dev.name).order_by(SensorReading.time.desc())[0].value)
    for con in Control.select():
         controls.append(con.name)
         values.append(Control.select().where(Control.name==con.name).order_by(Control.name.desc()).value)
    return render_template("controls.html",Sensors=sensors,Values=values,Controls=controls,Targets=targets)
@app.route("/update/controls",methods=['GET','POST'])
def updateControls():
    if request.method== 'GET':
        sensors = []
        values = []
        controls = []
        targets = []
        for dev in Sensor.select():
            sensors.append(dev.name)
            print(dev.name)
            values.append(SensorReading.select().where(SensorReading.name==dev.name).order_by(SensorReading.time.desc())[0].value)
            for i, v in enumerate(values):
                values[i]=round(values[i],3)
        for con in Control.select():
            controls.append(con.name)
            values.append(Control.select().where(Control.name==con.name).order_by(Control.name.desc()).value)
        return json.dumps({'sen':sensors,'val':values,'con':controls,'tar':targets})