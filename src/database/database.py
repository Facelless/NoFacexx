from pymongo import MongoClient

url = ''
database = MongoClient(url)
cluster = database[""]
collection = cluster[""]