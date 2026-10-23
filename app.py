import os
import subprocess
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Aapka Naya Bot Token
TOKEN = "8998795222:AAEAUpj2efPF0n0x1KaBamzb_cZ5Ge47RT4"
bot = telebot.TeleBot(TOKEN)

# Channels Config
CHANNEL_1_ID = -1004348616526
CHANNEL_1_LINK = "https://t.me/+Mi0ELzGRzChmOTBl"

CHANNEL_2_ID = -1004479477443
CHANNEL_2_LINK = "https://t.me/+_lgMP6V9O7thZmY1"

# Folder for hosting files
HOST_DIR = "hosted_bots"
if not os.path.exists(HOST_DIR):
    os.makedirs(HOST_DIR)

running_processes = {}

# Helper Function: Check User Subscription
def is_user_joined(user_id):
    try:
        member1 = bot.get_chat_member(CHANNEL_1_ID, user_id)
        member2 = bot.get_chat_member(CHANNEL_2_ID, user_id)
        
        valid_statuses = ['creator', 'administrator', 'member', 'restricted']
        c1 = member1.status in valid_statuses
        c2 = member2.status in valid_statuses
        
        return c1 and c2
    except Exception as e:
        print(f"Check Error: {e}")
        return False

# Join Markup Buttons
def get_join_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1_LINK))
    markup.add(InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2_LINK))
    markup.add(InlineKeyboardButton("VERIFY ✅", callback_data="check_join"))
    return markup

# /start Command Handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if is_user_joined(user_id):
        welcome_text = (
            "WELCOME ❤️ HOSTING BOT 24/7 ⏳ACTIVE ✅\n\n"
            "Verification successful! 🎉\n"
            "Ab mujhe apni Python (`.py`) file bhejo, main usko automatically host karke live kar dunga!\n\n"
            "📜 **Commands:**\n"
            "• `/status` - Active running bots dekhne ke liye\n"
            "• `/stop <filename.py>` - Running bot stop karne ke liye"
        )
        bot.reply_to(message, welcome_text, parse_mode="Markdown")
    else:
        ask_join_text = (
            "WELCOME ❤️ HOSTING BOT 24/7 ⏳ACTIVE ✅\n"
            "PLEASE CHANNEL JOIN 🤨 START BOT❤️‍🩹\n\n"
            "Bot ko use karne ke liye pehle diye gaye dono channels join karo aur phir 'VERIFY ✅' par click karo!"
        )
        bot.reply_to(message, ask_join_text, reply_markup=get_join_keyboard())

# Verify Button Callback
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_callback(call):
    user_id = call.from_user.id
    
    if is_user_joined(user_id):
        bot.answer_callback_query(call.id, "✅ Verification Successful!")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=(
                "WELCOME ❤️ HOSTING BOT 24/7 ⏳ACTIVE ✅\n\n"
                "Aapka Verification Ho Gaya Hai! 🎉\n"
                "Ab apni `.py` file send karo, main automatic host kar dunga!"
            )
        )
    else:
        bot.answer_callback_query(call.id, "❌ Aapne dono channels join nahi kiye hain!", show_alert=True)

# Document / File Upload Handler (Auto Host)
@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    
    if not is_user_joined(user_id):
        ask_join_text = (
            "WELCOME ❤️ HOSTING BOT 24/7 ⏳ACTIVE ✅\n"
            "PLEASE CHANNEL JOIN 🤨 START BOT❤️‍🩹\n\n"
            "File host karne ke liye pehle dono channels join karein!"
        )
        bot.reply_to(message, ask_join_text, reply_markup=get_join_keyboard())
        return

    file_name = message.document.file_name

    if not file_name.endswith('.py'):
        bot.reply_to(message, "❌ Sirf `.py` (Python) files allowed hain!")
        return

    msg = bot.reply_to(message, f"⚡ **{file_name}** downloading & hosting automatically...")

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        user_folder = os.path.join(HOST_DIR, str(user_id))
        os.makedirs(user_folder, exist_ok=True)

        file_path = os.path.join(user_folder, file_name)

        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        process_key = f"{user_id}_{file_name}"
        
        if process_key in running_processes:
            try:
                running_processes[process_key].terminate()
            except:
                pass

        process = subprocess.Popen(["python3", file_path])
        running_processes[process_key] = process

        bot.edit_message_text(
            f"✅ **File Successfully Live Ho Gayi!**\n\n"
            f"📁 **File:** `{file_name}`\n"
            f"🚀 **Status:** Active & Running 24/7",
            chat_id=message.chat.id,
            message_id=msg.message_id,
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.edit_message_text(f"⚠️ Hosting Error: {str(e)}", chat_id=message.chat.id, message_id=msg.message_id)

# Status Command
@bot.message_handler(commands=['status'])
def check_status(message):
    user_id = message.from_user.id
    if not is_user_joined(user_id):
        bot.reply_to(message, "WELCOME ❤️ HOSTING BOT 24/7 ⏳ACTIVE ✅\nPLEASE CHANNEL JOIN 🤨 START BOT❤️‍🩹", reply_markup=get_join_keyboard())
        return

    user_active = [k.split('_', 1)[1] for k in running_processes.keys() if k.startswith(f"{user_id}_")]

    if user_active:
        text = "🟢 **Aapke Active Live Bots:**\n\n"
        for fn in user_active:
            text += f"• `{fn}`\n"
    else:
        text = "🔴 Aapka koi bhi bot abhi live nahi chal raha hai."

    bot.reply_to(message, text, parse_mode="Markdown")

# Stop Command
@bot.message_handler(commands=['stop'])
def stop_script(message):
    user_id = message.from_user.id
    if not is_user_joined(user_id):
        bot.reply_to(message, "WELCOME ❤️ HOSTING BOT 24/7 ⏳ACTIVE ✅\nPLEASE CHANNEL JOIN 🤨 START BOT❤️‍🩹", reply_markup=get_join_keyboard())
        return

    try:
        file_name = message.text.split(" ", 1)[1]
        process_key = f"{user_id}_{file_name}"

        if process_key in running_processes:
            running_processes[process_key].terminate()
            del running_processes[process_key]
            bot.reply_to(message, f"🛑 **{file_name}** stop ho chuki hai.", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Is naam ki koi running file nahi mili.")
    except IndexError:
        bot.reply_to(message, "❌ Usage: `/stop filename.py`", parse_mode="Markdown")

print("🤖 Bot Active Ho Gaya Hai...")
bot.infinity_polling()
  
