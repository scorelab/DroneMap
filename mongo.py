#!/bin/python
import sys
import pymongo

def connect(uri):
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    return db

def insert(db,documentName,dataArray):
    document=db[documentName]
    val=document.insert(dataArray)
    if(val):
        print("Successed!")
    else:
        print("Something went wrong.")
        
def read(db):
    try:
        empCol = db.data1.find()
        for d in empCol:
            print d
    except Exception, e:
        print str(e)

def main():
    data = {
    "lon" : 25.225,
    "lat" : 45.222,
    "hei" : 25,
    "name" : "drone_1",
    "id" : "ucscdr_0001"
    }
    MONGODB_URI = 'mongodb://lasithniro:1234@ds159737.mlab.com:59737/dronedb'
    db=connect(MONGODB_URI)
    #insert(db,'data1',data)
    a=read(db)
    print(a)

if __name__ == "__main__":
    main()