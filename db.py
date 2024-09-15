from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
from config import MONGO_URI

# Initialize MongoDB client with SSL configuration
client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client['telegram_bot']
users_collection = db['users']
file_storage_collection = db['file_storage']

# Send a ping to confirm a successful connection
def check_mongo_connection(bot_instance, console_channel_id):
    try:
        client.admin.command('ping')
        bot_instance.send_message(console_channel_id, "Pinged your deployment. You successfully connected to MongoDB!", parse_mode="HTML")
    except Exception as e:
        bot_instance.send_message(console_channel_id, f"Failed to connect to MongoDB: {e}", parse_mode="HTML")

# Functions to interact with MongoDB collections
def save_user(chat_id):
    try:
        users_collection.update_one(
            {'chat_id': chat_id},
            {'$set': {'chat_id': chat_id}},
            upsert=True
        )
    except Exception as e:
        print(f"Failed to save user {chat_id}: {e}")

def save_file_storage(unique_id, file_info):
    try:
        file_storage_collection.update_one(
            {'unique_id': unique_id},
            {'$set': {'file_id': file_info[0], 'file_type': file_info[1]}},
            upsert=True
        )
    except Exception as e:
        print(f"Failed to save file {unique_id}: {e}")

def load_file_storage(unique_id):
    try:
        return file_storage_collection.find_one({'unique_id': unique_id})
    except Exception as e:
        print(f"Failed to load file {unique_id}: {e}")
        return None
