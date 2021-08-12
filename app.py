# To run this server use
"""bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
"""
import json
import model
import flask
from flask import Flask, render_template, request
from model import Sensor,SensorReading
app = Flask(__name__)
toDisplay=['pH','Dissolved Oxygen']
# Home page
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update",methods=['GET','POST'])

def update():
        if request.method== 'GET':
                (time1,values1,title1,toParse)=graphsUpdate(toDisplay[0])
                (time2,values2,title2,toParse2)=graphsUpdate(toDisplay[1])
                #graph1=flask.request.form('DeviceDrop')
                #console.log(graph1)
                return json.dumps({'Time':time1,'Values':values1,'Title':title1, 'Parsed':toParse,'Time2':time2,'Values2':values2,'Title2':title2,'Parsed2':toParse2})
        if request.method == 'POST':
                data=request.json
                print(data)
                for i in range(len(data)):
                        toDisplay[i]=data[i]
                return flask.jsonify(data)
                
# Graphs page
@app.route("/graphs",methods=['GET','POST'])
def graphs():
    devices=[]
    for dev in Sensor.select():
        devices.append(dev.name)
    return render_template("graphs.html",Devices=devices)
    #(time1,values1,title1,toParse,time2,values2,title2,toParse2)=graphsUpdate()
    #return render_template("graphs.html", Time=time1, Values=values1, Title=title1,Parsed=toParse,Time2=time2,Values2=values2,Title2=title2,Parsed2=toParse2)
def graphsUpdate(toDisplay="pH"):
    
    
    
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
    title2 = toDisplay[1]+" over time"
    print('Fetched Data')
    return time1,values1,title1, toParse
class dataPoints:
   def __init__(self,time,value):
      self.x=time
      self.y=value
# About page for project
@app.route("/about")
def about():
    return render_template("about.html")

# About page for project
@app.route("/test")
def test():
    return render_template("test.html")
