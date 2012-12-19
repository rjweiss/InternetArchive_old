import time
import random
import requests
import yaml
from pymongo import MongoClient

def main():
	connection = MongoClient()
	db = connection.archive
	collection = db.congressmen

	with open('legislators-current.yaml','r') as stream:
		congress = yaml.load(stream)

	#congressmen = [person['name']['first'] + ' ' + person['name']['last'] for person in congress]
	#congressmen = [person['name']['official_full'] for person in congress]#

	congressmen = []
	for person in congress:
		name = person['name']['first'] + ' ' + person['name']['last']
		if isinstance(name, unicode):
			congressmen.append(person['name']['official_full'])
		else:
			congressmen.append(name)

	url = 'http://archive.org/details/tv'

	for member in congressmen:
		i = 1
		while i:
			time.sleep(random.randint(1,3)) #let's not be rude
			payload = {'rows':1, 'start':i, 'output':'json', 'time':'20090604-20130101', 'q':member} #consider &network eventually
			r = requests.get(url, params=payload)
			if r.json():
				post = r.json()[0]
				post['congressman'] = member
				post['rownum'] = i
				collection.insert(post)
				i += 1
			else:
				i = False
				
if __name__ == "__main__":
	main()