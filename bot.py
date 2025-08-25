import telebot
import certifi
import urllib.parse
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import datetime
import os

# --- Bot Token & Admin ID ---
# Token-ti Render.com er Environment theke neya hobe
TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 6277866627 # Apnar Admin ID


TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("CRITICAL ERROR: BOT_TOKEN environment variable not found!")
    exit()

bot = telebot.TeleBot(TOKEN)

# --- MongoDB Setup ---
MONGO_URI = os.environ.get('MONGO_URI')
if not MONGO_URI:
    print("CRITICAL ERROR: MONGO_URI environment variable not found!")
    exit()

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)
db = client['earning_bot']
users_collection = db['users']
settings_collection = db['settings']
withdraw_requests_collection = db['withdraw_requests']


# --- Language Dictionaries (Adsterra link er jonno notun text add kora hoyeche) ---
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
        'ads_instruction': 'Click "Watch Ad" to get a link and earn points.\nLimits: 30 ads/session, 1h cooldown, max 90 ads/day.',
        'watch_ad': 'Watch Ad',
        'ad_watched': 'Ad link generated! You earned {points} points.',
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
        'admin_settings': '🔧 Admin Panel\n/set <key> <value> to change settings.\nCurrent:\n{settings}',
        'admin_requests': 'Pending Withdrawals:\n{requests}',
        'approve_withdraw': '✅ Approve {id}',
        'deny_withdraw': '❌ Deny {id}',
        'setting_updated': 'Setting {key} updated to {value}.',
        'withdraw_approved': 'Withdrawal {id} approved.',
        'withdraw_denied': 'Withdrawal {id} denied.',
        'ad_link_message': 'Click the button below to watch the ad. Points have been added to your balance.',
        'ad_link_button': '🔗 Watch Ad Now',
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
        'ads_instruction': '"বিজ্ঞাপন দেখুন" ক্লিক করে লিঙ্ক নিন এবং পয়েন্ট উপার্জন করুন।\nসীমা: প্রতি সেশনে ৩০টি, ১ঘন্টা কুলডাউন, দৈনিক সর্বোচ্চ ৯০টি।',
        'watch_ad': 'বিজ্ঞাপন দেখুন',
        'ad_watched': 'বিজ্ঞাপনের লিঙ্ক তৈরি হয়েছে! আপনি {points} পয়েন্ট উপার্জন করেছেন।',
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
        'admin_settings': '🔧 অ্যাডমিন প্যানেল\n/set <key> <value> পাঠান সেটিংস পরিবর্তন করতে।\nবর্তমান:\n{settings}',
        'admin_requests': 'পেন্ডিং উত্তোলনসমূহ:\n{requests}',
        'approve_withdraw': '✅ অনুমোদন {id}',
        'deny_withdraw': '❌ প্রত্যাখ্যান {id}',
        'setting_updated': 'সেটিং {key} {value}-এ আপডেট হয়েছে।',
        'withdraw_approved': 'উত্তোলন {id} অনুমোদিত।',
        'withdraw_denied': 'উত্তোলন {id} প্রত্যাখ্যাত।',
        'ad_link_message': 'বিজ্ঞাপন দেখতে নিচের বাটনে ক্লিক করুন। আপনার ব্যালেন্সে পয়েন্ট যোগ করা হয়েছে।',
        'ad_link_button': '🔗 এখনই বিজ্ঞাপন দেখুন',
    }
}

# --- Default Settings (Adsterra link add kora hoyeche) ---
default_settings = {
    'points_per_ad': 1.0,
    'points_per_referral': 10.0,
    'points_daily_task': 5.0,
    'usdt_rate': 0.0005,
    'min_withdraw': 1.0,
    'ads_per_session': 30,
    'cooldown_seconds': 3600,
    'daily_ads_limit': 90,
    'ad_link': 'http://pl26780328.profitableratecpm.com/2e/7b/58/2e7b58d34093cfaae6a3392a1b1d6043.js' # Ekhane apnar Adsterra link din
}
for key, value in default_settings.items():
    if not settings_collection.find_one({'key': key}):
        settings_collection.insert_one({'key': key, 'value': value})

ALLOWED_METHODS = ['binance', 'okx', 'trust']

# --- Helper Functions (Unchanged) ---
def get_setting(key):
    setting = settings_collection.find_one({'key': key})
    return setting['value'] if setting else default_settings.get(key)

def update_setting(key, value):
    try:
        # Try to convert to float if possible, otherwise keep as string
        value = float(value)
    except (ValueError, TypeError):
        pass # Keep as string if it's not a number (like the ad_link)
    settings_collection.update_one({'key': key}, {'$set': {'value': value}}, upsert=True)

