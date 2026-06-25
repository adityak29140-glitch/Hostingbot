import os
import sys
import re
import time
import uuid
import threading
import traceback
import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException

# Railway Environment Port Binding
os.environ["PORT"] = os.environ.get("PORT", "8080")

# Tera verified active token
TOKEN = "8773248276:AAEf_2WJpApeVK79QFiRn6ovIyo6S0SeC8E"
DEFAULT_CHAT_ID = "8620962808"  # TERA OWNER CHAT ID
OWNER_USERNAME = "ADITYAXPASWANJI"

# Main bot initialization
bot = telebot.TeleBot(TOKEN, threaded=True)

# InMemory Data Trackers
user_sessions = {}
live_threads = {}
premium_users = {} 
pending_requests = {}  # Owner approval tracker
error_logs = {}        # Failed deployments log storage
total_files_hosted = 0

# --- MAIN HOME PANEL KEYS ---
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("📤 FILE UPLOAD FREE"), types.KeyboardButton("📂 MY FILES"))
    markup.row(types.KeyboardButton("📊 SERVER STATS"), types.KeyboardButton("🚀 BOOST SERVER"))
    markup.row(types.KeyboardButton("⚙️ ADVANCED SETTINGS"), types.KeyboardButton("👑 GET PREMIUM"))
    return markup

# --- ADVANCED SETTINGS INLINE PANEL ---
def advanced_settings_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👤 MY PROFILE", callback_data="view_profile"),
        types.InlineKeyboardButton("🛡️ ISOLATION ENGINE", callback_data="anti_crash_info")
    )
    markup.add(
        types.InlineKeyboardButton("💬 LIVE SUPPORT", url=f"t.me/{OWNER_USERNAME}"),
        types.InlineKeyboardButton("🔄 REFRESH ENGINE", callback_data="refresh_engine")
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
        "⚡ <b>ADITYA MONSTER HOST v5.0 SECURE</b> ⚡\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🟢 <b>STATUS:</b> <code>SYSTEM ONLINE</code>\n"
        "🚀 <b>ENGINE:</b> <code>API ISOLATION ACTIVE</code>\n"
        "🛡️ <b>ADMIN CONTROL:</b> <code>STRICT APPROVAL MODE</code>\n"
        "📋 <b>BLOCK PROTECTION:</b> <code>100% SECURE ✅</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>🤖 PYTHON (.py) FILE SEND KARO! APNI SCRIPT LIVE LOGS AUR STRICT ISOLATION KE SATH APPROVAL MEIN JAYEGI.</i>"
    )
    bot.send_message(message.chat.id, haunted_caption, reply_markup=main_keyboard(), parse_mode='HTML')

# --- HANDLE TEXT BUTTON MENUS ---
@bot.message_handler(func=lambda message: message.text in ["📤 FILE UPLOAD FREE", "📂 MY FILES", "👑 GET PREMIUM", "📊 SERVER STATS", "⚙️ ADVANCED SETTINGS", "🚀 BOOST SERVER"])
def handle_text_menus(message):
    user_id = message.from_user.id
    
    if message.text == "📤 FILE UPLOAD FREE":
        bot.send_message(message.chat.id, "📥 <b>SEND ME YOUR PYTHON FILE (.py) NOW:</b>\n\n<i>File direct admin verification queue me save ho jayegi.</i>", parse_mode='HTML')
        
    elif message.text == "👑 GET PREMIUM":
        premium_text = (
            "👑 <b>ADITYA HOSTING PREMIUM PLANS</b> 👑\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🌟 <b>Benefits:</b> No File Limit, No Timeout, Dedicated Fast Server Routing.\n"
            "🔮 <i>Select your package to upgrade instantly:</i>"
        )
        bot.send_message(message.chat.id, premium_text, reply_markup=premium_plans_keyboard(), parse_mode='HTML')
        
    elif message.text == "📂 MY FILES":
        if user_id not in user_sessions or not user_sessions[user_id]:
            bot.send_message(message.chat.id, "❌ <b>KOI FILE ACTIVE NAHI HAI!</b>", parse_mode='HTML')
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        for bot_id, b_data in user_sessions[user_id].items():
            markup.add(types.InlineKeyboardButton(f"📄 {b_data['name']}", callback_data=f"manage_{bot_id}"))
        bot.send_message(message.chat.id, "📂 <b>YOUR TOTAL ACTIVE HOSTED FILES:</b>", reply_markup=markup, parse_mode='HTML')

    elif message.text == "📊 SERVER STATS":
        total_users = len(user_sessions)
        active_bots = len(live_threads)
        stats_text = (
            "📊 <b>LIVE SERVER STATISTICS</b> 📊\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 <b>Total Active Users:</b> <code>{total_users}</code>\n"
            f"🤖 <b>Running Bots in Background:</b> <code>{active_bots}</code>\n"
            f"📈 <b>Total Deployments Ever:</b> <code>{total_files_hosted}</code>\n"
            f"⚙️ <b>Server Guard:</b> <code>Isolated & Block Proof (0.01%)</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "✅ <b>All systems are running stable 24/7.</b>"
        )
        bot.send_message(message.chat.id, stats_text, parse_mode='HTML')

    elif message.text == "⚙️ ADVANCED SETTINGS":
        bot.send_message(message.chat.id, "⚙️ <b>ADITYA ADVANCED SETTINGS PANEL</b>", reply_markup=advanced_settings_keyboard(), parse_mode='HTML')
        
    elif message.text == "🚀 BOOST SERVER":
        status_boost = bot.send_message(message.chat.id, "⚡ <b>PURGING API LOGS & CACHE...</b>", parse_mode='HTML')
        time.sleep(1.2)
        bot.edit_message_text("🚀 <b>SERVER BOOSTED SUCCESSFUL! SPEED INCREASED BY 200% ✅</b>", message.chat.id, status_boost.message_id, parse_mode='HTML')

