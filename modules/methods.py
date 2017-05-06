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

def locateFile(filename):
        MAINFOLDER = "PSP0201"
        DATA_DIR = "data/" + filename
        current_dir = os.path.dirname(__file__)
        temp_path = os.path.dirname(current_dir) + '/'
        
        return temp_path + DATA_DIR



def readData(filename):
        json_file = locateFile(filename)
        if json_file.endswith(".json"):
                with open(json_file, "r") as infile:
                        users = json.load(infile)
                return users
        else:
                return json_file

def writeData(data, filename):
        json_file = locateFile(filename)
        with open(json_file, "w") as outfile:
                json.dump(data, outfile)

def defineWindow(title = "AskTrivia", geometry = "640x480"):
        window = Tkinter.Tk()
        window.title(title)
        window.geometry(geometry)
        return window




