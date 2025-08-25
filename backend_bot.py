import telebot
import pymongo
import time
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configuration
TOKEN = "7771736139:AAFhBdAAZF6-rV7YCX08hHK_FAYrHDe8sL0"
MONGO_URI = "mongodb+srv://botuser:Xyz12345@tgbot.wh52pfi.mongodb.net/?retryWrites=true&w=majority&appName=tgbot"
ADSTERRA_API_TOKEN = "0bc23fcccc35acd927d3e508222416b9"
AD_SERVER_URL = "https://pochi-adserver.onrender.com/ad"  # Update after ad server deployment
DASHBOARD_URL = "https://pochi-frontend.onrender.com"     # Update after frontend deployment
ADMIN_ID = 6277866627
USDT_RATE = 0.0005  # 1 point = 0.0005 USDT

# MongoDB setup
client = pymongo.MongoClient(MONGO_URI)
db = client["tgbot"]
users_collection = db["users"]
settings_collection = db["settings"]

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# Helper functions
def get_user(user_id):
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        user = {
            "user_id": user_id,
            "points": 0,
            "referrals": 0,
            "last_ad_time": 0,
            "ad_count": 0,
            "captcha_verified": False,
            "captcha_answer": None,
            "daily_checkin": 0,
            "followed_channel": False
        }
        users_collection.insert_one(user)
    return user

def generate_captcha():
    import random
    num1, num2 = random.randint(1, 10), random.randint(1, 10)
    answer = num1 + num2
    return f"{num1} + {num2} = ?", answer

def get_leaderboard():
    top_users = users_collection.find().sort("points", -1).limit(10)
    leaderboard = "\n".join([f"{i+1}. User {user['user_id']}: {user['points']} points" for i, user in enumerate(top_users)])
    return leaderboard or "No users yet."

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user["captcha_verified"]:
        question, answer = generate_captcha()
        user["captcha_answer"] = answer
        users_collection.update_one({"user_id": user_id}, {"$set": {"captcha_answer": answer}})
        
        markup = InlineKeyboardMarkup()
        for i in range(answer-2, answer+3):
            markup.add(InlineKeyboardButton(str(i), callback_data=f"captcha_{i}"))
        
        bot.send_message(user_id, f"Please solve this CAPTCHA: {question}", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Earn Points", callback_data="earn"))
        markup.add(InlineKeyboardButton("Swap to USDT", callback_data="swap"))
        markup.add(InlineKeyboardButton("Withdraw", callback_data="withdraw"))
        markup.add(InlineKeyboardButton("Leaderboard", callback_data="leaderboard"))
        markup.add(InlineKeyboardButton("Dashboard", url=DASHBOARD_URL))
        if user_id == ADMIN_ID:
            markup.add(InlineKeyboardButton("Admin Panel", callback_data="admin"))
        bot.send_message(user_id, "Welcome to Pochi Pochi Earning Bot!\nChoose an option:", reply_markup=markup)

# CAPTCHA verification
@bot.callback_query_handler(func=lambda call: call.data.startswith("captcha_"))
def verify_captcha(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    answer = int(call.data.split("_")[1])
    
    if answer == user["captcha_answer"]:
        users_collection.update_one({"user_id": user_id}, {"$set": {"captcha_verified": True}})
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "CAPTCHA verified! Use /start to continue.")
    else:
        question, answer = generate_captcha()
        users_collection.update_one({"user_id": user_id}, {"$set": {"captcha_answer": answer}})
        markup = InlineKeyboardMarkup()
        for i in range(answer-2, answer+3):
            markup.add(InlineKeyboardButton(str(i), callback_data=f"captcha_{i}"))
        bot.edit_message_text(f"Wrong answer. Try again: {question}", user_id, call.message.message_id, reply_markup=markup)

# Earn points menu
@bot.callback_query_handler(func=lambda call: call.data == "earn")
def earn_menu(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    if not user["captcha_verified"]:
        bot.send_message(user_id, "Please verify CAPTCHA with /start first.")
        return
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Watch Ads", callback_data="watch_ads"))
    markup.add(InlineKeyboardButton("Daily Check-in", callback_data="daily_checkin"))
    markup.add(InlineKeyboardButton("Follow Channel", callback_data="follow_channel"))
    markup.add(InlineKeyboardButton("Refer Friends", callback_data="refer"))
    bot.edit_message_text("How would you like to earn points?", user_id, call.message.message_id, reply_markup=markup)

# Watch ads
@bot.callback_query_handler(func=lambda call: call.data == "watch_ads")
def watch_ads(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    current_time = time.time()
    if current_time - user["last_ad_time"] < 3600:  # 1 hour cooldown
        bot.send_message(user_id, f"Please wait {int(3600 - (current_time - user['last_ad_time']))} seconds before watching more ads.")
        return
    if user["ad_count"] >= 90:  # Daily limit
        bot.send_message(user_id, "You've reached the daily ad limit (90). Try again tomorrow.")
        return
    
    # Simulate ad view via Adsterra
    try:
        response = requests.get(f"{AD_SERVER_URL}?token={ADSTERRA_API_TOKEN}&user_id={user_id}")
        if response.status_code == 200:
            points = 30  # Points per ad session
            users_collection.update_one(
                {"user_id": user_id},
                {"$inc": {"points": points, "ad_count": 30}, "$set": {"last_ad_time": current_time}}
            )
            bot.send_message(user_id, f"You earned {points} points by watching ads!")
        else:
            bot.send_message(user_id, "Error fetching ad. Try again later.")
    except:
        bot.send_message(user_id, "Ad server unavailable. Try again later.")

# Daily check-in
@bot.callback_query_handler(func=lambda call: call.data == "daily_checkin")
def daily_checkin(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    current_time = time.time()
    if current_time - user["daily_checkin"] < 24 * 3600:
        bot.send_message(user_id, "You've already checked in today. Try again tomorrow.")
        return
    
    points = 10
    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"points": points}, "$set": {"daily_checkin": current_time}}
    )
    bot.send_message(user_id, f"You earned {points} points for daily check-in!")

# Follow channel
@bot.callback_query_handler(func=lambda call: call.data == "follow_channel")
def follow_channel(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    if user["followed_channel"]:
        bot.send_message(user_id, "You've already followed the channel.")
        return
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Join @PochiPochiNews", url="https://t.me/PochiPochiNews"))
    markup.add(InlineKeyboardButton("I Joined", callback_data="confirm_follow"))
    bot.send_message(user_id, "Join our channel to earn 50 points!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_follow")
def confirm_follow(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    points = 50
    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"points": points}, "$set": {"followed_channel": True}}
    )
    bot.send_message(user_id, f"You earned {points} points for joining @PochiPochiNews!")

