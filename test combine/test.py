from Tkinter import *
import json
import os
import os.path


def locateUserJSON():
        MAINFOLDER = "PSP0201"
        DATA_DIR = "/data/users.json"
        current_dir = os.path.dirname(__file__)
        temp_path = current_dir
        while (temp_path.split("\\")[-1] != MAINFOLDER):
                temp_path = os.path.abspath(os.path.join(temp_path, os.pardir))
        return temp_path + DATA_DIR


def readData():
        json_file = locateUserJSON()
        with open(json_file, "r") as infile:
                users = json.loads(json.load(infile))
        return users

def writeData(data):
        json_file = locateUserJSON()
        with open(json_file, "w") as outfile:
                json.dump(data, outfile)

def defineWindow(title = "AskTrivia", geometry = "640x480"):
        window = Tkinter.Tk()
        window.title(title)
        window.geometry(geometry)
        return window
    
users = {}
for i in range(0,10):
   
    users[i] = {}
    users[i]["name"] = `i` + "hohoho"
    users[i]["password"] = "elemek"
    users[i]["exp"] = 100
    users[i]["weeklyexp"] = 50 
    users[i]["level"] = 1
    users[i]["description"] = "Type something here"

writeData(users)
