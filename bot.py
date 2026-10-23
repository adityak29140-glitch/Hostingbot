import json
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Bot Configuration
BOT_TOKEN = "8963703963:AAF-2e5poOVF7oqNPhg70oF7NL7Cv0BGdfE"
API_URL = "https://api.telegram.org/bot" + BOT_TOKEN + "/"
OWNER_ID = 8235337601
ADMIN_IDS = [8235337601]
CHANNEL_LINK = "https://t.me/All_channel_links_please_join"
CHANNEL_USERNAME = "All_channel_links_please_join"

# Database configuration
DB_FILE = "bot_database.json"

# Initialize database
def init_db():
    if not os.path.exists(DB_FILE):
        default_data = {
            "users": [],
            "admins": [8235337601],
            "banned": [],
            "settings": {
                "require_join": True
            }
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Function to check if user is admin
def is_admin(user_id):
    if user_id == OWNER_ID or user_id in ADMIN_IDS:
        return True
    db = init_db()
    return user_id in db.get("admins", [])

# Function to check if user is banned
def is_banned(user_id):
    db = init_db()
    return user_id in db.get("banned", [])

# Function to check channel membership
def check_channel_membership(chat_id, user_id):
    url = f"{API_URL}getChatMember?chat_id=@{CHANNEL_USERNAME}&user_id={user_id}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("ok") and "result" in data:
            status = data["result"].get("status")
            return status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking membership: {e}")
    return False

# Function to send message
def send_message(chat_id, text, keyboard=None):
    url = f"{API_URL}sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if keyboard:
        payload["reply_markup"] = json.dumps(keyboard)
    
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

# Function to edit message
def edit_message(chat_id, message_id, text, keyboard=None):
    url = f"{API_URL}editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if keyboard:
        payload["reply_markup"] = json.dumps(keyboard)
    
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        print(f"Error editing message: {e}")
        return None

# Function to get main keyboard
def get_main_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "📱 Phone Number", "callback_data": "lookup_phone"},
                {"text": "🚗 Vehicle Number", "callback_data": "lookup_vehicle"}
            ],
            [
                {"text": "🆔 Aadhaar Card", "callback_data": "lookup_aadhaar"},
                {"text": "📮 Pincode", "callback_data": "lookup_pincode"}
            ],
            [
                {"text": "🏢 GST Number", "callback_data": "lookup_gst"},
                {"text": "💸 UPI ID", "callback_data": "lookup_upi"}
            ],
            [
                {"text": "🏦 IFSC Code", "callback_data": "lookup_ifsc"},
                {"text": "🪪 Pan Card", "callback_data": "lookup_pan"}
            ],
            [
                {"text": "🌐 IP Lookup", "callback_data": "lookup_ip"},
                {"text": "🌤️ Weather Lookup", "callback_data": "lookup_weather"}
            ],
            [
                {"text": "👨‍👩‍👧‍👦 Family", "callback_data": "lookup_family"},
                {"text": "📷 Instagram", "callback_data": "lookup_instagram"}
            ],
            [
                {"text": "📡 TG Lookup", "callback_data": "lookup_tg"},
                {"text": "📧 Email", "callback_data": "lookup_email"}
            ],
            [
                {"text": "🔢 IMEI", "callback_data": "lookup_imei"},
                {"text": "🍛 RASHAN", "callback_data": "lookup_rashan"}
            ],
            [
                {"text": "❓ Help", "callback_data": "help"},
                {"text": "📊 Statistics", "callback_data": "stats"}
            ]
        ]
    }

# Function to get admin panel keyboard
def get_admin_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "➕ Add Inline Button", "callback_data": "admin_add_button"},
                {"text": "🔗 Add Button API", "callback_data": "admin_add_api"}
            ],
            [
                {"text": "📢 Add Channel", "callback_data": "admin_add_channel"},
                {"text": "👥 Add Admin", "callback_data": "admin_add_admin"}
            ],
            [
                {"text": "📣 Broadcast", "callback_data": "admin_broadcast"},
                {"text": "🚫 Ban User", "callback_data": "admin_ban"}
            ],
            [
                {"text": "✅ Unban User", "callback_data": "admin_unban"},
                {"text": "👥 All Users", "callback_data": "admin_users"}
            ],
            [
                {"text": "◀️ Back to Main", "callback_data": "back_to_main"}
            ]
        ]
    }

