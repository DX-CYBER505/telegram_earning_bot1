# Pochi Pochi Earning Bot

A multi-language Telegram earning bot with a web dashboard, allowing users to earn points by watching ads, completing tasks, and referring friends. Points can be swapped for USDT, with manual withdrawals approved by the admin. The project uses Python (backend), Java (ad server), and HTML/JavaScript (frontend), deployed on Render.

## Features
- **Ad Viewing**: Earn points via Adsterra Popunder ads (30 ads/session, 90/day, 1-hour cooldown).
- **Tasks**: Daily check-in and follow @PochiPochiNews.
- **Referral System**: Earn points for referrals.
- **Leaderboard**: Top 10 users by points.
- **USDT Swap**: Convert points to USDT (0.0005 USDT/point).
- **Withdrawals**: Manual USDT withdrawals (Binance, OKX, Trust Wallet).
- **Admin Panel**: Manage settings and withdrawals.
- **Security**: CAPTCHA prevents bot abuse.
- **Web Dashboard**: View balance, stats, and leaderboard.
- **Dual-Language**: English and Bangla support.

## Project Structure
```
telegram_earning_bot/
├── backend/
│   ├── bot.py
│   ├── requirements.txt
│   └── render.yaml
├── adserver/
│   ├── src/main/java/com/earningbot/AdServer.java
│   ├── pom.xml
│   └── render.yaml
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── styles.css
│   └── render.yaml
├── README.md
└── .gitignore
```

## Prerequisites
- Python 3.8+
- Java 17+ (with Maven)
- MongoDB Atlas account
- Telegram bot token (@BotFather)
- Adsterra account with Popunder ad unit
- Render account
- Git installed

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/telegram_earning_bot.git
cd telegram_earning_bot
```

### 2. Backend Setup (Python)
- Install dependencies:
  ```bash
  cd backend
  pip install -r requirements.txt
  ```
- Configure MongoDB Atlas:
  - Log in to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
  - Add your server IP or `0.0.0.0/0` in **Network Access**.
  - Ensure `botuser` and password match `MONGO_URI`.

### 3. Ad Server Setup (Java)
- Navigate to ad server directory:
  ```bash
  cd adserver
  ```
- Build with Maven:
  ```bash
  mvn clean install
  ```

### 4. Frontend Setup
- Host `frontend` files locally for testing:
  ```bash
  cd frontend
  python -m http.server 8000
  ```
- Access at `http://localhost:8000`.

