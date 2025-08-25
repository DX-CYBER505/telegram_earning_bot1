import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import datetime
import random
import time
import requests

# Bot Token
TOKEN = '7771736139:AAFhBdAAZF6-rV7YCX08hHK_FAYrHDe8sL0'
bot = telebot.TeleBot(TOKEN)

# Admin user ID
ADMIN_ID = 6277866627

# MongoDB setup
MONGO_URI = 'mongodb+srv://botuser:Xyz12345@tgbot.wh52pfi.mongodb.net/?retryWrites=true&w=majority&appName=tgbot'
client = MongoClient(MONGO_URI)
db = client['earning_bot']
users_collection = db['users']
settings_collection = db['settings']
withdraw_requests_collection = db['withdraw_requests']

# Adsterra API Token and Popunder URL
ADSTERRA_API_TOKEN = '0bc23fcccc35acd927d3e508222416b9'
ADSTERRA_POPUNDER_URL = 'http://pl26780328.profitableratecpm.com/2e/7b/58/2e7b58d34093cfaae6a3392a1b1d6043.js'

# Language dictionaries
languages = {
    'en': {
        'choose_language': 'Welcome to the Earning Bot! Choose your language:',
        'menu': '🏠 Main Menu',
        'balance': '💰 Balance',
        'earn_ads': '📺 Earn from Ads',
        'tasks': '📋 Tasks',
        'referral': '🤝 Referral',
        'leaderboard': '🏆 Leaderboard',
        'swap': '🔄 Swap Points to USDT',
        'withdraw': '💸 Withdraw USDT',
        'admin': '🔧 Admin Panel',
        'back': '⬅ Back to Menu',
        'stats': '📊 Your Stats',
        'captcha_prompt': 'Please solve this CAPTCHA to continue: {num1} + {num2} = ? Send the answer.',
        'captcha_success': 'CAPTCHA verified! Access granted.',
        'captcha_fail': 'Wrong answer. Try again.',
        'balance_info': '💰 Your Points: {points}\n💸 Your USDT: {usdt}',
        'stats_info': '📊 Your Stats:\nTotal Ads Watched: {ads}\nReferrals: {referrals}\nTotal Earned Points: {total_points}',
        'ads_instruction': 'Click "Watch Ad" to earn points.\nLimits: 30 ads/session, 1h cooldown, max 90 ads/day.',
        'watch_ad': 'Watch Ad',
        'ad_watched': 'Ad watched! You earned {points} points.',
        'session_limit': 'Session limit reached. Cooldown: {time} minutes.',
        'daily_limit': 'Daily ad limit reached. Try again tomorrow.',
        'referral_link': 'Your referral link: {link}\nReferrals: {referrals}\nReferral Points: {points}',
        'leaderboard_title': '🏆 Leaderboard (Top 10 by Points):',
        'no_leaderboard': 'No users on leaderboard yet.',
        'swap_instruction': 'Send /swap <points> to convert to USDT (Rate: 1 point = {rate} USDT).',
        'swap_success': 'Swapped {points} points to {usdt} USDT. USDT Balance: {balance}',
        'swap_fail': 'Not enough points or invalid amount.',
        'withdraw_instruction': 'Send /withdraw <amount> <method> <wallet_address>\nMethods: binance, okx, trust\nMin: {min} USDT',
        'withdraw_success': 'Withdrawal request for {amount} USDT via {method} to {wallet} sent. Await admin approval.',
        'withdraw_fail': 'Error: Insufficient USDT, below min ({min}), invalid method, or invalid request.',
        'task_daily': 'Daily Check-in',
        'claim_daily': 'Claim Daily Points',
        'daily_claimed': 'Daily points claimed! You earned {points} points.',
        'daily_already': 'You already claimed today.',
        'task_follow': 'Follow Social Media',
        'claim_follow': 'Claim Follow Reward',
        'follow_instruction': 'Follow our channel: {link}\nThen click "Claim Follow Reward".',
        'follow_claimed': 'Follow reward claimed! You earned {points} points.',
        'follow_already': 'You already claimed this reward.',
        'admin_settings': '🔧 Admin Panel\n/set <key> <value> to change settings.\nCurrent:\n{settings}',
        'admin_requests': 'Pending Withdrawals:\n{requests}',
        'admin_analytics': '📈 Analytics:\nTotal Users: {users}\nTotal Ads Watched: {ads}\nTotal Withdrawals: {withdrawals} USDT',
        'approve_withdraw': '✅ Approve {id}',
        'deny_withdraw': '❌ Deny {id}',
        'setting_updated': 'Setting {key} updated to {value}.',
        'withdraw_approved': 'Withdrawal {id} approved.',
        'withdraw_denied': 'Withdrawal {id} denied.',
        'ad_error': 'Error loading ad. Try again later.'
    },
    'bn': {
        'choose_language': 'আর্নিং বটে স্বাগতম! আপনার ভাষা নির্বাচন করুন:',
        'menu': '🏠 প্রধান মেনু',
        'balance': '💰 ব্যালেন্স',
        'earn_ads': '📺 বিজ্ঞাপন থেকে উপার্জন',
        'tasks': '📋 টাস্কসমূহ',
        'referral': '🤝 রেফারেল',
        'leaderboard': '🏆 লিডারবোর্ড',
        'swap': '🔄 পয়েন্ট USDT-এ রূপান্তর',
        'withdraw': '💸 USDT উত্তোলন',
        'admin': '🔧 অ্যাডমিন প্যানেল',
        'back': '⬅ মেনুতে ফিরে যান',
        'stats': '📊 আপনার পরিসংখ্যান',
        'captcha_prompt': 'অনুগ্রহ করে এই CAPTCHA সমাধান করুন: {num1} + {num2} = ? উত্তর পাঠান।',
        'captcha_success': 'CAPTCHA যাচাই হয়েছে! প্রবেশ অনুমোদিত।',
        'captcha_fail': 'ভুল উত্তর। আবার চেষ্টা করুন।',
        'balance_info': '💰 আপনার পয়েন্ট: {points}\n💸 আপনার USDT: {usdt}',
        'stats_info': '📊 আপনার পরিসংখ্যান:\nমোট বিজ্ঞাপন দেখা: {ads}\nরেফারেল: {referrals}\nমোট পয়েন্ট উপার্জন: {total_points}',
        'ads_instruction': '"বিজ্ঞাপন দেখুন" ক্লিক করুন পয়েন্ট উপার্জনের জন্য।\nসীমা: প্রতি সেশনে ৩০টি, ১ঘন্টা কুলডাউন, দৈনিক সর্বোচ্চ ৯০টি।',
        'watch_ad': 'বিজ্ঞাপন দেখুন',
        'ad_watched': 'বিজ্ঞাপন দেখা হয়েছে! আপনি {points} পয়েন্ট উপার্জন করেছেন।',
        'session_limit': 'সেশনের সীমা পৌঁছেছে। কুলডাউন: {time} মিনিট।',
        'daily_limit': 'দৈনিক বিজ্ঞাপন সীমা পৌঁছেছে। আগামীকাল চেষ্টা করুন।',
        'referral_link': 'আপনার রেফারেল লিঙ্ক: {link}\nরেফারেল: {referrals}\nরেফারেল পয়েন্ট: {points}',
        'leaderboard_title': '🏆 লিডারবোর্ড (পয়েন্ট অনুসারে শীর্ষ ১০):',
        'no_leaderboard': 'লিডারবোর্ডে এখনো কোনো ব্যবহারকারী নেই।',
        'swap_instruction': '/swap <points> পাঠান USDT-এ রূপান্তর করতে (রেট: ১ পয়েন্ট = {rate} USDT)।',
        'swap_success': '{points} পয়েন্ট {usdt} USDT-এ রূপান্তরিত। USDT ব্যালেন্স: {balance}',
        'swap_fail': 'পর্যাপ্ত পয়েন্ট নেই বা অবৈধ পরিমাণ।',
        'withdraw_instruction': '/withdraw <amount> <method> <wallet_address> পাঠান।\nমেথড: binance, okx, trust\nন্যূনতম: {min} USDT',
        'withdraw_success': '{amount} USDT {method} এর মাধ্যমে {wallet}-এ উত্তোলন অনুরোধ পাঠানো হয়েছে। অ্যাডমিন অনুমোদনের অপেক্ষায়।',
        'withdraw_fail': 'ত্রুটি: অপর্যাপ্ত USDT, ন্যূনতম ({min}) এর নিচে, অবৈধ মেথড, বা অবৈধ অনুরোধ।',
        'task_daily': 'দৈনিক চেক-ইন',
        'claim_daily': 'দৈনিক পয়েন্ট দাবি করুন',
        'daily_claimed': 'দৈনিক পয়েন্ট দাবি করা হয়েছে! আপনি {points} পয়েন্ট উপার্জন করেছেন।',
        'daily_already': 'আপনি আজকের দাবি করে ফেলেছেন।',
        'task_follow': 'সোশ্যাল মিডিয়া ফলো',
        'claim_follow': 'ফলো পুরস্কার দাবি করুন',
        'follow_instruction': 'আমাদের চ্যানেল ফলো করুন: {link}\nতারপর "ফলো পুরস্কার দাবি করুন" ক্লিক করুন।',
        'follow_claimed': 'ফলো পুরস্কার দাবি করা হয়েছে! আপনি {points} পয়েন্ট উপার্জন করেছেন।',
        'follow_already': 'আপনি এই পুরস্কার ইতিমধ্যে দাবি করেছেন।',
        'admin_settings': '🔧 অ্যাডমিন প্যানেল\n/set <key> <value> পাঠান সেটিংস পরিবর্তন করতে।\nবর্তমান:\n{settings}',
        'admin_requests': 'পেন্ডিং উত্তোলনসমূহ:\n{requests}',
        'admin_analytics': '📈 পরিসংখ্যান:\nমোট ব্যবহারকারী: {users}\nমোট বিজ্ঞাপন দেখা: {ads}\nমোট উত্তোলন: {withdrawals} USDT',
        'approve_withdraw': '✅ অনুমোদন {id}',
        'deny_withdraw': '❌ প্রত্যাখ্যান {id}',
        'setting_updated': 'সেটিং {key} {value}-এ আপডেট হয়েছে।',
        'withdraw_approved': 'উত্তোলন {id} অনুমোদিত।',
        'withdraw_denied': 'উত্তোলন {id} প্রত্যাখ্যাত।',
        'ad_error': 'বিজ্ঞাপন লোড করতে ত্রুটি। পরে আবার চেষ্টা করুন।'
    }
}

