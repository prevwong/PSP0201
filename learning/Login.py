import os
import json
#go to correct data file
cur_path = os.path.dirname(__file__)
new_path = os.path.join(cur_path, "../data/test.json")

    
with open(new_path) as infile:
    raw_file = json.load(infile)
    users = json.loads(raw_file)

name = raw_input("Give me the name")


for i in range(0, len(users)):
    if users[str(i)]["name"] == name:
        password = raw_input("Give me the password")
        if users[str(i)]["password"] == password:
            session_id = i
            break
        else:
            print "Passsword incorrect"
            break
    elif i == (len(users)-1):
        print "user not found"

        
