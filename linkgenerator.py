from pymongo import MongoClient
from flask import Flask
import flask

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
	if flask.request.method == 'GET':
		return flask.render_template('index.html')
	elif flask.request.method == 'POST':
		email = flask.request.form.get('email')
		name = flask.request.form.get('name')
		conn = MongoClient()
		conn.app.emails.insert({'email': email, 'name': name})
		return email

@app.route('/emails') 
def emails():
	conn = MongoClient()
	e = conn.app.emails.find()
	return '<br>'.join([em['name'] + ' ' + em['email'] for em in e])



if __name__ == '__main__': 
	app.debug = True
	app.run()
