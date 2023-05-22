import pymongo

myclient = pymongo.MongoClient("mongodb+srv://finnwaehlt:2103w9II@cluster0.ps1kys4.mongodb.net/")
mydb = myclient["dev3"]
mycol = mydb["test"]

mydict = { "name": "John", "address": "Highway 37" }
x = mycol.find_one()

print(x)

x = mycol.insert_one(mydict)