### 5. Deploy to Render
- Sign up at [Render](https://render.com) and create a new project.
- Connect your GitHub repository to Render:
  - Fork or push this repository to your GitHub account.
  - In Render, click **New** > **Web Service** and select your repository.
- Deploy each component:
  - **Backend**:
    - Select `backend` as Root Directory.
    - Set environment variables: `TOKEN`, `MONGO_URI`, `ADSTERRA_API_TOKEN`.
    - After deployment, note the `RENDER_URL` (e.g., `https://pochi-backend.onrender.com`).
    - Update `AD_SERVER_URL` and `DASHBOARD_URL` in Render’s environment variables.
  - **Ad Server**:
    - Select `adserver` as Root Directory.
    - Note the `RENDER_URL` (e.g., `https://pochi-adserver.onrender.com`).
    - Update `AD_SERVER_URL` in `backend` environment variables.
  - **Frontend**:
    - Select `frontend` as Root Directory (Static Site).
    - Note the `RENDER_URL` (e.g., `https://pochi-frontend.onrender.com`).
    - Update `DASHBOARD_URL` in `backend` and `BACKEND_URL` in `frontend/script.js`.
- Example environment variables:
  ```bash
  TOKEN=7771736139:AAFhBdAAZF6-rV7YCX08hHK_FAYrHDe8sL0
  MONGO_URI=mongodb+srv://botuser:Xyz12345@tgbot.wh52pfi.mongodb.net/?retryWrites=true&w=majority&appName=tgbot
  ADSTERRA_API_TOKEN=0bc23fcccc35acd927d3e508222416b9
  AD_SERVER_URL=https://pochi-adserver.onrender.com/ad
  DASHBOARD_URL=https://pochi-frontend.onrender.com
  BACKEND_URL=https://pochi-backend.onrender.com
  ```

### 6. Test the Bot
- Message the bot on Telegram with `/start`.
- Complete CAPTCHA and test features: ad viewing, tasks, referrals, swap, withdrawals.
- Access the web dashboard at the frontend `RENDER_URL` with your Telegram user ID.

### 7. Update URLs
- After deployment, update:
  - `AD_SERVER_URL` in `backend` environment variables.
  - `DASHBOARD_URL` in `backend` environment variables.
  - `BACKEND_URL` in `frontend/script.js`.

## Security Notes
- Store `TOKEN`, `MONGO_URI`, and `ADSTERRA_API_TOKEN` in Render environment variables.
- Change MongoDB password after testing.
- Use HTTPS for all Render services.

## Profit Strategy
- **Ad Revenue**: Adsterra Popunder ads yield ~$10-$50 per 1000 views.
- **Payouts**: 1000 ad views = 1000 points = 0.5 USDT, yielding ~$9.5-$49.5 profit.
- **Settings**: Adjust via admin panel (`/set` command in Telegram).

## Contributing
Fork the repository, submit issues, or create pull requests.

## License
MIT License

---

# পোচি পোচি আর্নিং বট

একটি বহু-ভাষা টেলিগ্রাম বট এবং ওয়েব ড্যাশবোর্ড, যা বিজ্ঞাপন দেখে, টাস্ক সম্পন্ন করে এবং রেফারেলের মাধ্যমে পয়েন্ট উপার্জন করতে দেয়। পয়েন্ট USDT-এ রূপান্তর করা যায় এবং অ্যাডমিন ম্যানুয়ালি উত্তোলন অনুমোদন করে। প্রকল্পটি Python (ব্যাকএন্ড), Java (অ্যাড সার্ভার), এবং HTML/JavaScript (ফ্রন্টএন্ড) ব্যবহার করে, Render-এ ডিপ্লয় করা হয়।

## ফিচারসমূহ
- **বিজ্ঞাপন দেখা**: Adsterra পপআন্ডার বিজ্ঞাপন (প্রতি সেশনে ৩০টি, দৈনিক ৯০টি, ১ ঘন্টা কুলডাউন)।
- **টাস্কসমূহ**: দৈনিক চেক-ইন এবং @PochiPochiNews ফলো।
- **রেফারেল সিস্টেম**: রেফারেলের জন্য পয়েন্ট।
- **লিডারবোর্ড**: শীর্ষ ১০ ব্যবহারকারী।
- **USDT রূপান্তর**: ০.০০০৫ USDT/পয়েন্ট হারে।
- **উত্তোলন**: Binance, OKX, Trust Wallet এর মাধ্যমে ম্যানুয়াল উত্তোলন।
- **অ্যাডমিন প্যানেল**: সেটিংস এবং উত্তোলন পরিচালনা।
- **নিরাপত্তা**: CAPTCHA দিয়ে বট অপব্যবহার প্রতিরোধ।
- **ওয়েব ড্যাশবোর্ড**: ব্যালেন্স, পরিসংখ্যান, এবং লিডারবোর্ড।
- **দ্বৈত-ভাষা**: ইংরেজি এবং বাংলা।

## প্রয়োজনীয়তা
- Python 3.8+
- Java 17+ (Maven সহ)
- MongoDB Atlas অ্যাকাউন্ট
- টেলিগ্রাম বট টোকেন (@BotFather)
- Adsterra অ্যাকাউন্ট এবং পপআন্ডার অ্যাড ইউনিট
- Render অ্যাকাউন্ট
- Git ইনস্টল

## সেটআপ নির্দেশনা

### ১. রিপোজিটরি ক্লোন করুন
```bash
git clone https://github.com/your-username/telegram_earning_bot.git
cd telegram_earning_bot
```

### ২. ব্যাকএন্ড সেটআপ (Python)
- ডিপেন্ডেন্সি ইনস্টল করুন:
  ```bash
  cd backend
  pip install -r requirements.txt
  ```
- MongoDB Atlas কনফিগার করুন:
  - [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)-এ লগইন করুন।
  - **Network Access**-এ সার্ভার IP বা `0.0.0.0/0` যোগ করুন।
  - `MONGO_URI`-এর `botuser` এবং পাসওয়ার্ড মিলিয়ে নিন।

### ৩. অ্যাড সার্ভার সেটআপ (Java)
- অ্যাড সার্ভার ফোল্ডারে যান:
  ```bash
  cd adserver
  ```
- Maven দিয়ে বিল্ড করুন:
  ```bash
  mvn clean install
  ```

### ৪. ফ্রন্টএন্ড সেটআপ
- স্থানীয়ভাবে টেস্ট করুন:
  ```bash
  cd frontend
  python -m http.server 8000
  ```
- `http://localhost:8000`-এ দেখুন।

### ৫. Render-এ ডিপ্লয় করুন
- [Render](https://render.com)-এ সাইন আপ করুন এবং নতুন প্রকল্প তৈরি করুন।
- GitHub রিপোজিটরি সংযুক্ত করুন:
  - এই রিপোজিটরি ফর্ক করুন বা আপনার GitHub-এ পুশ করুন।
  - Render-এ **New** > **Web Service** ক্লিক করুন এবং রিপোজিটরি নির্বাচন করুন।
- প্রতিটি উপাদান ডিপ্লয় করুন:
  - **ব্যাকএন্ড**:
    - `Root Directory`: `backend`
    - এনভায়রনমেন্ট ভেরিয়েবল সেট করুন: `TOKEN`, `MONGO_URI`, `ADSTERRA_API_TOKEN`।
    - ডিপ্লয়মেন্টের পর `RENDER_URL` নোট করুন (যেমন: `https://pochi-backend.onrender.com`)।
    - `AD_SERVER_URL` এবং `DASHBOARD_URL` আপডেট করুন।
  - **অ্যাড সার্ভার**:
    - `Root Directory`: `adserver`
    - `RENDER_URL` নোট করুন (যেমন: `https://pochi-adserver.onrender.com`)।
    - `backend` এর `AD_SERVER_URL` আপডেট করুন।
  - **ফ্রন্টএন্ড**:
    - `Root Directory`: `frontend`
    - `RENDER_URL` নোট করুন (যেমন: `https://pochi-frontend.onrender.com`)।
    - `backend` এর `DASHBOARD_URL` এবং `frontend/script.js` এর `BACKEND_URL` আপডেট করুন।
- উদাহরণ এনভায়রনমেন্ট ভেরিয়েবল:
  ```bash
  TOKEN=7771736139:AAFhBdAAZF6-rV7YCX08hHK_FAYrHDe8sL0
  MONGO_URI=mongodb+srv://botuser:Xyz12345@tgbot.wh52pfi.mongodb.net/?retryWrites=true&w=majority&appName=tgbot
  ADSTERRA_API_TOKEN=0bc23fcccc35acd927d3e508222416b9
  AD_SERVER_URL=https://pochi-adserver.onrender.com/ad
  DASHBOARD_URL=https://pochi-frontend.onrender.com
  BACKEND_URL=https://pochi-backend.onrender.com
  ```

### ৬. বট টেস্ট করুন
- টেলিগ্রামে `/start` দিয়ে বটে মেসেজ পাঠান।
- CAPTCHA সমাধান করুন এবং ফিচারগুলো টেস্ট করুন: বিজ্ঞাপন, টাস্ক, রেফারেল, রূপান্তর, উত্তোলন।
- ফ্রন্টএন্ড `RENDER_URL`-এ টেলিগ্রাম ইউজার আইডি দিয়ে ড্যাশবোর্ড দেখুন।

### ৭. URL আপডেট করুন
- ডিপ্লয়মেন্টের পর:
  - `backend` এর এনভায়রনমেন্ট ভেরিয়েবলে `AD_SERVER_URL` এবং `DASHBOARD_URL` আপডেট করুন।
  - `frontend/script.js` এ `BACKEND_URL` আপডেট করুন।

## নিরাপত্তা নোট
- `TOKEN`, `MONGO_URI`, এবং `ADSTERRA_API_TOKEN` Render-এ এনভায়রনমেন্ট ভেরিয়েবলে রাখুন।
- টেস্টিংয়ের পর MongoDB পাসওয়ার্ড পরিবর্তন করুন।
- সব Render সার্ভিসে HTTPS ব্যবহার করুন।

## লাভের কৌশল
- **বিজ্ঞাপন আয়**: Adsterra পপআন্ডার বিজ্ঞাপন প্রতি ১০০০ ভিউতে ~$১০-$৫০।
- **পেআউট**: ১০০০ ভিউ = ১০০০ পয়েন্ট = ০.৫ USDT, ~$৯.৫-$৪৯.৫ লাভ।
- **সেটিংস**: টেলিগ্রামে `/set` কমান্ড দিয়ে সমন্বয় করুন।

## অবদান
রিপোজিটরি ফর্ক করুন, ইস্যু জমা দিন, বা পুল রিকোয়েস্ট তৈরি করুন।

## লাইসেন্স
MIT লাইসেন্স