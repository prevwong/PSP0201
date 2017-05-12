# Methods Module, add all the general methods here
import os
import json
import Tkinter
import urllib2
import urllib


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
        DATA_DIR = "data/" + filename
        current_dir = os.path.dirname(__file__)
        temp_path = os.path.dirname(current_dir) + '/'
        
        return temp_path + DATA_DIR



def readOnlineJson(url):
    # Read JSON data from url
    error = 0;
    try:
        response = urllib.urlopen(url)
        try:
            jsonData = json.loads(response.read())
        except ValueError:
            error = 1;
    except IOError:
        error = 1;

    if ( error == 1 ) :
        return False;
    else:
        return jsonData

def readData(filename):
        json_file = locateFile(filename)
        if json_file.endswith(".json"):
            print "hi"
            with open(json_file, "r") as infile:
                try:
                    users = json.load(infile)
                except ValueError:
                    users = {}
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

def backupQuestions():
        categorynum = {"Random":9,"Books":10,"Film":11,"Music":12,"Musicals & Theatres":13,"Television":14,"Video Games":15,"Board Games":16,
               "Science & Nature":17,"Computers":18,"Mathematics":19,"Mythology":20,"Sports":21,"Geography":22,"History":23,"Politics":24,"Art":25,
               "Celebrities":26,"Animals":27,"Vehicles":28,"Comics":29,"Gadgets":30,"Japanese Anime & Manga":31,"Cartoon & Animations":32}

        quantities = [5, 10, 15, 20]

        obj = {}

        for i in categorynum:
                category = categorynum[i]
                obj[category] = {}

                for quantity in quantities: 
                        url = "https://opentdb.com/api.php?amount="+ str(quantity) +"&category=" + str(category)
                        response = urllib.urlopen(url)
                        jsonData = json.loads(response.read())
                        results = jsonData["results"]
                        obj[category][quantity] = results
                        print "added", category, quantity

        with open('data/backup.json', 'w') as outfile:
                json.dump(obj, outfile)

def URLRequest(url, params):
    data = urllib.urlencode(params)
    try:
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        return response.read()
    except:
        return None;

def getUserData(session_id):
    if (URLRequest("http://52.36.70.190:5002/user/", {"id" : session_id}) != None) :
        data = URLRequest("http://52.36.70.190:5002/user/", {"id" : session_id})
        return json.loads(data);
    else:
        data = readData("users.json");
        return data[session_id];

#URLRequest("http://localhost:5002/adduser/", { "name" : "prevwong", "password" : "imgeneva", "description" : "Hello world!" })

#print URLRequest("http://localhost:5002/usernames/", {})
