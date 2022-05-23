import os 
import glob
import json
import time

class experiment(object):
    """
    class used to manage the experiment JSON files, requires the local directory as an init argument. 
    """


    def __init__(self,dir):
        """
        creates the experiment object
        Parameters
        ----------
        dir : string
            the directory where the experiment files are located 
        """
        self.dir=dir
        self.running=0
        f,r=self.list()
        for i in range(len(f)):
            fi=open(f[i],'r')
            fromJson=json.load(fi)
            fi.close()
            if fromJson["running"]==1:
                self.running+=1



    def list(self):
        """
        Lists all the .json experiment files stored in the directory as defined by the self.dir
        Returns
        -------
        f : array
            contains strings with the filepaths for each file
        r : array
            contains strings with the file names for each file 
        """
        dir=self.dir
        files=glob.glob(os.path.join(dir,"*.*"))        # all files in directory
        f=[]
        r=[]
        for i in files:
            if os.path.splitext(i)[1]==".json":     # if of file type .json
                f.append(i)
                r.append(os.path.basename(i))       #get name from filepath
        f.sort()        # alphabetic sort to ensure return order 
        r.sort()
        return f,r

    def exists(self,name):
        """
        Checks to see if an already exists in the current directory
        Parameters
        ----------
        name : string
            name of experiment
        Returns
        -------
        state : boolean 
            if the file exists or not
        """
        file = name
        f,existing=self.list()
        state=False
        for i in existing:
            if i==(file+'.json'):
                state=True
        return state

    def new(self,name):
        """
        Creates new experiment
        Parameters
        ----------
        name : string
            the name of the experiment that is being created
        Results
        -------
        created : boolean
            if the file has been created or not
        """
        exists=self.exists(name)
        created=False
        if not exists:
            f=open(self.dir+"/"+name+".json","w")
            toJson={"name":name,"startTime":-1,"endTime":-1,"running":0}        #inits with start and end times of -1 and state of 0 indicating that the experiment has no data.
            json.dump(toJson,f)
            created=True
            f.close()
        return created

    def start(self,name):
        """
        Defines start time of the experiment in seconds since Unix Epoch
        Parameters
        ----------
        name : string
            the name of the experiment to start
        Returns
        -------
        boolean
            if the start time was defined
        """
        f=open(self.dir+"/"+name+".json","r")
        fromJson=json.load(f)
        f.close()
        f=open(self.dir+"/"+name+".json",'w')
        fromJson["startTime"]=time.time()#time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        fromJson["running"]=1       #sets running to 1, indicates that the experiment is actively running. 
        json.dump(fromJson,f)
        f.close()
        self.running+=1
        return True

    def end(self,name):
        """
        Defines end time of the experiment
        Parameters
        ----------
        name : string
            the name of the experiment to end
        Returns
        -------
        boolean
            if the end time was defined
        """
        f=open(self.dir+"/"+name+".json",'r')
        fromJson=json.load(f)
        f.close()
        f=open(self.dir+"/"+name+".json",'w')
        fromJson["endTime"]=time.time()#time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        fromJson["running"]=2       #sets running to 2, indicates that the experiment is finished
        json.dump(fromJson,f)
        f.close()
        self.running-=1
        return True


    def delete(self,name):
        """
        Deletes experiment
        Parameters
        ----------
        name : string
            the name of the experiment to delete
        Returns
        -------
        boolean
            if the experiment was deleted
        """
        os.remove(self.dir+"/"+name+".json")
        return True


    def info(self,name):
        """
        Returns the name, start, and end times for experiment.
        Parameters
        ----------
        name : string
            the name of the experiment
        Returns
        -------
        tuple
            returns the name,start time, end time, and running status as a tuple
        """
        #with open(self.dir+"/"+name+",json","r") as read_file:
        #    fromJson=json.loads(read_file)
        
        
        f=open(self.dir+"/"+name+".json",'r')
        fromJson=json.load(f)
        #print(fromJson)
        f.close()
        return [fromJson["name"],fromJson["startTime"],fromJson["endTime"],fromJson["running"]]