
import os
import subprocess
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8998795222:AAGI_enlw97EfIjt_ntxcBvCj6VFDT1l30g"
ADMIN_ID = 8903693040
bot = telebot.TeleBot(TOKEN)

# Channels Config
CHANNEL_1_ID = -1004348616526
CHANNEL_1_LINK = "https://t.me/+Mi0ELzGRzChmOTBl"

CHANNEL_2_ID = -1004479477443
CHANNEL_2_LINK = "https://t.me/+_lgMP6V9O7thZmY1"

HOST_DIR = "hosted_bots"
if not os.path.exists(HOST_DIR):
    os.makedirs(HOST_DIR)

running_processes = {}
user_history = {}

def is_user_joined(user_id):
    try:
        member1 = bot.get_chat_member(CHANNEL_1_ID, user_id)
        member2 = bot.get_chat_member(CHANNEL_2_ID, user_id)
        valid_statuses = ['creator', 'administrator', 'member', 'restricted']
        return (member1.status in valid_statuses) and (member2.status in valid_statuses)
    except Exception as e:
        print(f"Check Error: {e}")
        return False

def get_join_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 JOIN CHANNEL 1", url=CHANNEL_1_LINK))
    markup.add(InlineKeyboardButton("📢 JOIN CHANNEL 2", url=CHANNEL_2_LINK))
    markup.add(InlineKeyboardButton("✅ VERIFY NOW", callback_data="check_join"))
    return markup

