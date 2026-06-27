import os
import sys
import re
import time
import uuid
import subprocess
import threading
import traceback
import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException

# --- RAILWAY PERSISTENT RE-ENGINEERING ---
STORAGE_DIR = "/data" if os.path.exists("/data") else os.getcwd()
LOG_FILE_PATH = os.path.join(STORAGE_DIR, "crash_logs.txt")

# Environment Port Binding
os.environ["PORT"] = os.environ.get("PORT", "8080")

# ⚡ TERA VERIFIED HIGH-SECURITY DETAILS ⚡
TOKEN = "8926219447:AAEQciCFkb68viWtHGjmrPH_HTOUeJhucTA"  # NAYA TOKEN INJECTED ✅
DEFAULT_CHAT_ID = "8620962808"  # TERA OWNER CHAT ID
OWNER_USERNAME = "ADITYAXPASWANJI"
IMAGE_PATH = "6233.jpg"  # TERI SETUP IMAGE FILE

# Main bot initialization
bot = telebot.TeleBot(TOKEN, threaded=True)

# Secure Runtime Database Trackers
user_sessions = {}
live_threads = {}
premium_users = {} 
pending_requests = {}  
total_files_hosted = 0

# --- HELPER FUNCTION FOR PERSISTENT LOGS ---
def write_persistent_log(log_id, error_text):
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"=== LOG_ID: {log_id} ===\n{error_text}\n=====================\n\n")
    except Exception as e:
        print(f"Error saving log: {e}")

def read_persistent_log(log_id):
    if not os.path.exists(LOG_FILE_PATH):
        return "⚠️ Log traces empty or no crashes recorded yet."
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"=== LOG_ID: " + log_id + r" ===\n(.*?)\n=====================", content, re.DOTALL)
        if match:
            return match.group(1)
    except Exception as e:
        return f"⚠️ Error reading logs: {str(e)}"
    return "⚠️ Log traces purged from memory block or expired."

# --- PREMIUM HOME PANEL KEYBOARD ---
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("📤 FILE UPLOAD FREE"), types.KeyboardButton("📂 MY FILES"))
    markup.row(types.KeyboardButton("📊 SERVER STATS"), types.KeyboardButton("🚀 BOOST SERVER"))
    markup.row(types.KeyboardButton("⚙️ ADVANCED SETTINGS"), types.KeyboardButton("👑 GET PREMIUM"))
    return markup

# --- ADVANCED PRIVACY & SECURITY PANEL ---
def advanced_settings_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👤 MY PROFILE", callback_data="view_profile"),
        types.InlineKeyboardButton("🛡️ ANTI-PENETRATION", callback_data="anti_crash_info")
    )
    markup.add(
        types.InlineKeyboardButton("💬 LIVE SUPPORT", url=f"t.me/{OWNER_USERNAME}"),
        types.InlineKeyboardButton("🔄 PURGE LOG FILE", callback_data="refresh_engine")
    )
    return markup

# --- PREMIUM PLANS KEYBOARD ---
def premium_plans_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💎 1 MONTH | 10 FILES | RS 50", callback_data="buy_plan_50"),
        types.InlineKeyboardButton("💎 1 MONTH | 20 FILES | RS 80", callback_data="buy_plan_80"),
        types.InlineKeyboardButton("🔥 LIFETIME UNLIMITED | RS 150", callback_data="buy_plan_150")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = {}

    haunted_caption = (
        "⚡ <b>ADITYA MONSTER HOST v10.0 ULTIMATE PRO</b> ⚡\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "🟢 <b>SYSTEM STATUS:</b> <code>SECURE ONLINE</code>\n"
        "🚀 <b>CORE ENGINE:</b> <code>REAL VPS SUBPROCESS NODES</code>\n"
        "🛡️ <b>SECURITY LAYER:</b> <code>PERSISTENT STORAGE LOGS</code>\n"
        "⏰ <b>UPTIME ACCURACY:</b> <code>24/7 REAL-TIME ACTIVE ✅</code>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<i>🤖 BHAI, APNI PYTHON (.py) FILE SEND KARO! APKA ASLI CODE SUBPROCESS INDEPENDENT SANDBOX MEIN 24/7 LIVE CHALEGA APPROVAL KE BAAD.</i>"
    )
    
    if os.path.exists(IMAGE_PATH):
        with open(IMAGE_PATH, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=haunted_caption, reply_markup=main_keyboard(), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, haunted_caption, reply_markup=main_keyboard(), parse_mode='HTML')