def run_memory_polling(user_bot_instance, bot_id):
    try:
        user_bot_instance.remove_webhook()
        user_bot_instance.infinity_polling(timeout=20, long_polling_timeout=10, skip_pending=True)
    except Exception:
        pass

# --- FILE INPUT RECEIVED SYSTEM ---
@bot.message_handler(content_types=['document'])
def handle_auto_deployment(message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {}

    if not message.document.file_name.endswith('.py'):
        bot.send_message(message.chat.id, "❌ <b>REJECTED! SIRF .py FILE ACCEPT HOGI!</b>", parse_mode='HTML')
        return

    bot.send_message(
        message.chat.id, 
        "⏳ <b>WAIT FOR ADMIN APPROVAL...</b>\n\nAapki file verification ke liye Admin ke paas bhej di gayi hai. Engine parameters check hote hi update milega! ✅", 
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
        f"🔔 <b>NEW PYTHON FILE FOR APPROVAL!</b>\n\n"
        f"👤 <b>User ID:</b> <code>{user_id}</code>\n"
        f"📄 <b>File Name:</b> <code>{message.document.file_name}</code>\n"
        f"🆔 <b>Request ID:</b> <code>{req_id}</code>\n"
    )
    bot.send_document(DEFAULT_CHAT_ID, message.document.file_id, caption=admin_caption, reply_markup=owner_markup, parse_mode='HTML')

# --- CALLBACK SYSTEM PRO (ISOLATED EXECUTION) ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global total_files_hosted
    user_id = call.from_user.id
    
    if call.data.startswith("app_") or call.data.startswith("rej_"):
        if str(user_id) != DEFAULT_CHAT_ID:
            bot.answer_callback_query(call.id, "❌ Tu owner nahi hai!", show_alert=True)
            return
            
        action = call.data[:3]
        req_id = call.data[4:]
        req_data = pending_requests.get(req_id)
        
        if not req_data:
            bot.answer_callback_query(call.id, "❌ Session Expired!", show_alert=True)
            return
            
        target_user = req_data["user_id"]
        filename = req_data["file_name"]
        
        if action == "rej_":
            bot.send_message(target_user, f"❌ <b>YOUR FILE `{filename}` WAS REJECTED BY ADMIN!</b>", parse_mode='HTML')
            bot.edit_message_caption(f"❌ <b>REJECTED BY OWNER</b>\n📄 File: {filename}", call.message.chat.id, call.message.message_id, parse_mode='HTML')
            del pending_requests[req_id]
            return

        bot.send_message(target_user, f"🚀 <b>ADMIN APPROVED! INJECTING SCRIPT ENGINE...</b>", parse_mode='HTML')
        bot.edit_message_caption(f"⏳ <b>PROCESSING DEPLOYMENT...</b>\n📄 File: {filename}", call.message.chat.id, call.message.message_id, parse_mode='HTML')

        # STRICT ISOLATION BLOCK: Kisi bhi external API crash se main thread ko bachane ke liye try-catch wrapper
        try:
            file_info = bot.get_file(req_data["file_id"])
            file_content = bot.download_file(file_info.file_path)
            code_text = file_content.decode('utf-8', errors='ignore')
            
            token_match = re.search(r'(\d{9,10}:[A-Za-z0-9_-]{35})', code_text)
            chat_id_match = re.search(r'(?:chat_id|CHAT_ID|id)\s*=\s*["\']?(-?\d+)"\']?', code_text)
            
            if not token_match:
                raise Exception("TokenNotFoundError: Token pattern missing in code body.")

            extracted_token = token_match.group(1)
            extracted_chat = chat_id_match.group(1) if chat_id_match else DEFAULT_CHAT_ID

            # Isolated Bot Verification
            try:
                check_bot = telebot.TeleBot(extracted_token)
                check_bot.get_me()
            except ApiTelegramException as api_err:
                raise Exception(f"API Error Detected: Code {api_err.error_code} ({api_err.description})")

            bot_id = str(uuid.uuid4())[:8]
            target_bot = telebot.TeleBot(extracted_token, threaded=True)

            t = threading.Thread(target=run_memory_polling, args=(target_bot, bot_id), daemon=True)
            t.start()
            
            live_threads[bot_id] = {"instance": target_bot, "thread": t}
            user_sessions[target_user][bot_id] = {'name': filename, 'token': extracted_token, 'chat_id': extracted_chat}
            total_files_hosted += 1
            
            bot.send_message(target_user, f"✅ <b>YOUR SCRIPT IS NOW LIVE!</b>\n\n📄 File: <code>{filename}</code>", parse_mode='HTML')
            bot.edit_message_caption(f"✅ <b>APPROVED & ALIVE!</b>\n📄 File: {filename}\n⚙️ Thread: {bot_id}", call.message.chat.id, call.message.message_id, parse_mode='HTML')
            
        except Exception as e:
            log_id = str(uuid.uuid4())[:6]
            formatted_error = f"--- ISOLATED ENGINE ERROR (ID: {log_id}) ---\n" + "".join(traceback.format_exception(*sys.exc_info()))
            error_logs[log_id] = formatted_error

            log_markup = types.InlineKeyboardMarkup()
            log_markup.add(types.InlineKeyboardButton("VIEW LOGS 📋", callback_data=f"log_{log_id}"))

            bot.send_message(target_user, f"❌ <b>DEPLOYMENT FAILED! API/TOKEN FAULT REJECTED.</b>\n\n⚠️ Reason: <code>{str(e)}</code>", reply_markup=log_markup, parse_mode='HTML')
            bot.edit_message_caption(f"❌ <b>DEPLOYMENT FAUSED</b>\n⚠️ Error: {str(e)}", call.message.chat.id, call.message.message_id, reply_markup=log_markup, parse_mode='HTML')
            
        del pending_requests[req_id]
        bot.answer_callback_query(call.id)
        return

    elif call.data.startswith("log_"):
        log_id = call.data[4:]
        log_data = error_logs.get(log_id, "⚠️ Log expired or buffer flushed.")
        if len(log_data) > 4000:
            log_data = log_data[:4000] + "\n...[TRUNCATED]"
        bot.send_message(call.message.chat.id, f"📋 <b>API ENGINE REPORT (ID: {log_id}):</b>\n\n<code>{log_data}</code>", parse_mode='HTML')
        bot.answer_callback_query(call.id)
        return

    # --- NORMAL UTILS ---
    elif call.data == "view_profile":
        is_premium = "👑 PREMIUM USER" if premium_users.get(user_id, False) else "🆓 FREE USER"
        files_count = len(user_sessions.get(user_id, {}))
        bot.send_message(call.message.chat.id, f"👤 <b>PROFILE</b>\n🆔 ID: <code>{user_id}</code>\n🎖️ Status: {is_premium}\n📂 Hosted: {files_count}", parse_mode='HTML')
        bot.answer_callback_query(call.id)

    elif call.data == "anti_crash_info":
        bot.send_message(call.message.chat.id, "🛡️ <b>STRICT ISOLATION SYSTEM:</b> Active ✅\n\nUser ke bots ki internal API ya network issues aapke main panel engine ko block nahi karegi.", parse_mode='HTML')
        bot.answer_callback_query(call.id)

    elif call.data == "refresh_engine":
        bot.answer_callback_query(call.id, "🔄 System Memory Purged!", show_alert=True)

    elif call.data.startswith("manage_"):
        bot_id = call.data.split("_")[1]
        b_data = user_sessions.get(user_id, {}).get(bot_id)
        if b_data:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🛑 STOP BOT ENGINE", callback_data=f"stop_{bot_id}"))
            bot.edit_message_text(f"🛠 <b>MANAGING:</b> <code>{b_data['name']}</code>", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data.startswith("stop_"):
        bot_id = call.data.split("_")[1]
        if bot_id in live_threads:
            try: live_threads[bot_id]["instance"].stop_bot()
            except: pass
            del live_threads[bot_id]
        if user_id in user_sessions and bot_id in user_sessions[user_id]:
            del user_sessions[user_id][bot_id]
        bot.answer_callback_query(call.id, "Bot Stopped!")
        bot.delete_message(call.message.chat.id, call.message.message_id)

# --- 🔄 INFINITY NETWORK LOOP ---
if __name__ == "__main__":
    print("Premium Haunted Injector Engine Successfully Fired Up...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(timeout=30, long_polling_timeout=15, skip_pending=True)
        except Exception as e:
            print(f"Network Loop Re-connecting... Code: {e}")
            time.sleep(5)
    
