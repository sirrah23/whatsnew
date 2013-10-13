import requests
from pymongo import MongoClient
from flask import Flask
import flask
import bitly_api
import json

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


def links():
	r = requests.get("https://chartbeat.com/labs/rising/topterms/?host=chartbeat.com&apikey=1&tz=-240&_src=cb_dash")
	json = r.json()
	terms = []

	for i in range (0,6):
		terms.append(' '.join(json.get('data').get('top_terms').get('news')[i].get('grams')))
		
	for term in terms:
		print term


	con = bitly_api.Connection(access_token = "dfc9172d3faf9e940c5c10f3c40f50ac8a2e9093")
	links = []
	summaries = []

	for term in terms:
		appendthis = con.search(query = term, limit = 1)[0]
		links.append(appendthis.get('url'))
		summaries.append(appendthis.get('summaryTitle'))

	for i in range (0,6):
		print links[i]
		print summaries[i]
	return 0

if __name__ == '__main__': 
	app.debug = True
	app.run()

