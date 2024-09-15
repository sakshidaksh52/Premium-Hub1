import time
import uuid
import telebot
from telebot import types
from config import TOKEN, OWNER_ID, FORCE_SUB_CHANNEL
from db import save_user, save_file_storage, load_file_storage

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

def set_webhook_with_retry(url, max_retries=5, backoff_factor=2):
    for attempt in range(max_retries):
        try:
            bot.set_webhook(url=url, drop_pending_updates=False)
            break
        except telebot.apihelper.ApiTelegramException as e:
            if e.error_code == 429:
                retry_after = e.result_json['parameters']['retry_after']
                time.sleep(retry_after)
            else:
                if attempt < max_retries - 1:
                    time.sleep(backoff_factor ** attempt)
                else:
                    sys.exit(1)

@bot.message_handler(commands=['start'])
def handle_start(message):
    args = message.text.split()
    save_user(message.chat.id)
    if FORCE_SUB_CHANNEL != 0 and not user_joined_force_channel(message.chat.id):
        send_force_subscribe_message(message)
        return
    if len(args) > 1:
        unique_id = args[1]
        send_file_by_id(message, unique_id)
    else:
        send_welcome_message(message)

def user_joined_force_channel(user_id):
    try:
        if user_id == OWNER_ID:
            return True
        user = bot.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        return user.status in ['member', 'administrator']
    except Exception as e:
        return False

def send_force_subscribe_message(message):
    bot.send_message(
        message.chat.id,
        "*You need to join our compulsory channel😇 \n\nClick the link below to join 🔗 :*",
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Join Channel", url=f"https://t.me/{bot.get_chat(FORCE_SUB_CHANNEL).username}")]]
        ),
        parse_mode="Markdown"
    )

def send_file_by_id(message, unique_id):
    file_info = load_file_storage(unique_id)
    if file_info:
        send_file(message.chat.id, file_info['file_id'], file_info['file_type'])
    else:
        bot.send_message(message.chat.id, "File not found.")

def send_file(chat_id, file_id, file_type):
    if file_type == 'photo':
        bot.send_photo(chat_id, file_id, protect_content=True)
    elif file_type == 'video':
        bot.send_video(chat_id, file_id, protect_content=True)
    elif file_type == 'document':
        bot.send_document(chat_id, file_id, protect_content=True)
    elif file_type == 'audio':
        bot.send_audio(chat_id, file_id, protect_content=True)
    elif file_type == 'voice':
        bot.send_voice(chat_id, file_id, protect_content=True)
    else:
        bot.send_message(chat_id, "Unsupported file type.")
