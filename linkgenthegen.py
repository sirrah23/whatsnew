import bitly_api
import json
import requests
import sendgrid
import pymongo

s = sendgrid.Sendgrid('Goose23','sendgridiscool', secure = True)


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
	return links + summaries

#links()

def main():
	con = pymongo.MongoClient()
	e = con.app.emails.find()
	m = sendgrid.Message("hseth93@gmail.com", "What's New Today", message, "")
	for email in e:
		print email['email']
		m.add_to(email['email'], email['name'])
	s.web.send(m)

main()
