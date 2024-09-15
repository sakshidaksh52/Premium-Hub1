import os
import sys

# Environment variables for configuration
TOKEN = os.environ.get('TOKEN')
OWNER_ID = int(os.environ.get('OWNER_ID'))
ADMINS = [int(x) for x in os.environ.get('ADMINS').split(',')]
ADMINS.append(OWNER_ID)
PRIVATE_GROUP_ID = int(os.environ.get('PRIVATE_GROUP_ID'))
LOG_CHANNEL_ID = int(os.environ.get('LOG_CHANNEL_ID'))
CALLURL = os.environ.get('WEBHOOK_URL')
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))
CONSOLE_CHANNEL_ID = os.environ.get('CONSOLE_CHANNEL_ID')
MONGO_URI = os.environ.get('MONGO_URI')

# Allowed Private Channel IDs
ALLOWED_PRIVATE_CHANNEL_IDS = [int(x) for x in os.environ.get('ALLOWED_PRIVATE_CHANNEL_IDS', '').split(',') if x]

if not TOKEN or not MONGO_URI:
    sys.exit("TOKEN or MONGO_URI environment variable is not set.")