def get_main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📥 Upload File", callback_data="menu_upload"))
    markup.add(
        InlineKeyboardButton("📁 My Bots", callback_data="menu_mybot"),
        InlineKeyboardButton("📊 My Files", callback_data="menu_myfile")
    )
    markup.add(
        InlineKeyboardButton("📜 My History", callback_data="menu_history"),
        InlineKeyboardButton("🗑️ Delete Bot", callback_data="menu_delete")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_user_joined(user_id):
        welcome_msg = (
            "WELCOME ❤️ HOSTING BOT 24/7 ACTIVE ✅\n\n"
            "Aapka verification successful ho gaya hai!\n"
            "Neeche diye gaye options me se select karein:"
        )
        bot.reply_to(message, welcome_msg, reply_markup=get_main_menu())
    else:
        ask_join_text = (
            "WELCOME ❤️ HOSTING BOT 24/7 ACTIVE ✅\n\n"
            "PLEASE CHANNEL JOIN 🤨 START BOT ❤️‍🩹\n\n"
            "Pehle dono channels join karein aur phir 'VERIFY NOW' par click karein!"
        )
        bot.reply_to(message, ask_join_text, reply_markup=get_join_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    data = call.data

    if data == "check_join":
        if is_user_joined(user_id):
            msg = bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="VERIFICATION STARTED...\n[▒▒▒▒▒▒▒▒▒▒] 0%"
            )
            for i in range(20, 101, 20):
                time.sleep(0.3)
                filled = '█' * (i // 10)
                empty = '▒' * (10 - (i // 10))
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=msg.message_id,
                    text=f"CHECKING MEMBERSHIP & SECURITY...\n[{filled}{empty}] {i}%"
                )
            
            time.sleep(0.5)
            final_msg = (
                "VERIFICATION SUCCESSFUL! 🎉\n\n"
                "WELCOME ❤️ HOSTING BOT 24/7 ACTIVE ✅\n\n"
                "Ab aap apne bots manage kar sakte hain:"
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=msg.message_id,
                text=final_msg,
                reply_markup=get_main_menu()
            )
        else:
            bot.answer_callback_query(call.id, "Aapne abhi tak dono channels join nahi kiye hain!", show_alert=True)

    elif data == "menu_upload":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Ab apni .py (Python) file direct chat me send karo, main usko automatically host kar dunga!")

    elif data == "menu_mybot":
        bot.answer_callback_query(call.id)
        user_active = [k.split('_', 1)[1] for k in running_processes.keys() if k.startswith(f"{user_id}_")]
        if user_active:
            text = "AAPKE ACTIVE LIVE BOTS:\n\n"
            for fn in user_active:
                text += f"• {fn}\n"
        else:
            text = "Aapka koi bhi bot abhi live nahi chal raha hai."
        bot.send_message(call.message.chat.id, text)

    elif data == "menu_myfile":
        bot.answer_callback_query(call.id)
        user_folder = os.path.join(HOST_DIR, str(user_id))
        if os.path.exists(user_folder):
            files = os.listdir(user_folder)
            if files:
                text = "AAPKI HOSTED FILES:\n\n"
                for f in files:
                    text += f"• {f}\n"
            else:
                text = "Aapne abhi koi file upload nahi ki hai."
        else:
            text = "Aapka folder khali hai."
        bot.send_message(call.message.chat.id, text)

    elif data == "menu_history":
        bot.answer_callback_query(call.id)
        hist = user_history.get(user_id, [])
        if hist:
            text = "AAPKI HOSTING HISTORY:\n\n" + "\n".join([f"• {h}" for h in hist])
        else:
            text = "Koi history nahi mili."
        bot.send_message(call.message.chat.id, text)

    elif data == "menu_delete":
        bot.answer_callback_query(call.id)
        user_active = [k.split('_', 1)[1] for k in running_processes.keys() if k.startswith(f"{user_id}_")]
        if user_active:
            markup = InlineKeyboardMarkup()
            for fn in user_active:
                markup.add(InlineKeyboardButton(f"❌ Stop & Delete {fn}", callback_data=f"del_{fn}"))
            bot.send_message(call.message.chat.id, "Jis bot ko delete/stop karna hai uspar click karein:", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "Delete karne ke liye koi active bot nahi hai.")

    elif data.startswith("del_"):
        file_name = data.replace("del_", "")
        process_key = f"{user_id}_{file_name}"
        if process_key in running_processes:
            try:
                running_processes[process_key].terminate()
                del running_processes[process_key]
                bot.answer_callback_query(call.id, f"{file_name} ko delete aur stop kar diya gaya hai!", show_alert=True)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{file_name} successfully stop aur delete ho gaya hai.")
            except Exception as e:
                bot.answer_callback_query(call.id, f"Error: {e}", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "File nahi mili ya pehle se band hai.", show_alert=True)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    if not is_user_joined(user_id):
        ask_join_text = (
            "WELCOME ❤️ HOSTING BOT 24/7 ACTIVE ✅\n\n"
            "PLEASE CHANNEL JOIN 🤨 START BOT ❤️‍🩹"
        )
        bot.reply_to(message, ask_join_text, reply_markup=get_join_keyboard())
        return

    file_name = message.document.file_name
    if not file_name.endswith('.py'):
        bot.reply_to(message, "Sirf .py (Python) files allowed hain!")
        return

    # Hacker style 1 to 100 loading animation for file deployment
    msg = bot.reply_to(message, f"⚡ HACKER DEPLOYMENT STARTED FOR `{file_name}`...\n`[▒▒▒▒▒▒▒▒▒▒] 0%`", parse_mode="Markdown")
    for i in range(20, 101, 20):
        time.sleep(0.3)
        filled = '█' * (i // 10)
        empty = '▒' * (10 - (i // 10))
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg.message_id,
            text=f"⚡ DEPLOYING & INSTALLING DEPENDENCIES...\n`[{filled}{empty}] {i}%`",
            parse_mode="Markdown"
        )

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

        if user_id not in user_history:
            user_history[user_id] = []
        user_history[user_id].append(f"Hosted: {file_name} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        success_text = (
            "FILE SUCCESSFULLY LIVE HO GAYI! 🎉\n\n"
            f"File Name: {file_name}\n"
            "Status: Active & Running 24/7"
        )
        bot.edit_message_text(
            success_text,
            chat_id=message.chat.id,
            message_id=msg.message_id,
            reply_markup=get_main_menu()
        )

    except Exception as e:
        bot.edit_message_text(f"Hosting Error: {str(e)}", chat_id=message.chat.id, message_id=msg.message_id)

print("Bot Admin ID Aur Hacker Animation Ke Saath Live Ho Gaya Hai...")
bot.infinity_polling()
