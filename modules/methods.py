# Methods Module, add all the general methods here
import os
import json
import Tkinter

def loopList(items):
	for i in items:
		print i

def centerWindow(root):
	root.withdraw()
	root.update_idletasks()  # Update "requested size" from geometry manager

	x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
	y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
	root.geometry("+%d+%d" % (x, y))
	root.deiconify()

def locateUserJSON():
        MAINFOLDER = "PSP0201"
        DATA_DIR = "/data/test.json"
        current_dir = os.path.dirname(__file__)
        temp_path = current_dir
        while (temp_path.split("\\")[-1] != MAINFOLDER):
                temp_path = os.path.abspath(os.path.join(temp_path, os.pardir))
        return temp_path + DATA_DIR


def readData():
        json_file = locateUserJSON()
        with open(json_file, "r") as infile:
                users = json.load(infile)
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




