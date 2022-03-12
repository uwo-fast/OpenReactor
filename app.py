# To run this server use
"""bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
"""
from datetime import datetime
import json
import flask
import time
import os
from flask import Flask, render_template, request
from sensor import sensor
from sensor.model.model import Sensor,SensorReading,Control,SensorData
from sensor.device_detect import connected as ct
from experiments.experiments import experiment
app = Flask(__name__)

dir = os.path.dirname(os.path.realpath(__file__))

def innit_connected(I2C_dev):
    """
    Used to get all connected I2C devices 
    Parameters 
    ----------
    I2C_dev : array
        array that the I2C objects are appended to 
    """
    connected=ct()
    for sen in connected.devs:
        dev=sensor.I2C(name=sen[1],units=sen[2],address=sen[0],form=sen[3],request_message=sen[4],delay=sen[5],read_length=sen[6])      #creates I2C object for each detected sensor
        I2C_dev.append(dev)
        #print('sen:{}'.format(sen))
        #print(dev.value)
        if not SensorReading.select().where(SensorReading.name==dev.name):      #if this sensor hasn't been used before creates an 'empty' reading of -1 that creates an entry but isn't parsed
            print("Missing : {}".format(dev.name))
            dev.readEmpty()
            dev.store()

def innit_control():
    print(Control.select())
    #SensorData().define_control(name="System Toggle", target=-1,value=0)

def experiment_entries(timeStart,timeEnd,name):
    """
    Used to determine measurements taken within a given experiment cycle
    Parameters
    ----------
    timeStart : float
        experiment start time given in seconds elapsed since Unix epoch, note that JS uses milliseconds
    timeEnd : float 
        experiment end time given in seconds elapsed since Unix epoch
    name : string
        name of the sensor for which measurements are requested, if "all" then every reading regardless of sensor will be returned
    Returns
    -------
    tuple 
        returns 3 arrays the sensor names, the sensor values, and the measurement times, sorted by time
    """
    timeStart=datetime.fromtimestamp(timeStart)
    timeEnd=datetime.fromtimestamp(timeEnd)
    sensor=[]
    values=[]
    times=[]
    if name=="all":
        for v in SensorReading.select().where(SensorReading.time.between(timeStart,timeEnd)).order_by(SensorReading.time):      #selects all measurements between the two times
            sensor.append(v.name)
            values.append(v.value)
            times.append(v.time.timestamp())
        return sensor,values,times
    else:
        for v in SensorReading.select().where(SensorReading.name==name,SensorReading.time.between(timeStart,timeEnd)).order_by(SensorReading.time):     #selects measurements for specified sensor in time range
            sensor.append(v.name)
            values.append(v.value)
            times.append(v.time.timestamp())
        return sensor,values,times

I2C_dev=[]      #stores connected devices
innit_connected(I2C_dev)
print(I2C_dev)
innit_control()
toDisplay=[]        #array for currently displayed graphs
devices=[]      #used to store all devices that have ever been connected
for dev in Sensor.select():
    devices.append(dev.name)
print("Loaded app.py")
Data=SensorData()       #init database class
@app.route("/")
def index():
    """
    Default landing page
    Returns
    -------
        loads the default index.html 
    """
    return render_template("index.html")

#graph update methods
@app.route("/update/graphs/<graphID>/<name>",methods=['GET','POST'])

def update(graphID,name):
    """
    fetches up to date data for the graph
    Parameters
    ----------
    graphID : int
        the index for the requested graph to be updated
    name : string 
        name for the sensor that is being displayed on the graph
    Returns
    -------
        Method 'GET'
            JSON with the time array, value array, title of the graph, and formatted time array. 
        Method 'POST'
            returns confirmation of success, adds that graph to toDisplay 
    """
    if request.method== 'GET':
            print(toDisplay)
            print("Selected:{}".format(name))
            (time,values,title,toParse)=graphsUpdate(toDisplay[int(graphID)],name)
            return json.dumps({'Time':time,'Values':values,'Title':title, 'Parsed':toParse})
    if request.method == 'POST':
            data=request.json
            print(data[0])
            toDisplay[int(graphID)]=data[0]
            return flask.jsonify(data)

def graphsUpdate(toDisplay,selected):
    """"
    retrieves and formats data for graphing
    Parameters
    ----------
    toDisplay : string
        name of the sensor to display
    selected : string
        name of selected experiment that is to be displayed
    Returns
    -------
    tuple
        contains arrays that have the time of measurement, value of measurement, graph title, formatted time of measurement
    """
    print(toDisplay)
    if toDisplay=="-1":
        time1=[]
        values1=[]
        title1=[]
        toParse=[]
    else:
        title1 = toDisplay+" over time"
        dataTime=[]
        dataData=[]
        exp=experiment('./experiments')     #init experiment 
        sen,timeStart,timeEnd,running=exp.info(selected)        #gets the information for the given experiment 
        if timeEnd==-1:     #if the experiment hasn't ended, either still running or hasn't been started. Use current time. 
            timeEnd=datetime.fromtimestamp(time.time()).timestamp()
        if timeStart==-1:     #if the experiment hasn't ended, either still running or hasn't been started. Use current time. 
            timeStart=datetime.fromtimestamp(time.time()).timestamp()
        sen,dataData,dataTime=experiment_entries(timeStart,timeEnd,toDisplay)       #returns the data measurements during time interval 
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

    
@app.route("/add",methods=['POST'])
def add():
    """
    used whenever an empty graph is created on the page
    Parameters
    ----------
    Request : json
        json sent from interface containing number of current graphs
    """
    print(toDisplay)
    data=request.json[0]
    print(data)
    if data==0:     #if no graphs are displayed then toDisplay should be cleared to reflect this
            toDisplay.clear()
    if (len(toDisplay))==data:      #ensure that the number of graphs on frontend and backend are the same, then adds new empty graph to array
            toDisplay.append("-1")
    return flask.jsonify(data)
                
