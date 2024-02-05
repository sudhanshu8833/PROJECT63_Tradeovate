from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
# Replace the connection string and client instantiation with your MongoDB server details
data = {}
with open("datamanagement/helpful_scripts/background.json") as json_file:
    data = json.load(json_file)
mongo_uri = "mongodb+srv://jonas_peres:project63_tradeovate@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(
    mongo_uri, server_api=ServerApi('1'), connect=False)


# print(client.list_database_names())
database = client['sudhanshu']
coll = database['admin']
print(coll.find_one())
# Connect to the admin database
# admin_db = client.admin

# # Replace 'admin_username' and 'admin_password' with the credentials for the admin user
# admin_username = 'sudhanshu8833'
# admin_password = 'Madhya246###'

# # Create a user in the admin database
# admin_db.command('createUser', admin_username, pwd=admin_password, roles=['userAdminAnyDatabase'])


# # Now connect to the target database where you want to grant access
# target_db = client['your_database']

# # Replace 'target_username' and 'target_password' with the credentials for the target user
# target_username = 'target_username'
# target_password = 'target_password'

# # Create a user in the target database and grant specific roles
# target_db.add_user(target_username, target_password, roles=[
#     {'role': 'readWrite', 'db': 'your_database'}
# ])

# # Close the connection to the target database
# client.close()