# Function to get example message
def get_example_message(type_key):
    examples = {
        'phone': "• 📱 Phone: `9876543210`\n• 🏢 GST: `27ABCDE1234F1Z5`\n• 💸 UPI: `username@bank`\n• 🏦 IFSC: `SBIN0001234`\n• 📮 Pincode: `110001`\n• 🚗 Vehicle: `UP32QP0001`\n• 🪪 Pan Card: `ABCDE1234F`\n• 🌐 IP: `8.8.8.8`\n• 📧 Email: `user@example.com`\n• 🔢 IMEI: `123456789012345`",
        'weather': "• 🌤️ Weather: `Mumbai` or `Mumbai,IN`\n• Example: `London` or `New York,US`",
        'instagram': "• 📷 Instagram: `username`\n• Example: `instagram` or `cristiano`",
        'tg': "• 📡 TG Lookup: `username`\n• Example: `@username` or `username`",
        'family': "• 👨‍👩‍👧‍👦 Family: `Family Name`\n• Example: `Singh` or `Sharma`",
        'rashan': "• 🍛 RASHAN: `Ration Card Number`\n• Example: `123456789012`"
    }
    
    base_text = "🔍 *Send Input*\n━━━━━━━━━━━━━━━━━━━━\n\n"
    base_text += "Please send the required information:\n\n"
    base_text += "📋 *Examples:*\n"
    base_text += examples.get(type_key, examples['phone'])
    base_text += "\n━━━━━━━━━━━━━━━━━━━━\n"
    base_text += "Made by @REDX64\n"
    base_text += "Powered By ROH-X"
    
    return base_text

# Function to perform lookup
def perform_lookup(lookup_type, input_text):
    apis = {
        'phone': f'https://api.example.com/phone/{input_text}',
        'aadhaar': f'https://api.example.com/aadhaar/{input_text}',
        'gst': f'https://api.example.com/gst/{input_text}',
        'upi': f'https://api.example.com/upi/{input_text}',
        'ifsc': f'https://api.example.com/ifsc/{input_text}',
        'pincode': f'https://api.example.com/pincode/{input_text}',
        'vehicle': f'https://api.example.com/vehicle/{input_text}',
        'pan': f'https://api.example.com/pan/{input_text}',
        'ip': f'https://api.example.com/ip/{input_text}',
        'weather': f'https://api.example.com/weather/{input_text}',
        'instagram': f'https://api.example.com/instagram/{input_text}',
        'tg': f'https://tg-2-num-api-org.vercel.app/api/search?userid={input_text}',
        'email': f'https://api.example.com/email/{input_text}',
        'imei': f'https://api.example.com/imei/{input_text}',
        'rashan': f'https://api.example.com/rashan/{input_text}',
        'family': f'https://api.example.com/family/{input_text}'
    }
    
    response = f"🔍 *{lookup_type.capitalize()} Lookup Result*\n━━━━━━━━━━━━━━━━━━━━\n\n"
    response += f"📝 *Input:* `{input_text}`\n\n"
    response += "⚠️ *Note:* API integration is pending.\n"
    response += f"API Endpoint: {apis.get(lookup_type, 'N/A')}\n\n"
    response += "━━━━━━━━━━━━━━━━━━━━\n"
    response += "Made by @Xyz_Zico\n"
    response += "Powered By ROH-X"
    
    return response

