from flask import Flask, render_template, request, url_for, g, jsonify
import sqlite3 as sql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
        db.row_factory = sql.Row 
    return db

def query_db(query, args=(), one=False):
	try:
	    cur = get_db().execute(query, args)
	    rv = cur.fetchall()
	    cur.close()
	    if ( rv ) :
	    	if one :
	    		return rv[0]
	    	else:
	    		return rv
	    else:
	    	return None;
	except:
		print "Database query error"
		return None;

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/adduser/', methods=['POST'])
def adduser():
    name=request.form['name']
    password=request.form['password']
    description=request.form['description']
    newid = insert_user(name,password,description);
    return jsonify({"id" : newid });

def insert_user(name,password,description):
	newid = 0;
	con = sql.connect(DATABASE)
	cur = con.cursor()
	cur.execute("INSERT INTO users (name,password,description) VALUES (?,?,?)", (name,password,description))
	con.commit()
	newid = cur.lastrowid
	con.close()
	return newid

def update_user_exp(user_id, exp, weekly_exp, level):
	print "updating...", user_id
	if checkUser(False, user_id):
		print "update"
		con = sql.connect(DATABASE)
		cur = con.cursor()
		cur.execute("UPDATE users SET exp=(?), weekly_exp=(?), level=(?) WHERE id=(?)", (exp,weekly_exp,level, user_id))
		con.commit()
		con.close()
		print "update user exp:";
	else:
		print "User does not exist!"

@app.route('/updateexp/', methods=['POST'])
def updateexp():
	user_id=request.form["id"]
	exp = request.form["exp"]
	weekly_exp = request.form["weekly_exp"];
	level = request.form["level"]
	update_user_exp(user_id, exp, weekly_exp, level);
	return jsonify({"success" : True})



def getUser(name, user_id = False):
	if ( user_id == False ) :
		query = query_db("select * from users WHERE name=(?)", (name,), True);
	else:
		query = query_db("select * from users WHERE id=(?)", (user_id,), True);

	if query == None:
		return False;
	else:
		return query;

def checkUser(name, user_id = False):
	data = query_db("select * from users")
	if data != None:
		for user in data:
			if name != False:
				if user["name"] == name :
					return True;
					break
			else:
				if ( int(user_id) == user["id"] ) :
					return True;
					break;
	return False;

@app.route("/usernames/", methods=["GET"])
def usernames():
	users = []
	data = query_db("select * from users")
	if data != None:
		for user in data:
			print user["id"]
			users.append(user["name"])

		response = { "users": users }
	else:
		response = { "error": True }

	return jsonify(response)

@app.route("/public/", methods=["GET"])
def public():
	users = {}
	data = query_db("select * from users")
	if ( data != None ) :
		for user in data:
			users[user["id"]] = { "name" : user["name"], "exp" : user["exp"], "weekly_exp" : user["weekly_exp"], "level" : user["level"] }
		response = users;
	else:
		response = { "error" : True }
	return jsonify(response);

@app.route("/loginUser/", methods=["POST"])
def loginUser():
	name=request.form["name"]
	print name, checkUser(name)
	if ( checkUser(name) ): 
		response = { "password" : getUser(name)["password"], "id": getUser(name)["id"], "name": getUser(name)["name"], "exp": getUser(name)["exp"], "weekly_exp" : getUser(name)["weekly_exp"], "level" : getUser(name)["level"] }
		return jsonify(response)
	else: 
		return jsonify({"error" : True})

@app.route("/user/", methods=["POST"])
def user():
	user_id=request.form["id"]
	response = "";
	if ( checkUser(False, user_id) ) :
		response = getUser(False, user_id)
		return jsonify({ "name" : response["name"], "level" : response["level"], "description" : response["description"] });

if __name__ == "__main__":
	#insert_user("prevwong", "imgenev", "I am Prev!")
	with app.app_context():
		#print getUser("prevwong")["exp"]
		#print getUser(False, 1)
		#print checkUser("prevwong") 
		app.run(host="0.0.0.0", port=5002)