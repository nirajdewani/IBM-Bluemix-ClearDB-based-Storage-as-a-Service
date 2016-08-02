# -*- coding: utf-8 -*-
import MySQLdb
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import hashlib

app = Flask(__name__)
gUserName = ""
db = MySQLdb.connect(hostIP, DBusername, DBpassword, DBname)
cursor = db.cursor()

def getFiles(userName):
	query = ("SELECT fileName FROM file WHERE userName = '{0}'").format(userName)
	cursor.execute(query)
	fileList = cursor.fetchall()
	return fileList

def insertFile(fileName, description, hash, userName):
	query = ("INSERT INTO file (fileName, description, hash, userName) VALUES ('{0}', '{1}', '{2}', '{3}')").format(fileName, description, hash, userName)
	cursor.execute(query)
	db.commit()

@app.route('/authenticate', methods=['POST'])
def authenticate():
	global gUserName
	userName = str(request.form["userName"])
	password = str(request.form["password"])
	query = ("SELECT userName FROM credential WHERE userName = '{0}' AND password = '{1}'").format(userName, password)
	cursor.execute(query)
	retrievedUserName = cursor.fetchone()
	
	if type(retrievedUserName) is not 'NoneType':
		fileList = getFiles(userName)
		gUserName = userName
		if str(len(fileList)) == 0:
			return render_template("files.html", fileList=fileList, userName=userName)
		else:
			return render_template("upload.html", userName=userName)
	else:
		return False
	
@app.route('/uploadFile', methods=['POST'])
def uploadFile():
	global gUserName
	f = request.files['file']
	content = f.read()
	hashObject = hashlib.md5(content)
	
	fileList = getFiles(gUserName)
	return render_template("files.html", fileList=fileList)

@app.route('/insertUser', methods=['POST'])
def insertUser():
	userName = str(request.form["userName"])
	password = str(request.form["password"])
	query = ("INSERT INTO credential (userName, password) VALUES ('{0}', '{1}')").format(userName, password)
	cursor.execute(query)
	db.commit()
	return render_template("upload.html", userName=userName)

@app.route('/index', methods=['GET'])
def index():
	return render_template("index.html")	
	
@app.route('/signup')
def signup():
	return render_template("signup.html")

def main():
	app.run(debug=True)
	
if __name__=='__main__':main()