# Function to get welcome message
def get_welcome_message():
    text = "🤖 *Welcome To Multi Lookup Bot*\n━━━━━━━━━━━━━━━━━━━━\n\n"
    text += "🔍 *Features:*\n"
    text += "• 📱 Phone Number Lookup\n"
    text += "• 🆔 Aadhaar Card Lookup\n"
    text += "• 🏢 GST Number Lookup\n"
    text += "• 💸 UPI ID Lookup\n"
    text += "• 🏦 IFSC Code Lookup\n"
    text += "• 📮 Pincode Lookup\n"
    text += "• 🚗 Vehicle RC Lookup\n"
    text += "• 🪪 Pan Card Lookup\n"
    text += "• 🌐 IP Address Lookup\n"
    text += "• 🌤️ Weather Lookup\n"
    text += "• 👨‍👩‍👧‍👦 Family Details Lookup\n"
    text += "• 📷 Instagram Profile Lookup\n"
    text += "• 📡 Telegram Profile Lookup\n"
    text += "• 📧 Email Address Lookup\n"
    text += "• 🔢 IMEI Number Lookup\n"
    text += "• 🍛 RASHAN Card Lookup\n"
    text += "\n━━━━━━━━━━━━━━━━━━━━\n"
    text += "Made by @Xyz_Zico\n"
    text += "Powered By ROH-X."
    return text

