from flask import Flask, render_template, request, url_for, g, jsonify
import sqlite3 as sql

DATABASE = 'database.db'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
        db.row_factory = sql.Row 
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

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
	return render_template("index.html")



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
	for user in query_db('select * from users'):
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
	for user in query_db("select * from users"):
		print user["id"]
		users.append(user["name"])

	all_users = { "users": users }
	return jsonify(all_users)

@app.route("/public/", methods=["GET"])
def public():
	users = {}
	for user in query_db("select * from users"):
		users[user["id"]] = { "name" : user["name"], "exp" : user["exp"], "weekly_exp" : user["weekly_exp"], "level" : user["level"] }

	return jsonify(users);

@app.route("/loginUser/", methods=["POST"])
def loginUser():
	name=request.form["name"]
	print name, checkUser(name)
	if ( checkUser(name) ): 
		response = { "password" : getUser(name)["password"], "id": getUser(name)["id"], "name": getUser(name)["name"], "exp": getUser(name)["exp"], "weekly_exp" : getUser(name)["weekly_exp"], "level" : getUser(name)["level"] }
		return jsonify(response)
	
	return False;

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
		app.run(port=5002)