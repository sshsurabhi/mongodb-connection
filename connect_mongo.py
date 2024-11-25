from pymongo import MongoClient

client = MongoClient(
    host="127.0.0.1",
    port = 27017,
    username = "datascientest",
    password = "dst123"
)

print(client.list_database_names())

sample = client["sample"]
c_zips = sample["zips"]
# we can write like this also 
# c_zips = client["sample"]["zips"]

print(c_zips.find_one())

# rand_ = sample.create_collection(name="rand_")

# # We can check the creation of the collection with this 
# print(sample.list_collection_names())

# data = [
#   {"name": "Melthouse","bread":"Wheat","sauce": "Ceasar"},
#   {"name": "Italian BMT", "extras": ["pickles","onions","lettuce"],"sauce":["Chipotle", "Aioli"]},
#   {"name": "Steakhouse Melt","bread":"Parmesan Oregano"}, 
#   {"name": "Germinal", "author":"Emile Zola"}, 
#   {"pastry":"cream puff","flavour":"chocolate","size":"big"}
# ]

# rand_.insert_many(data)


# print(rand_)

for i in list(zips.find({},{"_id":0,"city":1})):
    print(i)