def get_user_lang(user_id):
    user = users_collection.find_one({'user_id': user_id})
    return user.get('language', 'en') if user else 'en'

def update_user_lang(user_id, lang):
    users_collection.update_one({'user_id': user_id}, {'$set': {'language': lang}}, upsert=True)

def register_user(user_id, username, referred_by=None):
    if not users_collection.find_one({'user_id': user_id}):
        new_user = {
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
            'last_daily_claim': None,
            'total_ads_watched': 0,
            'total_points_earned': 0.0
        }
        users_collection.insert_one(new_user)
        if referred_by and referred_by != user_id:
            points = float(get_setting('points_per_referral'))
            users_collection.update_one({'user_id': int(referred_by)}, {'$inc': {'referrals': 1, 'points': points}})

def can_watch_ad(user_id):
    now = datetime.datetime.now()
    user = users_collection.find_one({'user_id': user_id})
    if not user:
        return False, 'not_found'

    last_ad_time = user.get('last_ad_time')
    ads_today = user.get('ads_today', 0)
    session_ads = user.get('session_ads', 0)

    if last_ad_time is None or last_ad_time.date() < now.date():
        users_collection.update_one({'user_id': user_id}, {'$set': {'ads_today': 0, 'session_ads': 0}})
        ads_today = 0
        session_ads = 0

    daily_limit = int(get_setting('daily_ads_limit'))
    if ads_today >= daily_limit:
        return False, 'daily'

    ads_per_session = int(get_setting('ads_per_session'))
    if session_ads >= ads_per_session:
        cooldown = int(get_setting('cooldown_seconds'))
        if last_ad_time and (now - last_ad_time).total_seconds() >= cooldown:
            users_collection.update_one({'user_id': user_id}, {'$set': {'session_ads': 0}})
            return True, None
        else:
            remaining = cooldown - (now - last_ad_time).total_seconds() if last_ad_time else cooldown
            return False, remaining / 60
    return True, None

def send_main_menu(user_id, lang):
    texts = languages[lang]
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(texts['earn_ads'], callback_data='earn_ads'),
        InlineKeyboardButton(texts['tasks'], callback_data='tasks'),
        InlineKeyboardButton(texts['referral'], callback_data='referral'),
        InlineKeyboardButton(texts['leaderboard'], callback_data='leaderboard'),
        InlineKeyboardButton(texts['swap'], callback_data='swap'),
        InlineKeyboardButton(texts['withdraw'], callback_data='withdraw'),
        InlineKeyboardButton(texts['balance'], callback_data='balance'),
        InlineKeyboardButton(texts['stats'], callback_data='stats')
    )
    if user_id == ADMIN_ID:
        markup.add(InlineKeyboardButton(texts['admin'], callback_data='admin'))
    bot.send_message(user_id, texts['menu'], reply_markup=markup)

