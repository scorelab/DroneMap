import sys
import pymongo


def connect(uri):
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    return db


def insert(db, documentName, dataArray):
    document = db[documentName]
    val = document.insert(dataArray)
    if (val):
        print("Successed!")
    else:
        print("Something went wrong.")


def read(db):
    try:
        data_column = db.data1.find()
        for d in data_column:
            print d
    except Exception, e:
        print str(e)