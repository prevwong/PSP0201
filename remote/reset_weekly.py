from flask import Flask, render_template, request, url_for, g, jsonify
from server import app, get_db, query_db, update_user

def reset_weekly():
	users = {}
	data = query_db("select * from users")
	if ( data != None ) :
		# If no error
		for user in data:
			try:
				# Update the user's exp, given their id
				update_user(user["id"], {"weekly_exp" : 0})
			except:
				# error, print an error message in the console
				print "Error, cannot reset weekly exp"
		response = {"success" : True };
	else:
		# Error
		response = { "error" : True }

if __name__ == "__main__":
	with app.app_context():
		reset_weekly()
