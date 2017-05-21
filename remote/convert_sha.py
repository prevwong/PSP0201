from flask import Flask
from server import app, query_db, update_user
import hashlib

def password_hash(string):
    hash_obj = hashlib.sha256(string.encode())
    return hash_obj.hexdigest()

def convert_to_sha():
    update_user("1", {"password": str(password_hash("testing123"))})

if __name__ == "__main__":
	with app.app_context():
		convert_to_sha();