# Default settings
default_settings = {
    'points_per_ad': 1.0,
    'points_per_referral': 10.0,
    'points_daily_task': 5.0,
    'points_follow_task': 20.0,
    'ads_per_session': 30,
    'cooldown_seconds': 3600,
    'daily_ads_limit': 90,
    'usdt_rate': 0.0005,  # 1 point = 0.0005 USDT (adjust for profit margin)
    'min_withdraw': 1.0
}
for key, value in default_settings.items():
    if not settings_collection.find_one({'key': key}):
        settings_collection.insert_one({'key': key, 'value': value})

# Allowed payment methods
ALLOWED_METHODS = ['binance', 'okx', 'trust']

# Helper functions
def get_setting(key):
    setting = settings_collection.find_one({'key': key})
    return setting['value'] if setting else default_settings.get(key, 0)

def update_setting(key, value):
    settings_collection.update_one({'key': key}, {'$set': {'value': value}}, upsert=True)

def get_user_lang(user_id):
    user = users_collection.find_one({'user_id': user_id})
    return user['language'] if user else 'en'

def update_user_lang(user_id, lang):
    users_collection.update_one({'user_id': user_id}, {'$set': {'language': lang}}, upsert=True)

def register_user(user_id, username, referred_by=None):
    if not users_collection.find_one({'user_id': user_id}):
        users_collection.insert_one({
            'user_id': user_id,
            'username': username,
            'language': 'en',
            'points': 0.0,
            'usdt_balance': 0.0,
            'referred_by': referred_by,
            'referrals': 0,
            'last_ad_time': None,
            'ads_today': 0,
            'session_ads': 0,
            'last_daily_claim': None
        })
    if referred_by and referred_by != user_id:
        points = float(get_setting('points_per_referral'))
        users_collection.update_one({'user_id': referred_by}, {'$inc': {'referrals': 1, 'points': points}})
    conn.commit()

