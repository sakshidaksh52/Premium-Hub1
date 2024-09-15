from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
from config import MONGO_URI, CONSOLE_CHANNEL_ID
from bot import bot

# Initialize MongoDB client with SSL configuration
client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client['telegram_bot']
users_collection = db['users']
file_storage_collection = db['file_storage']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    bot.send_message(CONSOLE_CHANNEL_ID, "Pinged your deployment. You successfully connected to MongoDB!", parse_mode="HTML")
except Exception as e:
    bot.send_message(CONSOLE_CHANNEL_ID, f"Failed to connect to MongoDB: {e}", parse_mode="HTML")

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
