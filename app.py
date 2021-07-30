# To run this server use
"""bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
"""
import json
import model
import flask
from flask import Flask, render_template
from model import Sensor,SensorReading
app = Flask(__name__)

# Home page
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update",methods=['GET'])
def update():
        (time1,values1,title1,toParse,time2,values2,title2,toParse2)=graphsUpdate()
        return json.dumps({'Time':time1,'Values':values1, 'Parsed':toParse,'Time2':time2,'Values2':values2,'Title2':title2,'Parsed2':toParse2})
# Graphs page
@app.route("/graphs",methods=['GET','POST'])
def graphs():
    (time1,values1,title1,toParse,time2,values2,title2,toParse2)=graphsUpdate()
    return render_template("graphs.html", Time=time1, Values=values1, Title=title1,Parsed=toParse,Time2=time2,Values2=values2,Title2=title2,Parsed2=toParse2)
    #return flask.jsonify({'payload':json.dumps({'Time':time1,'Values':values1, 'Parsed':toParse,'Time2':time2,'Values2':values2,'Title2':title2,'Parsed2':toParse2})})
def graphsUpdate():
    toDisplay=['pH','Dissolved Oxygen']

    
    title1 = toDisplay[0]+" over time"
    xLabel1 = "Time"
    yLabel1 = "Number"

    
    dataTime=[]
    for Time in SensorReading.select().where(SensorReading.name==toDisplay[0]).order_by(SensorReading.time):
         dataTime.append(Time.time.timestamp())
    dataData=[]
    print(dataTime)
    for Data in SensorReading.select().where(SensorReading.name==toDisplay[0]).order_by(SensorReading.time):
        dataData.append(Data.value)
    print(dataData)
    values1 = dataData
    time1=[]
    time1=dataTime
    first=time1[0]
    for i in range(len(time1)):
        time1[i]=(time1[i]-first)/3600
    toParse=[]
    for i in range(len(dataTime)):
        toParse.append((dataTime[i],values1[i]))
        print(toParse[i])
    title2 = toDisplay[1]+" over time"
    xLabel2 = "Time"
    yLabel2 = "Number"


    dataTime2=[]
    for Time2 in SensorReading.select().where(SensorReading.name==toDisplay[1]).order_by(SensorReading.time):
         dataTime2.append(Time2.time.timestamp())
    dataData2=[]
    print(dataTime2)
    for Data2 in SensorReading.select().where(SensorReading.name==toDisplay[1]).order_by(SensorReading.time):
        dataData2.append(Data2.value)
    print(dataData2)
    values2 = dataData2
    time2=[]
    time2=dataTime2
    first2=time2[0]
    for i in range(len(time2)):
        time2[i]=(time2[i]-first2)/3600
    toParse2=[]
    for i in range(len(dataTime2)):
        toParse2.append((dataTime2[i],values2[i]))
        print(toParse2[i])

    return time1,values1,title1, toParse, time2,values2,title2,toParse2
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