# Main webhook endpoint
@app.route("/", methods=["POST"])
def webhook():
    init_db()
    update = request.get_json()
    
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]
        text = message.get("text", "")
        
        # Register user
        db = init_db()
        if user_id not in db["users"]:
            db["users"].append(user_id)
            save_db(db)
            
        # Check if user is banned
        if is_banned(user_id):
            send_message(chat_id, "🚫 You are banned from using this bot.\nContact: @Xyz_Zico")
            return jsonify({"status": "ok"})
            
        # Check channel membership
        if db["settings"]["require_join"] and not check_channel_membership(chat_id, user_id):
            keyboard = {
                "inline_keyboard": [
                    [{"text": "📢 Join Channel", "url": CHANNEL_LINK}],
                    [{"text": "✅ Joined", "callback_data": "check_join"}]
                ]
            }
            send_message(chat_id, f"🔒 *Please join our channel to use this bot!*\n\nChannel: {CHANNEL_LINK}", keyboard)
            return jsonify({"status": "ok"})
            
        # Handle commands
        if text == "/start":
            send_message(chat_id, get_welcome_message(), get_main_keyboard())
        elif text == "/admin" and is_admin(user_id):
            send_message(chat_id, "🔐 *Admin Panel*\n━━━━━━━━━━━━━━━━━━━━\n\nWelcome Admin! Use the buttons below to manage the bot.", get_admin_keyboard())
        elif "reply_to_message" in message:
            reply_text = message["reply_to_message"].get("text", "")
            if is_admin(user_id) and "Broadcast Mode" in reply_text:
                success, failed = 0, 0
                for user in db["users"]:
                    if send_message(user, text):
                        success += 1
                    else:
                        failed += 1
                send_message(chat_id, f"📢 *Broadcast Complete*\n✅ Success: {success}\n❌ Failed: {failed}")
            elif "Send Input" in reply_text:
                lookup_type = "phone"
                if "Vehicle" in reply_text: lookup_type = "vehicle"
                elif "Aadhaar" in reply_text: lookup_type = "aadhaar"
                elif "Pincode" in reply_text: lookup_type = "pincode"
                elif "GST" in reply_text: lookup_type = "gst"
                elif "UPI" in reply_text: lookup_type = "upi"
                elif "IFSC" in reply_text: lookup_type = "ifsc"
                elif "Pan" in reply_text: lookup_type = "pan"
                elif "IP" in reply_text: lookup_type = "ip"
                elif "Weather" in reply_text: lookup_type = "weather"
                elif "Instagram" in reply_text: lookup_type = "instagram"
                elif "TG" in reply_text: lookup_type = "tg"
                elif "Email" in reply_text: lookup_type = "email"
                elif "IMEI" in reply_text: lookup_type = "imei"
                elif "RASHAN" in reply_text: lookup_type = "rashan"
                elif "Family" in reply_text: lookup_type = "family"
                
                result = perform_lookup(lookup_type, text)
                send_message(chat_id, result)
                
    elif "callback_query" in update:
        callback = update["callback_query"]
        chat_id = callback["message"]["chat"]["id"]
        user_id = callback["from"]["id"]
        message_id = callback["message"]["message_id"]
        data = callback["data"]
        
        if is_banned(user_id):
            send_message(chat_id, "🚫 You are banned from using this bot.\nContact: @Xyz_Zico")
            return jsonify({"status": "ok"})
            
        db = init_db()
        if db["settings"]["require_join"] and not check_channel_membership(chat_id, user_id) and data != "check_join":
            keyboard = {
                "inline_keyboard": [
                    [{"text": "📢 Join Channel", "url": CHANNEL_LINK}],
                    [{"text": "✅ Joined", "callback_data": "check_join"}]
                ]
            }
            edit_message(chat_id, message_id, f"🔒 *Please join our channel to use this bot!*\n\nChannel: {CHANNEL_LINK}", keyboard)
            return jsonify({"status": "ok"})
            
        if data.startswith("lookup_"):
            lookup_type = data.replace("lookup_", "")
            example_msg = get_example_message(lookup_type)
            keyboard = {"inline_keyboard": [[{"text": "◀️ Back", "callback_data": "back_to_main"}]]}
            edit_message(chat_id, message_id, example_msg, keyboard)
            
        elif data == "help":
            help_text = "❓ *Help & Support*\n━━━━━━━━━━━━━━━━━━━━\n\n"
            help_text += "📌 *How to Use:*\n1️⃣ Select any lookup option from the menu\n2️⃣ Send the required information\n3️⃣ Get instant results!\n\n"
            help_text += f"📞 *Support:* @Xyz_Zico\n📢 *Channel:* {CHANNEL_LINK}\n\n━━━━━━━━━━━━━━━━━━━━\nMade by @Xyz_Zico\nPowered By ROH-X"
            edit_message(chat_id, message_id, help_text, get_main_keyboard())
            
        elif data == "stats":
            total_users = len(db["users"])
            banned_users = len(db["banned"])
            active_users = total_users - banned_users
            stats_text = f"📊 *Bot Statistics*\n━━━━━━━━━━━━━━━━━━━━\n\n👥 Total Users: `{total_users}`\n✅ Active Users: `{active_users}`\n🚫 Banned Users: `{banned_users}`\n👑 Owner: @Xyz_Zico\n\n━━━━━━━━━━━━━━━━━━━━\nMade by @REDX64\nPowered By ROH-X"
            edit_message(chat_id, message_id, stats_text, get_main_keyboard())
            
        elif data == "back_to_main":
            edit_message(chat_id, message_id, get_welcome_message(), get_main_keyboard())
            
        elif data == "check_join":
            if check_channel_membership(chat_id, user_id):
                edit_message(chat_id, message_id, get_welcome_message(), get_main_keyboard())
            else:
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "📢 Join Channel", "url": CHANNEL_LINK}],
                        [{"text": "✅ Joined", "callback_data": "check_join"}]
                    ]
                }
                edit_message(chat_id, message_id, "❌ *You haven't joined the channel yet!*\n\nPlease join and click 'Joined' button.", keyboard)
                
        elif data.startswith("admin_") and is_admin(user_id):
            action = data.replace("admin_", "")
            if action == "users":
                users_list = "👥 *All Users*\n━━━━━━━━━━━━━━━━━━━━\n\n"
                for index, user in enumerate(db["users"][:50]):
                    status = "🚫 Banned" if user in db["banned"] else "✅ Active"
                    users_list += f"`{index + 1}.` User ID: `{user}` - {status}\n"
                users_list += f"\n━━━━━━━━━━━━━━━━━━━━\nTotal: {len(db['users'])} users"
                send_message(chat_id, users_list)
                
        # Answer callback query
        try:
            requests.get(f"{API_URL}answerCallbackQuery?callback_query_id={callback['id']}")
        except Exception:
            pass
        
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
