import time
import random
import requests
import yaml
from pymongo import MongoClient

def main():
        print 'Connection to Mongo..'
	connection = MongoClient()
	db = connection.iarchive
	collection = db.congressmen

        print 'Loading list of Congressmen...'
        with open('legislators-current.yaml','r') as stream:
		congress = yaml.load(stream)
        print '..done.'

	congressmen = []
	for person in congress:
		name = person['name']['first'] + ' ' + person['name']['last']
		if isinstance(name, unicode):
			congressmen.append(person['name']['official_full'])
		else:
			congressmen.append(name)

	url = 'http://archive.org/details/tv'

        continuing = False
	for member in congressmen:
                print 'Querying for ' + member + '...'
		i = 1
		while i:
			time.sleep(random.randint(3,5)) #let's not be rude
                        if continuing:
                                time.sleep(60)
                        payload = {'rows':10, 'start':i, 'output':'json', 'time':'20090604-20130101', 'q':member} #consider &network eventually
			r = requests.get(url, params=payload)
                        if r.status_code != 200:
                                print 'Request url (Status code ' + r.status_code
                                +'): ' + r.url
                                print 'Response content: \n' +  r.content
                                if continuing:
                                        print 'Failed twice on ' + r.url
                                continuing = True
                                continue
                        else if r.json():
                                continuing = False
                                for post in r.json():
				        post['congressman'] = member
        				post['rownum'] = i
	        			collection.insert(post)
				i += 10
			else:
			        break	
if __name__ == "__main__":
	main()
