import os
import subprocess
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8998795222:AAF_TUI7vT4dSHp28gjUQoTxDwTeH4SMjD4"
ADMIN_ID = 8903693040
bot = telebot.TeleBot(TOKEN)

# Channels Config
CHANNEL_1_ID = -1004348616526
CHANNEL_1_LINK = "https://t.me/+Mi0ELzGRzChmOTBl"

CHANNEL_2_ID = -1004479477443
CHANNEL_2_LINK = "https://t.me/+_lgMP6V9O7thZmY1"

HOST_DIR = "hosted_bots"
PENDING_DIR = "pending_bots"

for d in [HOST_DIR, PENDING_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

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

def get_permanent_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("📥 Upload File"), KeyboardButton("📦 PIP Upload"))
    markup.row(KeyboardButton("📁 My Bots"), KeyboardButton("📊 My Files"))
    markup.row(KeyboardButton("📜 My History"), KeyboardButton("🗑️ Delete Bot"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_user_joined(user_id):
        welcome_msg = (
            "WELCOME ❤️ HOSTING BOT 24/7 ACTIVE ✅\n\n"
            "Aapka verification successful ho gaya hai!\n"
            "Neeche permanent menu se option select karein:"
        )
        bot.reply_to(message, welcome_msg, reply_markup=get_permanent_menu())
    else:
        ask_join_text = (
            "WELCOME ❤️ HOSTING BOT 24/7 ACTIVE ✅\n\n"
            "PLEASE CHANNEL JOIN 🤨 START BOT ❤️‍🩹\n\n"
            "Pehle dono channels join karein aur phir 'VERIFY NOW' par click karein!"
        )
        bot.reply_to(message, ask_join_text, reply_markup=get_join_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def handle_verification(call):
    user_id = call.from_user.id
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
        bot.delete_message(call.message.chat.id, msg.message_id)
        final_msg = (
            "VERIFICATION SUCCESSFUL! 🎉\n\n"
            "WELCOME ❤️ HOSTING BOT 24/7 ACTIVE ✅\n\n"
            "Ab aap niche diye gaye permanent buttons se apne bots manage kar sakte hain:"
        )
        bot.send_message(call.message.chat.id, final_msg, reply_markup=get_permanent_menu())
    else:
        bot.answer_callback_query(call.id, "Aapne abhi tak dono channels join nahi kiye hain!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_text_menu(message):
    user_id = message.from_user.id
    text = message.text

    if not is_user_joined(user_id):
        bot.reply_to(message, "PLEASE CHANNEL JOIN 🤨 START BOT ❤️‍🩹", reply_markup=get_join_keyboard())
        return

    if text == "📥 Upload File":
        bot.reply_to(message, "Ab apni .py (Python) file direct chat me send karo, wo admin approval ke liye chali jayegi!")

    elif text == "📦 PIP Upload":
        bot.reply_to(message, "Ab apni requirements.txt file send karo, admin approval ke baad libraries install ho jayengi!")

    elif text == "📁 My Bots":
        dead_keys = []
        for k, p in running_processes.items():
            if k.startswith(f"{user_id}_") and p.poll() is not None:
                dead_keys.append(k)
        for dk in dead_keys:
            del running_processes[dk]

        user_active = [k.split('_', 1)[1] for k in running_processes.keys() if k.startswith(f"{user_id}_")]
        if user_active:
            resp = "AAPKE ACTIVE LIVE BOTS:\n\n" + "\n".join([f"• {fn}" for fn in user_active])
        else:
            resp = "Aapka koi bhi bot abhi live nahi chal raha hai."
        bot.reply_to(message, resp)

    elif text == "📊 My Files":
        user_folder = os.path.join(HOST_DIR, str(user_id))
        if os.path.exists(user_folder):
            files = os.listdir(user_folder)
            if files:
                resp = "AAPKI HOSTED FILES:\n\n" + "\n".join([f"• {f}" for f in files])
            else:
                resp = "Aapne abhi koi file upload nahi ki hai."
        else:
            resp = "Aapka folder khali hai."
        bot.reply_to(message, resp)

    elif text == "📜 My History":
        hist = user_history.get(user_id, [])
        if hist:
            resp = "AAPKI HOSTING HISTORY:\n\n" + "\n".join([f"• {h}" for h in hist])
        else:
            resp = "Koi history nahi mili."
        bot.reply_to(message, resp)

    elif text == "🗑️ Delete Bot":
        user_active = [k.split('_', 1)[1] for k in running_processes.keys() if k.startswith(f"{user_id}_")]
        if user_active:
            markup = InlineKeyboardMarkup()
            for fn in user_active:
                markup.add(InlineKeyboardButton(f"❌ Stop & Delete {fn}", callback_data=f"del_{fn}"))
            bot.reply_to(message, "Jis bot ko delete/stop karna hai uspar click karein:", reply_markup=markup)
        else:
            bot.reply_to(message, "Delete karne ke liye koi active bot nahi hai.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_"))
def handle_delete_callback(call):
    user_id = call.from_user.id
    file_name = call.data.replace("del_", "")
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

# User uploads document (.py or requirements.txt) -> Sends to Admin for approval
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
    if not (file_name.endswith('.py') or file_name == 'requirements.txt'):
        bot.reply_to(message, "Sirf .py (Python) files ya requirements.txt allowed hain!")
        return

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        pending_user_dir = os.path.join(PENDING_DIR, str(user_id))
        os.makedirs(pending_user_dir, exist_ok=True)
        pending_path = os.path.join(pending_user_dir, file_name)

        with open(pending_path, 'wb') as f:
            f.write(downloaded_file)

        admin_markup = InlineKeyboardMarkup()
        admin_markup.add(
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}_{file_name}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}_{file_name}")
        )

        file_type_label = "PYTHON BOT FILE" if file_name.endswith('.py') else "PIP REQUIREMENTS FILE"
        caption = (
            f"📥 NEW {file_type_label} APPROVAL REQUEST\n\n"
            f"👤 User ID: {user_id}\n"
            f"📁 File Name: {file_name}\n\n"
            f"Approve ya Reject karne ke liye neeche click karein:"
        )

        bot.send_document(
            ADMIN_ID,
            message.document.file_id,
            caption=caption,
            reply_markup=admin_markup
        )

        bot.reply_to(message, f"⚡ Aapki file {file_name} Admin ke paas approval ke liye bhej di gayi hai!")

    except Exception as e:
        bot.reply_to(message, f"Error sending file for approval: {str(e)}")

# Real Admin Approval Handler
@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def handle_admin_approval(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Aap admin nahi hain!", show_alert=True)
        return

    data = call.data
    action, rest = data.split("_", 1)
    parts = rest.split("_", 1)
    target_user_id = int(parts[0])
    file_name = parts[1]

    pending_path = os.path.join(PENDING_DIR, str(target_user_id), file_name)

    if action == "approve":
        if not os.path.exists(pending_path):
            bot.answer_callback_query(call.id, "File pending folder me nahi mili!", show_alert=True)
            return

        user_folder = os.path.join(HOST_DIR, str(target_user_id))
        os.makedirs(user_folder, exist_ok=True)
        target_path = os.path.join(user_folder, file_name)

        # Move file to active hosted folder
        os.rename(pending_path, target_path)

        if file_name == "requirements.txt":
            try:
                subprocess.run(["pip", "install", "-r", target_path], check=True)
                bot.answer_callback_query(call.id, "Requirements successfully installed!", show_alert=True)
            except Exception as e:
                bot.answer_callback_query(call.id, f"Pip error: {e}", show_alert=True)
        else:
            process_key = f"{target_user_id}_{file_name}"
            if process_key in running_processes:
                try:
                    running_processes[process_key].terminate()
                except:
                    pass

            # REALLY START THE BOT PROCESS HERE
            process = subprocess.Popen(["python3", target_path])
            running_processes[process_key] = process

            if target_user_id not in user_history:
                user_history[target_user_id] = []
            user_history[target_user_id].append(f"Hosted: {file_name} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

            bot.answer_callback_query(call.id, "Bot Approved & Deployed Successfully!", show_alert=True)

        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=f"✅ APPROVED & DEPLOYED LIVE\n\nUser ID: {target_user_id}\nFile: {file_name}"
        )

        try:
            bot.send_message(
                target_user_id,
                f"🎉 Aapki file {file_name} Admin dwara Approve ho gayi hai!\n\nStatus: Active & Running 24/7 🚀"
            )
        except Exception as e:
            print(f"Failed to notify user: {e}")

    elif action == "reject":
        if os.path.exists(pending_path):
            os.remove(pending_path)

        bot.answer_callback_query(call.id, "File Rejected!", show_alert=True)
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=f"❌ REJECTED\n\nUser ID: {target_user_id}\nFile: {file_name}"
        )

        try:
            bot.send_message(
                target_user_id,
                f"❌ Aapki file {file_name} Admin dwara Reject kar di gayi hai."
            )
        except Exception as e:
            print(f"Failed to notify user: {e}")

print("Real Bot Deployment Engine Live...")
bot.infinity_polling()
    
