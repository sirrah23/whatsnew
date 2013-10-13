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

	for i in range (0,10):
		terms.append(' '.join(json.get('data').get('top_terms').get('news')[i].get('grams')))
		
	for term in terms:
		print term

	print '\n'

	con = bitly_api.Connection(access_token = "dfc9172d3faf9e940c5c10f3c40f50ac8a2e9093")
	linksummary = []

	for term in terms:
		appendthis = con.search(query = term, limit = 1)[0]
		linksummary.append((appendthis.get('summaryTitle').replace('<B>',"")).replace('</B>',""))
		linksummary.append(appendthis.get('aggregate_link'))

		
	'''
	for i in range (0,6):
		print linksummary[i]
		print '\n'
	'''		
	return linksummary

def messagecreator(linksum):
	message = ""
	for i in range(0,20):
		message = message + linksum[i] + '\n' + '\n' 
	return message

def main(message):
	con = pymongo.MongoClient()
	e = con.app.emails.find()
	for email in e:
		print email['email']
		message2 = "Hello"+ ' ' +  email['name'] + ",\nHere's some cool stuff that's been happening.\n" + '\n' +  message
		m = sendgrid.Message("whatsnew93@gmail.com", "What's New Today", message2, "")
		m.add_to(email['email'], email['name'])
	s.web.send(m)

linksummary = links()
message = messagecreator(linksummary)
print message
main(message)
