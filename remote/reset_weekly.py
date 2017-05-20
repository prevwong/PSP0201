from flask import Flask
from server import app, query_db, update_user

def reset_weekly():
	users = {}
	data = query_db("select * from users")
	if ( data != None ) :
		# If no error
		for user in data:
			try:
				# Update the user's exp, given their id
				update_user(user["id"], {"weekly_exp" : 0})
				print "Successfully reset every user's weekly_exp"
			except:
				# error, print an error message in the console
				print "Error, cannot reset weekly exp"
	else:
		# Error
		print "Error, cannot reset weekly exp"

if __name__ == "__main__":
	with app.app_context():
		reset_weekly()