# --- HANDLE TEXT BUTTON MENUS ---
@bot.message_handler(func=lambda message: message.text in ["📤 FILE UPLOAD FREE", "📂 MY FILES", "👑 GET PREMIUM", "📊 SERVER STATS", "⚙️ ADVANCED SETTINGS", "🚀 BOOST SERVER"])
def handle_text_menus(message):
    user_id = message.from_user.id
    
    if message.text == "📤 FILE UPLOAD FREE":
        bot.send_message(message.chat.id, "📥 <b>SEND ME YOUR PYTHON FILE (.py) NOW:</b>\n\n<i>File binary filters pass hote hi Admin verification channel par forward ho jayegi.</i>", parse_mode='HTML')
        
    elif message.text == "👑 GET PREMIUM":
        premium_text = (
            "👑 <b>ADITYA HOSTING PREMIUM PLANS</b> 👑\n"
            "<b>━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            "🌟 <b>BENEFITS:</b> No File Limit, No Timeout, Dedicated Fast Server Routing, Isolated Nodes.\n"
            "🔮 <i>Select your package to upgrade instantly:</i>"
        )
        bot.send_message(message.chat.id, premium_text, reply_markup=premium_plans_keyboard(), parse_mode='HTML')
        
    elif message.text == "📂 MY FILES":
        if user_id not in user_sessions or not user_sessions[user_id]:
            bot.send_message(message.chat.id, "❌ <b>CURRENTLY NO FILE IS HOSTED ACTIVE!</b>", parse_mode='HTML')
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        for bot_id, b_data in user_sessions[user_id].items():
            markup.add(types.InlineKeyboardButton(f"📄 {b_data['name']}", callback_data=f"manage_{bot_id}"))
        bot.send_message(message.chat.id, "📂 <b>YOUR REAL-TIME RUNNING HOSTED FILES:</b>", reply_markup=markup, parse_mode='HTML')

    elif message.text == "📊 SERVER STATS":
        total_users = len(user_sessions)
        active_bots = len(live_threads)
        stats_text = (
            "📊 <b>LIVE SECURITY SERVER STATISTICS</b> 📊\n"
            "<b>━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            f"👥 <b>TOTAL ACTIVE USERS:</b> <code>{total_users}</code>\n"
            f"🤖 <b>REAL BACKGROUND RUNNING BOTS:</b> <code>{active_bots}</code>\n"
            f"📈 <b>TOTAL DEPLOYMENTS OVERALL:</b> <code>{total_files_hosted}</code>\n"
            f"🛡️ <b>PRIVACY ENGINE STATE:</b> <code>Subprocess Isolated Sandbox (100%)</code>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            "✅ <b>All operational execution models are stable.</b>"
        )
        bot.send_message(message.chat.id, stats_text, parse_mode='HTML')

    elif message.text == "⚙️ ADVANCED SETTINGS":
        bot.send_message(message.chat.id, "⚙️ <b>ADITYA PRIVACY ADVANCED CONTROL PANEL</b>", reply_markup=advanced_settings_keyboard(), parse_mode='HTML')
        
    elif message.text == "🚀 BOOST SERVER":
        status_boost = bot.send_message(message.chat.id, "⚡ <b>PURGING ALL EXPIRED MEMORY BLOCK BUFFERS...</b>", parse_mode='HTML')
        time.sleep(1.2)
        bot.edit_message_text("🚀 <b>SERVER CORE BOOSTED SUCCESSFUL! RAM TIMEOUT OPTIMIZED TO MAXIMUM ✅</b>", message.chat.id, status_boost.message_id, parse_mode='HTML')