def can_watch_ad(user_id):
    now = datetime.datetime.now()
    c.execute('SELECT last_ad_time, ads_today, session_ads FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    last_ad_str, ads_today, session_ads = row if row else (None, 0, 0)

    last_ad = datetime.datetime.fromisoformat(last_ad_str) if last_ad_str else None

    if last_ad is None or last_ad.date() < now.date():
        c.execute('UPDATE users SET ads_today = 0, session_ads = 0, last_ad_time = ? WHERE user_id = ?', (now.isoformat(), user_id))
        ads_today = 0
        session_ads = 0
        conn.commit()

    daily_limit = int(get_setting('daily_ads_limit'))
    if ads_today >= daily_limit:
        return False, 'daily'

    ads_per_session = int(get_setting('ads_per_session'))
    if session_ads >= ads_per_session:
        cooldown = int(get_setting('cooldown_seconds'))
        if (now - last_ad).total_seconds() >= cooldown:
            c.execute('UPDATE users SET session_ads = 0 WHERE user_id = ?', (user_id,))
            conn.commit()
            return True, None
        else:
            remaining = cooldown - (now - last_ad).total_seconds()
            return False, remaining / 60
    return True, None

def send_main_menu(user_id, lang):
    texts = languages[lang]
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(texts['earn_ads'], callback_data='earn_ads'))
    markup.add(InlineKeyboardButton(texts['tasks'], callback_data='tasks'))
    markup.add(InlineKeyboardButton(texts['referral'], callback_data='referral'))
    markup.add(InlineKeyboardButton(texts['leaderboard'], callback_data='leaderboard'))
    markup.add(InlineKeyboardButton(texts['swap'], callback_data='swap'))
    markup.add(InlineKeyboardButton(texts['withdraw'], callback_data='withdraw'))
    if user_id == ADMIN_ID:
        markup.add(InlineKeyboardButton(texts['admin'], callback_data='admin'))
    bot.send_message(user_id, texts['menu'], reply_markup=markup)

