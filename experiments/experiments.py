import os
import glob
import json
import time


class experiment(object):
    """
    Class used to manage the experiment JSON files, requires the local directory as an init argument.
    """

    def __init__(self, dir):
        """
        Creates the experiment object.
        Parameters
        ----------
        dir : string
            The directory where the experiment files are located.
        """
        self.dir = dir
        self.running = 0
        self.running_start = -1
        f, r = self.list()
        for i in range(len(f)):
            fi = open(f[i], "r")
            fromJson = json.load(fi)
            fi.close()
            if fromJson["running"] == 1:
                self.running += 1
                self.running_start = fromJson["startTime"]

    def list(self):
        """
        Lists all the .json experiment files stored in the directory as defined by self.dir.

        Returns
        -------
        f : list
            Contains strings with the filepaths for each file.
        r : list
            Contains strings with the file names for each file.
        """
        dir = self.dir
        files = glob.glob(os.path.join(dir, "*.*"))  # all files in directory
        f = []
        r = []
        for i in files:
            if os.path.splitext(i)[1] == ".json":  # if of file type .json
                f.append(i)
                r.append(os.path.basename(i))  # get name from filepath
        f.sort()  # alphabetic sort to ensure return order
        r.sort()
        return f, r

    def exists(self, name):
        """
        Checks to see if an experiment already exists in the current directory.

        Parameters
        ----------
        name : string
            Name of the experiment.

        Returns
        -------
        state : bool
            True if the file exists, False otherwise.
        """
        file = name
        f, existing = self.list()
        state = False
        for i in existing:
            if i == (file + ".json"):
                state = True
        return state

    def new(self, name):
        """
        Creates a new experiment.

        Parameters
        ----------
        name : string
            The name of the experiment that is being created.

        Returns
        -------
        created : bool
            True if the file has been created, False otherwise.
        """
        exists = self.exists(name)
        created = False
        if not exists:
            f = open(os.path.join(self.dir, name + ".json"), "w")
            toJson = {
                "name": name,
                "startTime": -1,
                "endTime": -1,
                "running": 0,
            }  # Initialize with default values
            json.dump(toJson, f)
            created = True
            f.close()
        return created

    def start(self, name):
        """
        Defines the start time of the experiment in seconds since Unix Epoch.

        Parameters
        ----------
        name : string
            The name of the experiment to start.

        Returns
        -------
        bool
            True if the start time was defined.
        """
        filepath = os.path.join(self.dir, name + ".json")
        with open(filepath, "r") as f:
            fromJson = json.load(f)
        fromJson["startTime"] = time.time()
        fromJson["running"] = 1  # Experiment is actively running.
        with open(filepath, "w") as f:
            json.dump(fromJson, f)
        self.running += 1
        return True

    def end(self, name):
        """
        Defines the end time of the experiment.

        Parameters
        ----------
        name : string
            The name of the experiment to end.

        Returns
        -------
        bool
            True if the end time was defined.
        """
        filepath = os.path.join(self.dir, name + ".json")
        with open(filepath, "r") as f:
            fromJson = json.load(f)
        fromJson["endTime"] = time.time()
        fromJson["running"] = 2  # Experiment is finished.
        with open(filepath, "w") as f:
            json.dump(fromJson, f)
        self.running -= 1
        return True

    def delete(self, name):
        """
        Deletes an experiment.

        Parameters
        ----------
        name : string
            The name of the experiment to delete.

        Returns
        -------
        bool
            True if the experiment was deleted.
        """
        os.remove(os.path.join(self.dir, name + ".json"))
        return True

    def info(self, name):
        """
        Returns the name, start time, end time, and running status for the experiment.

        Parameters
        ----------
        name : string
            The name of the experiment.

        Returns
        -------
        list
            Contains the name, start time, end time, and running status.
        """
        filepath = os.path.join(self.dir, name + ".json")
        with open(filepath, "r") as f:
            fromJson = json.load(f)
        return [
            fromJson["name"],
            fromJson["startTime"],
            fromJson["endTime"],
            fromJson["running"],
        ]