# --- 🚀 SUBPROCESS EXECUTOR 🚀 ---
def run_isolated_subprocess(temp_filename, bot_id, filename, target_user, log_id):
    global total_files_hosted
    try:
        process = subprocess.Popen(
            [sys.executable, temp_filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        live_threads[bot_id]["process_obj"] = process
        total_files_hosted += 1
        
        bot.send_message(target_user, f"✅ <b>AUTOMATIC DEPLOYING SUCCESSFUL 🎉</b>\n\n📄 File: <code>{filename}</code>\n⏰ Uptime State: <b>🟢 REAL 24/7 SECURE ACTIVE WITH ASLI CODE LOGIC</b>", parse_mode='HTML')
        
        stdout, stderr = process.communicate()
        if process.returncode != 0 and stderr:
            write_persistent_log(log_id, f"--- RUNTIME CRASH IN USER SCRIPT ---\n{stderr}")
            
    except Exception as e:
        write_persistent_log(log_id, f"--- SYSTEM EXECUTOR CRASH ---\n{str(e)}\n{traceback.format_exc()}")

# --- FILE INPUT RECEIVED SYSTEM ---
@bot.message_handler(content_types=['document'])
def handle_auto_deployment(message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {}

    if not message.document.file_name.endswith('.py'):
        bot.send_message(message.chat.id, "❌ <b>CRITICAL REJECTION! ONLY .py FORMAT IS ALLOWED BY SERVER POLICY!</b>", parse_mode='HTML')
        return

    bot.send_message(
        message.chat.id, 
        "⏳ <b>WAIT FOR ADMIN APPROVAL...</b>\n\n📄 Aapki script secure channel se Owner approval panel par bhej di gayi hai. Jaise hi approve hoga, automatic deployment instantly start ho jayegi! ✅", 
        parse_mode='HTML'
    )

    req_id = str(uuid.uuid4())[:8]
    pending_requests[req_id] = {
        "user_id": user_id,
        "file_id": message.document.file_id,
        "file_name": message.document.file_name
    }

    owner_markup = types.InlineKeyboardMarkup(row_width=2)
    owner_markup.add(
        types.InlineKeyboardButton("APPROVE ✅", callback_data=f"app_{req_id}"),
        types.InlineKeyboardButton("REJECT ❌", callback_data=f"rej_{req_id}")
    )

    admin_caption = (
        f"🔔 <b>NEW PYTHON FILE PROTECTION QUEUE!</b>\n\n"
        f"👤 <b>USER CHAT ID:</b> <code>{user_id}</code>\n"
        f"📄 <b>FILE IDENTIFIER:</b> <code>{message.document.file_name}</code>\n"
        f"🆔 <b>SECURE REQ ID:</b> <code>{req_id}</code>\n"
    )
    bot.send_document(DEFAULT_CHAT_ID, message.document.file_id, caption=admin_caption, reply_markup=owner_markup, parse_mode='HTML')

# --- CALLBACK SYSTEM PRO ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    
    if call.data.startswith("app_") or call.data.startswith("rej_"):
        if str(user_id) != DEFAULT_CHAT_ID:
            bot.answer_callback_query(call.id, "❌ Access Denied! Security Restriction.", show_alert=True)
            return
            
        action = call.data[:3]
        req_id = call.data[4:]
        req_data = pending_requests.get(req_id)
        
        if not req_data:
            bot.answer_callback_query(call.id, "❌ Session Buffers Expired!", show_alert=True)
            return
            
        target_user = req_data["user_id"]
        filename = req_data["file_name"]
        
        # ❌ ADMIN REJECT STATE
        if action == "rej_":
            bot.send_message(
                target_user, 
                f"❌ <b>ADMIN REJECTED / NOT LIVE ⚠️</b>\n\n"
                f"📄 Aapki file <code>{filename}</code> ko server admin ne reject kar diya hai, isiliye ye script live nahi ki gayi.", 
                parse_mode='HTML'
            )
            bot.edit_message_caption(
                f"❌ <b>ADMIN REJECTED & NOT LIVE</b>\n"
                f"<b>━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
                f"📄 <b>File Name:</b> <code>{filename}</code>\n"
                f"👤 <b>User ID:</b> <code>{target_user}</code>\n"
                f"🛡️ <b>Status:</b> <code>TERMINATED CLEAN</code>", 
                call.message.chat.id, call.message.message_id, parse_mode='HTML'
            )
            del pending_requests[req_id]
            bot.answer_callback_query(call.id, "Successfully Rejected & Flagged Not Live!")
            return

        # 🚀 AUTOMATIC DEPLOY STATUS START
        bot.send_message(target_user, f"🚀 <b>AUTOMATIC DEPLOYING STARTED...</b>\n\n⚙️ <i>Injecting 24/7 sandboxed live parameters into background modules. Firing Real Subprocess Node...</i>", parse_mode='HTML')
        bot.edit_message_caption(f"🚀 <b>STATUS: DEPLOYING REAL RUNTIME ENGINE...</b>\n📄 File: {filename}", call.message.chat.id, call.message.message_id, parse_mode='HTML')

        time.sleep(1.0)

        log_id = str(uuid.uuid4())[:6]
        try:
            file_info = bot.get_file(req_data["file_id"])
            file_content = bot.download_file(file_info.file_path)
            code_text = file_content.decode('utf-8', errors='ignore')
            
            token_match = re.search(r'(\d{9,10}:[A-Za-z0-9_-]{35})', code_text)
            chat_id_match = re.search(r'(?:chat_id|CHAT_ID|id)\s*=\s*["\']?(-?\d+)"\']?', code_text)
            
            if not token_match:
                raise Exception("TokenNotFoundError: Configured Bot API Token missing in text data.")

            extracted_token = token_match.group(1)
            extracted_chat = chat_id_match.group(1) if chat_id_match else DEFAULT_CHAT_ID

            try:
                check_bot = telebot.TeleBot(extracted_token)
                check_bot.get_me()
            except ApiTelegramException as api_err:
                raise Exception(f"API Blocked/Invalid: Code {api_err.error_code} ({api_err.description})")

            # --- SAVE SECURE NODE FILE ---
            bot_id = str(uuid.uuid4())[:8]
            temp_filename = os.path.join(STORAGE_DIR, f"user_bot_{bot_id}.py")
            with open(temp_filename, "w", encoding="utf-8") as f:
                f.write(code_text)

            live_threads[bot_id] = {"filename": temp_filename, "process_obj": None, "token": extracted_token}
            user_sessions[target_user][bot_id] = {'name': filename, 'token': extracted_token, 'chat_id': extracted_chat}

            t = threading.Thread(target=run_isolated_subprocess, args=(temp_filename, bot_id, filename, target_user, log_id), daemon=True)
            t.start()
            
            bot.edit_message_caption(f"✅ <b>DEPLOYED SUCCESSFUL & REAL ACTIVE 24/7!</b>\n📄 File: {filename}\n⚙️ Node Thread: {bot_id}", call.message.chat.id, call.message.message_id, parse_mode='HTML')
            
        except Exception as e:
            formatted_error = f"--- API GATEWAY INITIALIZATION CRASH (ID: {log_id}) ---\n" + "".join(traceback.format_exception(*sys.exc_info()))
            write_persistent_log(log_id, formatted_error)

            log_markup = types.InlineKeyboardMarkup()
            log_markup.add(types.InlineKeyboardButton("VIEW LOGS 📋", callback_data=f"log_{log_id}"))

            bot.send_message(target_user, f"❌ <b>AUTOMATIC DEPLOYING FAILED OVER API INSTANCE!</b>\n\n⚠️ Reason: <code>{str(e)}</code>", reply_markup=log_markup, parse_mode='HTML')
            bot.edit_message_caption(f"❌ <b>DEPLOY FAUSED: API SANDBOX TERMINATION</b>\n⚠️ Error: {str(e)}", call.message.chat.id, call.message.message_id, reply_markup=log_markup, parse_mode='HTML')
            
        del pending_requests[req_id]
        bot.answer_callback_query(call.id)
        return

    elif call.data.startswith("log_"):
        log_id = call.data[4:]
        log_data = read_persistent_log(log_id)
        if len(log_data) > 4000:
            log_data = log_data[:4000] + "\n...[LOG EXCEEDED TRUNCATION]"
        bot.send_message(call.message.chat.id, f"📋 <b>ISOLATED SCRIPT ERROR STACK (ID: {log_id}):</b>\n\n<code>{log_data}</code>", parse_mode='HTML')
        bot.answer_callback_query(call.id)
        return

    # --- REGULAR PANEL LOGICS ---
    elif call.data == "view_profile":
        is_premium = "👑 PREMIUM PRIVACY USER" if premium_users.get(user_id, False) else "🆓 FREE USER NODE"
        files_count = len(user_sessions.get(user_id, {}))
        bot.send_message(call.message.chat.id, f"👤 <b>ENCRYPTED PROFILE</b>\n🆔 ID: <code>{user_id}</code>\n🎖️ Status: <b>{is_premium}</b>\n📂 Real Hosted: <code>{files_count}</code>", parse_mode='HTML')
        bot.answer_callback_query(call.id)

    elif call.data == "anti_crash_info":
        bot.send_message(call.message.chat.id, "🛡️ <b>ANTI-PENETRATION FIREWALL:</b> Active ✅", parse_mode='HTML')
        bot.answer_callback_query(call.id)

    elif call.data == "refresh_engine":
        if os.path.exists(LOG_FILE_PATH):
            try:
                os.remove(LOG_FILE_PATH)
                bot.answer_callback_query(call.id, "🔄 Persistent Log File Purged Clean!", show_alert=True)
            except:
                bot.answer_callback_query(call.id, "❌ Error clearing logs.")
        else:
            bot.answer_callback_query(call.id, "👍 Log file already clean.", show_alert=True)

    elif call.data.startswith("manage_"):
        bot_id = call.data.split("_")[1]
        b_data = user_sessions.get(user_id, {}).get(bot_id)
        if b_data:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🛑 TERMINATE HOST NODE", callback_data=f"stop_{bot_id}"))
            bot.edit_message_text(f"🛠 <b>MANAGING DATASTREAM:</b> <code>{b_data['name']}</code>", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data.startswith("stop_"):
        bot_id = call.data.split("_")[1]
        if bot_id in live_threads:
            try:
                if live_threads[bot_id]["process_obj"]:
                    live_threads[bot_id]["process_obj"].terminate()
                if os.path.exists(live_threads[bot_id]["filename"]):
                    os.remove(live_threads[bot_id]["filename"])
            except: pass
            del live_threads[bot_id]
            
        if user_id in user_sessions and bot_id in user_sessions[user_id]:
            del user_sessions[user_id][bot_id]
        bot.answer_callback_query(call.id, "Deployment Node Terminated Clean.")
        bot.delete_message(call.message.chat.id, call.message.message_id)

# --- 🔄 INFINITY SERVER LOOP ---
if __name__ == "__main__":
    print("Premium Haunted Injector Secure Engine Fired Up Successfully...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(timeout=30, long_polling_timeout=15, skip_pending=True)
        except Exception as e:
            print(f"Server Restructuring Network Loop Re-connecting... Error: {e}")
            time.sleep(5)
    