# Graphs page
@app.route("/graphs",methods=['GET','POST'])

def graphs():
    """
    Loads default graphs page
    Returns
    ------
        load graphs.html, also sends the connected devices
    """
    return render_template("graphs.html",Devices=devices)
    #(time1,values1,title1,toParse,time2,values2,title2,toParse2)=graphsUpdate()
    #return render_template("graphs.html", Time=time1, Values=values1, Title=title1,Parsed=toParse,Time2=time2,Values2=values2,Title2=title2,Parsed2=toParse2)

@app.route("/about")
def about():
    """
    Loads default info page
    Returns
    -------
        loads about.html
    """
    return render_template("about.html")

# Page for controls
@app.route("/controls")
def controls():
    """
    Loads the controls page, sends information at time of request
    Returns
    -------
        loads controls.html with initial values
    """
    sensors = []
    values = []
    controls =[]
    targets = []
    controls_values=[]
    print(Control.select()[0].name)
    for dev in Sensor.select():     #for sensors in database
        sensors.append(dev.name)
        print("Name:{}".format(dev.name))
        #for i in SensorReading.select().where(SensorReading.name==dev.name):
        #    print("Reading:{}".format(i.value))
        length=len(SensorReading.select().where(SensorReading.name==dev.name))
        val=SensorReading.select().where(SensorReading.name==dev.name).order_by(SensorReading.time)[length-1].value     #gets last measurement
        print(val)
        values.append(val)
    for con in Control.select():        #for declared control systems
         controls.append(con.name)
         length=len(Control.select().where(Control.name==con.name).order_by(Control.name.desc()))
         valTar=Control.select().where(Control.name==con.name).order_by(Control.name.desc())[length-1].target
         targets.append(valTar)
         valCon=Control.select().where(Control.name==con.name).order_by(Control.name.desc())[length-1].value
         controls_values.append(valCon)
    return render_template("controls.html",Sensors=sensors,Values=values,Controls=controls,Targets=targets,ControlsValues=controls_values)
@app.route("/update/controls",methods=['GET'])
def updateControls():
    """
    updates the controls page with current values
    Returns
    -------
    json
        contains connected sensors, values, initiated controls, control targets, and control values
    """
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
    """
    Takes measurements of sensors when selected in controls interface, sets targets for control systems
    Parameters
    ----------
    side : string 
        either "sensor" or "control" the interface is split into two sides, one for sensors and one for controls
    request : json
        contains the name of the sensor or control mechanism that needs to be read/updated
    """
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

@app.route("/update/experiments/<method>/<name>",methods=['GET','POST'])
def updateExp(method,name):
    """
    interfaces with the experiment files, handles writing and reading.
    See /experiments/experiments.py 
    Parameters
    ----------
    method : string
        the requested information/instruction 
    name : string
        the name of the experiment to be interfaced with
    Returns
    -------
    json
        content returned is based on request method, if 'GET' returns a JSON of an array, if 'POST' then returns success boolean
    """
    exp=experiment('./experiments')
    print(exp.list())
    if request.method=='GET':
        if method=="list":
            path,ret=exp.list()     #all experiments regardless of status
        elif method=="info":
            ret=exp.info(name)      #name, start time, end time, status of experiment
        return json.dumps({'ret':ret})
    elif request.method=='POST':    #all methods return boolean of success status
        if method=="new":
            success=exp.new(name)
        elif method=="start":
            success=exp.start(name)
        elif method=="end":
            success=exp.end(name)
        elif method=="delete":
            success=exp.delete(name)
        elif method=="exists":
            success=exp.exists(name)
            time.sleep(1)
        return flask.jsonify(success)
    
@app.route("/download/csv/<selected>/<forSensor>",methods=['GET'])
def createDownload(selected,forSensor):
    """
    gathers data for export as CSV
    Parameters
    ----------
    selected : string
        the name of selected experiment
    forSensor : string
        name of sensor for which the measurements should be exported 
    Returns
    -------
    json
        sensor name, array containing values, array containing timestamps. 
    """
    dataTime=[]
    dataData=[]
    exp=experiment('./experiments')
    sen,timeStart,timeEnd,running=exp.info(selected)
    if timeEnd==-1:
        timeEnd=datetime.fromtimestamp(time.time()).timestamp()
    sen,dataData,dataTime=experiment_entries(timeStart,timeEnd,forSensor)
    return json.dumps({'sensorName':sen,'values':dataData,'time':dataTime})