# --- Handlers (Main logic unchanged, only 'watch_ad' is modified) ---
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    username = message.from_user.username or f'user_{user_id}'
    args = message.text.split()
    referred_by = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    
    user = users_collection.find_one({'user_id': user_id})
    if not user:
        register_user(user_id, username, referred_by)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('English', callback_data='set_lang_en'))
        markup.add(InlineKeyboardButton('বাংলা', callback_data='set_lang_bn'))
        bot.send_message(user_id, languages['en']['choose_language'], reply_markup=markup)
    else:
        lang = get_user_lang(user_id)
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
    user = users_collection.find_one({'user_id': user_id})

    if not user:
        bot.answer_callback_query(call.id, "Please /start the bot first.", show_alert=True)
        return

    if data == 'earn_ads':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(texts['watch_ad'], callback_data='watch_ad'))
        markup.add(InlineKeyboardButton(texts['back'], callback_data='main_menu'))
        bot.edit_message_text(texts['ads_instruction'], user_id, call.message.message_id, reply_markup=markup)

    # MODIFIED LOGIC FOR ADSTERRA
    elif data == 'watch_ad':
        can, info = can_watch_ad(user_id)
        if can:
            points = float(get_setting('points_per_ad'))
            ad_link = get_setting('ad_link')

            # Create a button that links to the ad
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(texts['ad_link_button'], url=ad_link))
            markup.add(InlineKeyboardButton(texts['back'], callback_data='earn_ads'))

            # Edit the message to show the ad link
            bot.edit_message_text(texts['ad_link_message'], user_id, call.message.message_id, reply_markup=markup)

            # Give points immediately after sending the link (trust-based)
            now = datetime.datetime.now()
            users_collection.update_one(
                {'user_id': user_id},
                {
                    '$inc': {'points': points, 'ads_today': 1, 'session_ads': 1, 'total_ads_watched': 1, 'total_points_earned': points},
                    '$set': {'last_ad_time': now}
                }
            )
            # Notify user they got points
            bot.answer_callback_query(call.id, texts['ad_watched'].format(points=points))
        else:
            # Limit handling remains the same
            if info == 'daily':
                bot.answer_callback_query(call.id, texts['daily_limit'], show_alert=True)
            elif info == 'not_found':
                 bot.answer_callback_query(call.id, "User not found. Please /start the bot.", show_alert=True)
            else:
                bot.answer_callback_query(call.id, texts['session_limit'].format(time=round(info)), show_alert=True)

    elif data == 'tasks':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(texts['claim_daily'], callback_data='claim_daily'))
        markup.add(InlineKeyboardButton(texts['back'], callback_data='main_menu'))
        bot.edit_message_text(texts['tasks'], user_id, call.message.message_id, reply_markup=markup)

    elif data == 'claim_daily':
        now = datetime.datetime.now()
        last_claim = user.get('last_daily_claim')
        if last_claim is None or last_claim.date() < now.date():
            points = float(get_setting('points_daily_task'))
            users_collection.update_one(
                {'user_id': user_id},
                {
                    '$inc': {'points': points, 'total_points_earned': points},
                    '$set': {'last_daily_claim': now}
                }
            )
            bot.answer_callback_query(call.id, texts['daily_claimed'].format(points=points))
        else:
            bot.answer_callback_query(call.id, texts['daily_already'], show_alert=True)

    # --- Other handlers are unchanged ---
    elif data == 'referral':
        ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        referrals = user.get('referrals', 0)
        points_from_ref = referrals * float(get_setting('points_per_referral'))
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(texts['back'], callback_data='main_menu'))
        bot.edit_message_text(texts['referral_link'].format(link=ref_link, referrals=referrals, points=points_from_ref), user_id, call.message.message_id, reply_markup=markup)

    elif data == 'leaderboard':
        top_users = users_collection.find().sort('points', -1).limit(10)
        lb_list = list(top_users)
        if lb_list:
            lb = '\n'.join(f"{i+1}. {u.get('username', 'N/A')} - {u.get('points', 0):.2f} points" for i, u in enumerate(lb_list))
            text = texts['leaderboard_title'] + '\n\n' + lb
        else:
            text = texts['no_leaderboard']
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(texts['back'], callback_data='main_menu'))
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    elif data == 'swap':
        rate = float(get_setting('usdt_rate'))
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(texts['back'], callback_data='main_menu'))
        bot.edit_message_text(texts['swap_instruction'].format(rate=rate), user_id, call.message.message_id, reply_markup=markup)

    elif data == 'withdraw':
        min_withdraw = get_setting('min_withdraw')
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(texts['back'], callback_data='main_menu'))
        bot.edit_message_text(texts['withdraw_instruction'].format(min=min_withdraw), user_id, call.message.message_id, reply_markup=markup)

    elif data == 'balance':
        points = user.get('points', 0)
        usdt = user.get('usdt_balance', 0)
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(texts['back'], callback_data='main_menu'))
        bot.edit_message_text(texts['balance_info'].format(points=f"{points:.2f}", usdt=f"{usdt:.4f}"), user_id, call.message.message_id, reply_markup=markup)

    elif data == 'stats':
        ads = user.get('total_ads_watched', 0)
        referrals = user.get('referrals', 0)
        total_points = user.get('total_points_earned', 0)
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(texts['back'], callback_data='main_menu'))
        bot.edit_message_text(texts['stats_info'].format(ads=ads, referrals=referrals, total_points=f"{total_points:.2f}"), user_id, call.message.message_id, reply_markup=markup)

    elif data == 'admin':
        if user_id != ADMIN_ID: return
        settings_str = '\n'.join(f"{k}: {get_setting(k)}" for k in default_settings)
        requests = list(withdraw_requests_collection.find({'status': 'pending'}))
        requests_str = '\n'.join(f"ID: {r['_id']}, User: {r['user_id']}, Amount: {r['amount']}" for r in requests) or 'None'
        markup = InlineKeyboardMarkup()
        for r in requests:
            req_id = str(r['_id'])
            markup.add(InlineKeyboardButton(texts['approve_withdraw'].format(id=req_id[-4:]), callback_data=f'approve_{req_id}'))
            markup.add(InlineKeyboardButton(texts['deny_withdraw'].format(id=req_id[-4:]), callback_data=f'deny_{req_id}'))
        markup.add(InlineKeyboardButton(texts['back'], callback_data='main_menu'))
        bot.edit_message_text(texts['admin_settings'].format(settings=settings_str) + '\n\n' + texts['admin_requests'].format(requests=requests_str), user_id, call.message.message_id, reply_markup=markup)

    elif data.startswith('approve_'):
        if user_id != ADMIN_ID: return
        from bson.objectid import ObjectId
        req_id = ObjectId(data.split('_')[1])
        withdraw_requests_collection.update_one({'_id': req_id}, {'$set': {'status': 'approved'}})
        bot.answer_callback_query(call.id, texts['withdraw_approved'].format(id=str(req_id)[-4:]))

    elif data.startswith('deny_'):
        if user_id != ADMIN_ID: return
        from bson.objectid import ObjectId
        req_id = ObjectId(data.split('_')[1])
        request = withdraw_requests_collection.find_one({'_id': req_id})
        if request:
            users_collection.update_one({'user_id': request['user_id']}, {'$inc': {'usdt_balance': request['amount']}})
            withdraw_requests_collection.update_one({'_id': req_id}, {'$set': {'status': 'denied'}})
            bot.answer_callback_query(call.id, texts['withdraw_denied'].format(id=str(req_id)[-4:]))

    elif data == 'main_menu':
        send_main_menu(user_id, lang)
        bot.delete_message(user_id, call.message.message_id)


