import pymongo

client = pymongo.MongoClient("link to the remote database/dbname") # defaults to port 27017

db = client.db_name

# print the number of documents in a collection
print db.collection_name.count()