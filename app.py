from flask import Flask, request, abort
from bot import bot, set_webhook_with_retry
from db import check_mongo_connection
from config import CALLURL, CONSOLE_CHANNEL_ID

# Initialize Flask app
app = Flask(__name__)

# Remove any existing webhook and set a new one
bot.remove_webhook()
set_webhook_with_retry(CALLURL)

# Check MongoDB connection (now with passing the bot instance)
check_mongo_connection(bot, CONSOLE_CHANNEL_ID)

@app.route('/')
def host():
    base_url = request.base_url
    return f"The HOST URL of this application is: {base_url}"

@app.route('/', methods=['POST'])
def receive_updates():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data(as_text=True)
        update = bot.types.Update.de_json(json_string)
        if update is not None:
            bot.process_new_updates([update])
        return '', 200
    else:
        abort(403)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
