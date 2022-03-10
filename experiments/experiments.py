import os 
import glob
import json
import time

class experiment(object):
    """
    class used to manage the experiment JSON files, requires the local directory as an init argument. 
    """


    def __init__(self,dir):
        self.dir=dir


    def list(self):
        dir=self.dir
        files=glob.glob(os.path.join(dir,"*.*"))
        f=[]
        r=[]
        for i in files:
            if os.path.splitext(i)[1]==".json":
                f.append(i)
                r.append(os.path.basename(i))
        f.sort()
        r.sort()
        return f,r

    def exists(self,name):
        file = name
        f,existing=self.list()
        state=False
        for i in existing:
            if i==file:
                state=True
        return state

    def new(self,name):
        """
        Creates new experiment
        """
        exists=self.exists(name)
        created=False
        if not exists:
            f=open(self.dir+"/"+name+".json","w")
            toJson={"name":name,"startTime":-1,"endTime":-1,"running":0}
            json.dump(toJson,f)
            created=True
            f.close()
        return created

    def start(self,name):
        """
        Defines start time of the experiment
        """
        f=open(self.dir+"/"+name+".json","r")
        fromJson=json.load(f)
        f.close()
        f=open(self.dir+"/"+name+".json",'w')
        fromJson["startTime"]=time.time()#time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        fromJson["running"]=1
        json.dump(fromJson,f)
        f.close()
        return True

    def end(self,name):
        """
        Defines end time of the experiment
        """
        f=open(self.dir+"/"+name+".json",'r')
        fromJson=json.load(f)
        f.close()
        f=open(self.dir+"/"+name+".json",'w')
        fromJson["endTime"]=time.time()#time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        fromJson["running"]=2
        json.dump(fromJson,f)
        f.close()


    def delete(self,name):
        """
        Deletes experiment
        """
        os.remove(self.dir+"/"+name+".json")
        return True


    def info(self,name):
        """
        Returns the name, start, and end times for experiment.
        """
        #with open(self.dir+"/"+name+",json","r") as read_file:
        #    fromJson=json.loads(read_file)
        
        
        f=open(self.dir+"/"+name+".json",'r')
        fromJson=json.load(f)
        print(fromJson)
        f.close()
        return [fromJson["name"],fromJson["startTime"],fromJson["endTime"],fromJson["running"]]