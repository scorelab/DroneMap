<<<<<<< HEAD
#Created by Imal thiunuwan using Intellij Idea

import pymongo

client = pymongo.MongoClient("link to the remote database/dbname") # defaults to port 27017

db = client.db_name

# print the number of documents in a collection
=======
#Created by Imal thiunuwan using Intellij Idea

import pymongo

client = pymongo.MongoClient("link to the remote database/dbname") # defaults to port 27017

db = client.db_name

# print the number of documents in a collection
>>>>>>> 26846c361adaea2e3e36788f1b50de57f6e1e958
print db.collection_name.count()