@bot.message_handler(commands=['swap', 'withdraw', 'set'])
def command_handlers(message):
    user_id = message.chat.id
    lang = get_user_lang(user_id)
    texts = languages[lang]
    user = users_collection.find_one({'user_id': user_id})
    command = message.text.split()[0]

    if command == '/swap':
        if not user: return bot.reply_to(message, "Please /start the bot first.")
        try:
            points_to_swap = float(message.text.split()[1])
            if points_to_swap > user.get('points', 0) or points_to_swap <= 0:
                return bot.reply_to(message, texts['swap_fail'])
            rate = float(get_setting('usdt_rate'))
            usdt_earned = points_to_swap * rate
            users_collection.update_one({'user_id': user_id}, {'$inc': {'points': -points_to_swap, 'usdt_balance': usdt_earned}})
            new_balance = users_collection.find_one({'user_id': user_id}).get('usdt_balance', 0)
            bot.reply_to(message, texts['swap_success'].format(points=points_to_swap, usdt=f"{usdt_earned:.4f}", balance=f"{new_balance:.4f}"))
        except (IndexError, ValueError):
            bot.reply_to(message, texts['swap_fail'])
    
    elif command == '/withdraw':
        min_w = float(get_setting('min_withdraw'))
        if not user: return bot.reply_to(message, "Please /start the bot first.")
        try:
            args = message.text.split()[1:]
            amount, method, wallet = float(args[0]), args[1].lower(), args[2]
            if method not in ALLOWED_METHODS or amount > user.get('usdt_balance', 0) or amount <= 0 or amount < min_w:
                return bot.reply_to(message, texts['withdraw_fail'].format(min=min_w))
            
            users_collection.update_one({'user_id': user_id}, {'$inc': {'usdt_balance': -amount}})
            withdraw_requests_collection.insert_one({'user_id': user_id, 'amount': amount, 'method': method, 'wallet': wallet, 'status': 'pending', 'timestamp': datetime.datetime.now()})
            bot.reply_to(message, texts['withdraw_success'].format(amount=amount, method=method, wallet=wallet))
            bot.send_message(ADMIN_ID, f"New withdraw request: User {user_id}, Amount {amount}, Method {method}, Wallet {wallet}")
        except (IndexError, ValueError):
            bot.reply_to(message, texts['withdraw_fail'].format(min=min_w))

    elif command == '/set':
        if user_id != ADMIN_ID: return
        try:
            args = message.text.split(maxsplit=2)[1:]
            key, value = args[0], args[1]
            if key in default_settings:
                update_setting(key, value)
                bot.reply_to(message, texts['setting_updated'].format(key=key, value=value))
            else:
                bot.reply_to(message, f"'{key}' is not a valid setting.")
        except IndexError:
            bot.reply_to(message, 'Invalid command. Use: /set <key> <value>')

# --- Bot Polling ---
print("Bot is running...")
bot.remove_webhook()  
bot.infinity_polling()