# Handlers
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    username = message.from_user.username or f'user_{user_id}'
    args = message.text.split()
    referred_by = int(args[1]) if len(args) > 1 else None
    register_user(user_id, username, referred_by)
    lang = get_user_lang(user_id)
    if lang == 'en':  # Default, but prompt for choice if not set
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('English', callback_data='set_lang_en'))
        markup.add(InlineKeyboardButton('বাংলা', callback_data='set_lang_bn'))
        bot.send_message(user_id, languages['en']['choose_language'], reply_markup=markup)
    else:
        send_main_menu(user_id, lang)

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_lang_'))
def set_lang_handler(call):
    user_id = call.message.chat.id
    lang = call.data.split('_')[2]
    update_user_lang(user_id, lang)
    bot.delete_message(user_id, call.message.message_id)
    send_main_menu(user_id, lang)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    lang = get_user_lang(user_id)
    texts = languages[lang]
    data = call.data

    if data == 'earn_ads':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(texts['watch_ad'], callback_data='watch_ad'))
        bot.edit_message_text(texts['ads_instruction'], user_id, call.message.message_id, reply_markup=markup)

    elif data == 'watch_ad':
        can, info = can_watch_ad(user_id)
        if can:
            points = float(get_setting('points_per_ad'))
            now = datetime.datetime.now()
            c.execute('UPDATE users SET points = points + ?, ads_today = ads_today + 1, session_ads = session_ads + 1, last_ad_time = ? WHERE user_id = ?', (points, now.isoformat(), user_id))
            conn.commit()
            # Integrate real ad display for profit (e.g., send ad link from ad network API)
            # For example: bot.send_message(user_id, "Watch this ad: https://ad-network-link.com")
            # Revenue comes from ad network payouts to bot owner.
            bot.answer_callback_query(call.id, texts['ad_watched'].format(points=points))
        else:
            if info == 'daily':
                bot.answer_callback_query(call.id, texts['daily_limit'], show_alert=True)
            else:
                bot.answer_callback_query(call.id, texts['session_limit'].format(time=round(info)), show_alert=True)

    elif data == 'tasks':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(texts['claim_daily'], callback_data='claim_daily'))
        bot.edit_message_text(texts['tasks'], user_id, call.message.message_id, reply_markup=markup)

    elif data == 'claim_daily':
        now = datetime.datetime.now()
        c.execute('SELECT last_daily_claim FROM users WHERE user_id = ?', (user_id,))
        last_claim_str = c.fetchone()[0]
        last_claim = datetime.datetime.fromisoformat(last_claim_str) if last_claim_str else None
        if last_claim is None or last_claim.date() < now.date():
            points = float(get_setting('points_daily_task'))
            c.execute('UPDATE users SET points = points + ?, last_daily_claim = ? WHERE user_id = ?', (points, now.isoformat(), user_id))
            conn.commit()
            bot.answer_callback_query(call.id, texts['daily_claimed'].format(points=points))
        else:
            bot.answer_callback_query(call.id, texts['daily_already'], show_alert=True)

    elif data == 'referral':
        ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        c.execute('SELECT referrals, points FROM users WHERE user_id = ?', (user_id,))
        referrals, points = c.fetchone()
        points_from_ref = referrals * float(get_setting('points_per_referral'))  # Approximate
        bot.edit_message_text(texts['referral_link'].format(link=ref_link, referrals=referrals, points=points_from_ref), user_id, call.message.message_id)

    elif data == 'leaderboard':
        c.execute('SELECT username, points FROM users ORDER BY points DESC LIMIT 10')
        rows = c.fetchall()
        if rows:
            lb = '\n'.join(f"{i+1}. {row[0]} - {row[1]} points" for i, row in enumerate(rows))
            bot.edit_message_text(texts['leaderboard_title'] + '\n' + lb, user_id, call.message.message_id)
        else:
            bot.edit_message_text(texts['no_leaderboard'], user_id, call.message.message_id)

    elif data == 'swap':
        rate = float(get_setting('usdt_rate'))
        bot.edit_message_text(texts['swap_instruction'].format(rate=rate), user_id, call.message.message_id)

    elif data == 'withdraw':
        bot.edit_message_text(texts['withdraw_instruction'], user_id, call.message.message_id)

    elif data == 'admin':
        if user_id != ADMIN_ID:
            return
        settings_str = '\n'.join(f"{k}: {get_setting(k)}" for k in default_settings)
        c.execute("SELECT id, user_id, amount, method, wallet FROM withdraw_requests WHERE status = 'pending'")
        requests = c.fetchall()
        requests_str = '\n'.join(f"ID: {r[0]}, User: {r[1]}, Amount: {r[2]}, Method: {r[3]}, Wallet: {r[4]}" for r in requests) or 'None'
        markup = InlineKeyboardMarkup()
        for r in requests:
            markup.add(InlineKeyboardButton(texts['approve_withdraw'].format(id=r[0]), callback_data=f'approve_{r[0]}'))
            markup.add(InlineKeyboardButton(texts['deny_withdraw'].format(id=r[0]), callback_data=f'deny_{r[0]}'))
        bot.edit_message_text(texts['admin_settings'].format(settings=settings_str) + '\n\n' + texts['admin_requests'].format(requests=requests_str), user_id, call.message.message_id, reply_markup=markup)

    elif data.startswith('approve_'):
        if user_id != ADMIN_ID:
            return
        req_id = int(data.split('_')[1])
        c.execute("UPDATE withdraw_requests SET status = 'approved' WHERE id = ?", (req_id,))
        conn.commit()
        bot.answer_callback_query(call.id, texts['withdraw_approved'].format(id=req_id))

    elif data.startswith('deny_'):
        if user_id != ADMIN_ID:
            return
        req_id = int(data.split('_')[1])
        c.execute("UPDATE withdraw_requests SET status = 'denied' WHERE id = ?", (req_id,))
        conn.commit()
        bot.answer_callback_query(call.id, texts['withdraw_denied'].format(id=req_id))

