from flask import Flask, render_template, request, url_for, g, jsonify
import sqlite3 as sql
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")
app = Flask(__name__)

def get_db():
	# check if _database attribute exist
    db = getattr(g, '_database', None)
    if db is None:
    	# if doesnt, establish a new connection and save _database attribute
    	# this prevents multiple instances to the database
        db = g._database = sql.connect(DATABASE)
        db.row_factory = sql.Row 
    return db

# @function for querying/retrieving database
def query_db(query, args=(), one=False):
	try:
	    cur = get_db().execute(query, args)
	    data = cur.fetchall()
	    cur.close()
	    if ( data ) :
	    	# If one=True
	    	if one :
	    		# Only return the first data
	    		return data[0]
	    	else:
	    		# Return all data in an array
	    		return data
	    else:
	    	# No data
	    	return None;
	except:
		# Table does not exist
		print "Database query error"
		return None;

# @function for creating a new user column in database
def insert_user(name,password,description):
	# Create a Connection to the Database
	con = sql.connect(DATABASE)
	cur = con.cursor()
	# Run and execute SQL query; Insert name, password and description with respective values into the users table
	cur.execute("INSERT INTO users (name,password,description) VALUES (?,?,?)", (name,password,description))
	con.commit()
	# Get latest id
	newid = cur.lastrowid
	con.close()
	return newid

# @function updating user in database
def update_user(user_id, params):
	# Check if user exist
	if checkUser(False, user_id):
		# Create connection to database
		con = sql.connect(DATABASE)
		cur = con.cursor()
		# Update the users table
		query = "UPDATE users SET "
		counter = 0;
		# For each key:value in {params}, accumalate it to the query variable

		for i in params :
			counter = counter + 1
			query += str(i) + "=" + str(params[i])
			if (counter != len(params)) :
				query += ","
			query += " "
		query += "WHERE id=" + str(user_id)
		# So it will be like UPDATE users SET key1=value1, key2 value2 WHERE id=3
		con.execute(query);
		con.commit()
		con.close()
		print "Updated User";
	else:
		print "User does not exist!"

# @function for getting user data; by default is to use the user's name to retrieve data, but you can also use user_id
def getUser(name, user_id = False):
	if ( user_id ) :
		# If user_id is True
		# Run data by selecting user's id
		data = query_db("select * from users WHERE id=(?)", (user_id,), True);
	else:
		# If user_id is False (default)
		# Run data by selecting user's name
		data = query_db("select * from users WHERE name=(?)", (name,), True);

	if data == None:
		# Error, return false
		return False;
	else:
		# Sucess, return data
		return data;

# @function for checking if User Exist
def checkUser(name, user_id = False):
	data = query_db("select * from users")
	if data != None:
		# No error, proceed with looping
		for user in data:
			if name != False:
				# If name is given in parameter, check if user exist by comparing with user names
				if user["name"] == name :
					return True;
					break
			else:
				# Else, check if user exist by comparing with user ids'
				if ( int(user_id) == user["id"] ) :
					return True;
					break;
	return False;

# Below are all functions for Flask's routing
# requst.form["param"] = Getting param from the POST request
# jsonify = Converts a dictionary into a JSON string for HTML viewing
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/addUser/', methods=['POST'])
def addUser():
    name=request.form['name']
    password=request.form['password']
    description=request.form['description']
    try:
    	# No error, return new_id
    	newid = insert_user(name,password,description);
    	response = {"id" : newid }
    except:
    	# Error
    	response = {"error" : True}

    return jsonify(response);

@app.route('/updateExp/', methods=['POST'])
def updateExp():
	user_id=request.form["id"]
	exp = request.form["exp"]
	weekly_exp = request.form["weekly_exp"];
	level = request.form["level"]
	try:
		# No error
		update_user(user_id, { "exp" : exp, "weekly_exp" : weekly_exp, "level" : level });
		response = {"success" : True}
	except:
		# Error
		response = {"error" : True}
	
	return jsonify(response)


@app.route('/updateDescription/', methods=['POST'])
def updateDescription():
	user_id=request.form["id"]
	description = "'{}'".format(request.form["description"])
	try:
		# No error
		update_user(user_id, {"description" : description});
		response = {"success" : True}
	except:
		# Error
		response = {"error" : True}
	return jsonify(response)


@app.route("/usernames/", methods=["GET"])
def usernames():
	users = []
	data = query_db("select * from users")
	if data != None:
		# If no error
		for user in data:
			# Add each user's name into the users[]
			users.append(user["name"])
		# Create a response dictionary containing users[]
		response = { "users": users }
	else:
		# Error
		response = { "error": True }

	return jsonify(response)

@app.route("/public/", methods=["GET"])
def public():
	users = {}
	data = query_db("select * from users")
	if ( data != None ) :
		# If no error
		for user in data:
			# Add user's info into users{}
			users[user["id"]] = { "name" : user["name"], "exp" : user["exp"], "weekly_exp" : user["weekly_exp"], "level" : user["level"] }
		# Create a response variable to contain the users{}
		response = users;
	else:
		# Error
		response = { "error" : True }
	return jsonify(response);

@app.route("/loginUser/", methods=["POST"])
def loginUser():
	name=request.form["name"]
	print name, checkUser(name)
	if ( checkUser(name) ): 
		# If user exist
		response = {  "password" : getUser(name)["password"], "id": getUser(name)["id"], "name": getUser(name)["name"], "description": getUser(name)["description"], "exp": getUser(name)["exp"], "weekly_exp" : getUser(name)["weekly_exp"], "level" : getUser(name)["level"] }
	else: 
		response = { "error" : True }
	return jsonify(response)

@app.route("/user/", methods=["POST"])
def user():
	user_id=request.form["id"]
	# Check if User exist given user_id
	if ( checkUser(False, user_id) ) :
		# User exists
		data = getUser(False, user_id)
		response = { "name" : data["name"], "level" : data["level"], "description" : data["description"] }
	else: 
		# User does not exist, error
		response = { "error" : True }
	return jsonify(response);

if __name__ == "__main__":
	with app.app_context():
		# Run flask run on machine's IP on port 5002
		app.run(host="0.0.0.0", port=5002)