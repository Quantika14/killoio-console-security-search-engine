from pymongo import MongoClient
import bson 

conection = MongoClient('localhost')
db = conection.killoDB

#Insert data into database
def insert_mongodb(data):
	try:
		cursor = db.killoSEC.update({'url':data["link"]}, data , True)
	except:
		print "[WARNING]ERROR INSERT MONGODB"

#Get links to the DB 
def get_link(ids):
	try:
		cursor = db.killoSEC.find({'_id':bson.ObjectId(oid=str(ids))})
		for curso in cursor:
			cursor_int=curso.get('link')
			return True, curso
		return False
	except:
		return False

def get_id(link):
	try:
		cursor = db.killoSEC.find({'link': link} )
		for curso in cursor:
			c = curso.get('_id')
			return c
	except:
		print "[WARNING] ERROR GET ID"
