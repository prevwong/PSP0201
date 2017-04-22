import json
import os

#go to correct data file
cur_path = os.path.dirname(__file__)
new_path = os.path.join(cur_path, "../data/test.json")

#store user profile inside database
    
users = {}
users[0] = {}
users[0]["name"] = "Prev Wong"
users[0]["type"] = "Supreme Leader"
users[0]["id"] = "1161101470"
users[0]["exp"] = "500"
users[0]["weeklyexp"] = "20"

new_id = len(users)
users[new_id] = {}
users[new_id]["name"] = "Prev Wong12"
users[new_id]["type"] = "Supreme Leader"
users[new_id]["id"] = "11611021470"
users[new_id]["exp"] = "5000"
users[new_id]["weeklyexp"] = "10"

new_id = len(users)
users[new_id] = {}
users[new_id]["name"] = "Prev 23"
users[new_id]["type"] = "Supreme Leader"
users[new_id]["id"] = "1161101470"
users[new_id]["exp"] = "2500"
users[new_id]["weeklyexp"] = "0"

new_id = len(users)
users[new_id] = {}
users[new_id]["name"] = "Wei Lo2312ng"
users[new_id]["type"] = "Barte123nder"
users[new_id]["id"] = "11611012345"
users[new_id]["exp"] = "1234"
users[new_id]["weeklyexp"] = "2050"

users = json.dumps(users, sort_keys=True)

with open(new_path, "w") as outfile:
    json.dump(users, outfile)

#reading user from database
    
with open(new_path) as infile:
    raw_file = json.load(infile)
    users = json.loads(raw_file)

#sort by exp
    
def sort_by_exp(users):
    exp_sorted = sorted(users, key=lambda x: int((users[str(x)]["exp"])), reverse=True)
    i = 1
    info_array = {}
    for id in exp_sorted:
        info_array[i]={}
        info_array[i]["name"] = users[id]["name"]
        info_array[i]["exp"] = users[id]["exp"]
        i = i + 1
    return info_array
    
#sort by weekly exp
def sort_by_weeklyexp(users):
    weeklyexp_sorted = sorted(users, key=lambda x: int((users[str(x)]["exp"])), reverse=True)
    i = 1
    info_array = {}
    for id in weeklyexp_sorted:
        info_array[i]={}
        info_array[i]["name"] = users[id]["name"]
        info_array[i]["weeklyexp"] = users[id]["weeklyexp"]
        i = i + 1
    return info_array



    
print sort_by_exp(users)