# Refer friends
@bot.callback_query_handler(func=lambda call: call.data == "refer")
def refer(call):
    user_id = call.from_user.id
    referral_link = f"https://t.me/PochiPochiBot?start={user_id}"
    bot.send_message(user_id, f"Invite friends with this link to earn 100 points per referral:\n{referral_link}")

@bot.message_handler(commands=['start'])
def handle_referral(message):
    args = message.text.split()
    if len(args) > 1:
        referrer_id = int(args[1])
        user_id = message.from_user.id
        if referrer_id != user_id:
            user = get_user(user_id)
            if not user["captcha_verified"]:
                return
            referrer = get_user(referrer_id)
            users_collection.update_one(
                {"user_id": referrer_id},
                {"$inc": {"points": 100, "referrals": 1}}
            )
            bot.send_message(referrer_id, f"Someone joined using your referral link! You earned 100 points.")

# Swap points to USDT
@bot.callback_query_handler(func=lambda call: call.data == "swap")
def swap_points(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    points = user["points"]
    usdt = points * USDT_RATE
    bot.send_message(user_id, f"You have {points} points, which can be swapped for {usdt:.4f} USDT.\nReply with /swap {amount} to proceed.")

@bot.message_handler(commands=['swap'])
def process_swap(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    try:
        amount = float(message.text.split()[1])
        if amount <= 0 or amount * USDT_RATE > user["points"] * USDT_RATE:
            bot.send_message(user_id, "Invalid amount or insufficient points.")
            return
        points_needed = amount / USDT_RATE
        users_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"points": -points_needed}}
        )
        bot.send_message(ADMIN_ID, f"User {user_id} requested to swap {points_needed} points for {amount:.4f} USDT.")
        bot.send_message(user_id, f"Swap request for {amount:.4f} USDT sent to admin for approval.")
    except:
        bot.send_message(user_id, "Use /swap {amount} (e.g., /swap 0.5)")

# Withdraw USDT
@bot.callback_query_handler(func=lambda call: call.data == "withdraw")
def withdraw(call):
    user_id = call.from_user.id
    bot.send_message(user_id, "Please provide your USDT wallet address (Binance, OKX, or Trust Wallet) using /withdraw {address}")

@bot.message_handler(commands=['withdraw'])
def process_withdraw(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    try:
        address = message.text.split()[1]
        points = user["points"]
        usdt = points * USDT_RATE
        bot.send_message(ADMIN_ID, f"User {user_id} requested withdrawal of {usdt:.4f} USDT to {address}")
        bot.send_message(user_id, f"Your withdrawal request for {usdt:.4f} USDT to {address} has been sent to admin.")
    except:
        bot.send_message(user_id, "Use /withdraw {address} (e.g., /withdraw 0x123...)")

# Leaderboard
@bot.callback_query_handler(func=lambda call: call.data == "leaderboard")
def show_leaderboard(call):
    user_id = call.from_user.id
    bot.send_message(user_id, f"🏆 Top 10 Users:\n{get_leaderboard()}")

# Admin panel
@bot.callback_query_handler(func=lambda call: call.data == "admin")
def admin_panel(call):
    user_id = call.from_user.id
    if user_id != ADMIN_ID:
        bot.send_message(user_id, "Access denied.")
        return
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("View Settings", callback_data="view_settings"))
    markup.add(InlineKeyboardButton("Update USDT Rate", callback_data="update_rate"))
    bot.send_message(user_id, "Admin Panel:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "view_settings")
def view_settings(call):
    user_id = call.from_user.id
    if user_id != ADMIN_ID:
        return
    settings = settings_collection.find_one() or {"usdt_rate": USDT_RATE}
    bot.send_message(user_id, f"Current USDT Rate: {settings['usdt_rate']} USDT/point")

@bot.callback_query_handler(func=lambda call: call.data == "update_rate")
def update_rate(call):
    user_id = call.from_user.id
    if user_id != ADMIN_ID:
        return
    bot.send_message(user_id, "Enter new USDT rate with /set rate {value} (e.g., /set rate 0.0005)")

@bot.message_handler(commands=['set'])
def set_settings(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.send_message(user_id, "Access denied.")
        return
    
    try:
        args = message.text.split()
        if args[1] == "rate":
            new_rate = float(args[2])
            settings_collection.update_one({}, {"$set": {"usdt_rate": new_rate}}, upsert=True)
            bot.send_message(user_id, f"USDT rate updated to {new_rate} USDT/point.")
    except:
        bot.send_message(user_id, "Use /set rate {value} (e.g., /set rate 0.0005)")

# Start polling
bot.infinity_polling()