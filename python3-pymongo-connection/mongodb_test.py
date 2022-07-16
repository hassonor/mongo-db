# Script to test MongoDB connection
# MongoDB Atlas connection string needs to be edited with your connection

from pymongo import MongoClient

uri = "mongodb+src://admindb:xxxxxxxx@cluster0-u7xxx.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(uri)

# switch to mflix database (mongodb Atlas demo database)
mflix = client['sample_mflix']

# list collection names
print('Mflix Collections: ')
for name in mflix.list_collection_names():
    print(name)