@bot.message_handler(commands=['swap'])
def swap_handler(message):
    user_id = message.chat.id
    lang = get_user_lang(user_id)
    texts = languages[lang]
    try:
        points = float(message.text.split()[1])
        c.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
        current_points = c.fetchone()[0]
        if points > current_points or points <= 0:
            bot.reply_to(message, texts['swap_fail'])
            return
        rate = float(get_setting('usdt_rate'))
        usdt = points * rate
        c.execute('UPDATE users SET points = points - ?, usdt_balance = usdt_balance + ? WHERE user_id = ?', (points, usdt, user_id))
        conn.commit()
        c.execute('SELECT usdt_balance FROM users WHERE user_id = ?', (user_id,))
        balance = c.fetchone()[0]
        bot.reply_to(message, texts['swap_success'].format(points=points, usdt=usdt, balance=balance))
    except:
        bot.reply_to(message, texts['swap_fail'])

@bot.message_handler(commands=['withdraw'])
def withdraw_handler(message):
    user_id = message.chat.id
    lang = get_user_lang(user_id)
    texts = languages[lang]
    try:
        args = message.text.split()[1:]
        amount = float(args[0])
        method = args[1].lower()
        wallet = args[2]
        if method not in ALLOWED_METHODS:
            bot.reply_to(message, texts['withdraw_fail'].format(min=get_setting('min_withdraw')))
            return
        min_w = float(get_setting('min_withdraw'))
        c.execute('SELECT usdt_balance FROM users WHERE user_id = ?', (user_id,))
        balance = c.fetchone()[0]
        if amount > balance or amount <= 0 or amount < min_w:
            bot.reply_to(message, texts['withdraw_fail'].format(min=min_w))
            return
        c.execute('INSERT INTO withdraw_requests (user_id, amount, method, wallet) VALUES (?, ?, ?, ?)', (user_id, amount, method, wallet))
        c.execute('UPDATE users SET usdt_balance = usdt_balance - ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
        bot.reply_to(message, texts['withdraw_success'].format(amount=amount, method=method, wallet=wallet))
        # Notify admin
        bot.send_message(ADMIN_ID, f"New withdraw request: User {user_id}, Amount {amount}, Method {method}, Wallet {wallet}")
    except:
        bot.reply_to(message, texts['withdraw_fail'].format(min=get_setting('min_withdraw')))

@bot.message_handler(commands=['set'])
def set_handler(message):
    user_id = message.chat.id
    if user_id != ADMIN_ID:
        return
    lang = get_user_lang(user_id)
    texts = languages[lang]
    try:
        args = message.text.split()[1:]
        key = args[0]
        value = args[1]
        if key in default_settings:
            update_setting(key, value)
            bot.reply_to(message, texts['setting_updated'].format(key=key, value=value))
    except:
        bot.reply_to(message, 'Invalid /set command.')

# Start the bot
bot.infinity_polling()
