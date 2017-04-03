import json


users = {}
users[0] = {}
users[0]["name"] = "Prev Wong"
users[0]["type"] = "Supreme Leader"
users[0]["id"] = "1161101470"

users[1] = {}
users[1]["name"] = "Wei Long"
users[1]["type"] = "Bartender"
users[1]["id"] = "11611012345"


jsonData = json.dumps(users)

print jsonData
