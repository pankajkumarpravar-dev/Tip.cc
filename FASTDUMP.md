# 🚀 TIPPY BOT - PRE-LAUNCH CHECKLIST

## ⚡ QUICK START (5 STEPS)

### Step 1: Create Discord Bot
1. Go to https://discord.com/developers/applications
2. Click "New Application" → Name it "Tippy"
3. Go to "Bot" section → Click "Add Bot"
4. Copy the **TOKEN** (keep it secret!)
5. Enable these Intents:
   - ✅ Message Content Intent
   - ✅ Server Members Intent

### Step 2: Get Bot Invite Link
1. Go to OAuth2 → URL Generator
2. Select scopes: `bot`
3. Select permissions:
   - Send Messages
   - Embed Links
   - Read Message History
4. Copy the URL and invite bot to your test server

### Step 3: Setup Environment File
```bash
cp .env.example .env
```

Edit `.env`:
```
DISCORD_TOKEN=paste_your_token_here
LTC_EMOJI=<:stolen_emoji_blaze:1517930529637400698>
ADMIN_IDS=your_discord_id_here
```

Get your Discord ID:
- Enable Developer Mode (Discord Settings → Advanced → Developer Mode)
- Right-click yourself → Copy User ID
- Paste in `ADMIN_IDS`

### Step 4: Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Start bot
python bot.py
```

You should see:
```
✅ Tippy is online as Tippy#0000
🔗 Connected to X servers
✅ Loaded cog: help.py
✅ Loaded cog: wallet.py
✅ Loaded cog: tip.py
✅ Loaded cog: utility.py
✅ Loaded cog: admin.py
```

### Step 5: Test Commands
In Discord:
```
$help                         # See all commands
$balance                      # Check balance
$addbalance @yourself ltc 1   # Add test balance (admin)
$tip @user ltc 0.1 "message" # Send tip
$daily                        # Claim bonus
```

---

## 📋 FULL PRE-LAUNCH CHECKLIST

### ✅ Discord Setup
- [ ] Create application at Discord Developer Portal
- [ ] Add bot to application
- [ ] Copy bot token
- [ ] Enable Message Content Intent
- [ ] Enable Server Members Intent
- [ ] Create OAuth2 URL with bot scope
- [ ] Invite bot to test server
- [ ] Bot appears online in Discord

### ✅ Environment Configuration
- [ ] Copy `.env.example` → `.env`
- [ ] Add `DISCORD_TOKEN`
- [ ] Add your Discord ID to `ADMIN_IDS`
- [ ] Add custom LTC emoji (or use default)
- [ ] Test file is not committed (check .gitignore)

### ✅ Local Setup
- [ ] Python 3.8+ installed
- [ ] Created virtual environment
- [ ] Installed all requirements (`pip install -r requirements.txt`)
- [ ] Database created (`tippy.db` appears after first run)

### ✅ Bot Testing
- [ ] Bot starts without errors
- [ ] All 5 cogs load successfully
- [ ] `$help` command works
- [ ] `$balance` command works
- [ ] Can add test balance with `$addbalance`
- [ ] Can send tips with `$tip`
- [ ] Can claim daily with `$daily`
- [ ] Error handling works (try invalid command)

### ✅ Database
- [ ] `tippy.db` file created
- [ ] All tables created (run `sqlite3 tippy.db ".tables"`)
- [ ] Can add users
- [ ] Can add transactions
- [ ] No database errors in logs

### ✅ Cooldowns
- [ ] Tip cooldown works (5 second wait)
- [ ] Daily cooldown works (24 hour wait)
- [ ] Rain cooldown works (10 minute wait)
- [ ] Airdrop cooldown works (20 minute wait)

### ✅ Error Handling
- [ ] Invalid command shows error
- [ ] Missing arguments shows error
- [ ] Insufficient balance shows error
- [ ] Cannot tip yourself
- [ ] Cannot tip bots
- [ ] Negative amounts rejected

---

## 🔑 REQUIRED VARIABLES EXPLAINED

### Must Have
```
DISCORD_TOKEN          → Bot token from Developer Portal
ADMIN_IDS              → Your Discord ID (comma-separated for multiple)
```

### Nice to Have
```
LTC_EMOJI              → Custom emoji for Litecoin (default works fine)
SOL_EMOJI              → Custom emoji for Solana (default: ⊙)
LOG_CHANNEL_ID         → Channel ID for logging (optional)
WITHDRAW_CHANNEL_ID    → Channel ID for withdrawals (optional)
```

### Optional Cooldowns (defaults fine)
```
TIP_COOLDOWN=5                  # Seconds between tips
WITHDRAW_COOLDOWN=300           # Seconds (5 minutes)
RAIN_COOLDOWN=600               # Seconds (10 minutes)
AIRDROP_COOLDOWN=1200           # Seconds (20 minutes)
```

---

## 🧪 TESTING COMMANDS

### User Commands (No Admin Needed)
```
$help                           # List all commands
$balance                        # Your balance
$profile                        # Your profile
$profile @user                  # View someone's profile
$transactions                   # Your transactions
$transactions @user             # View someone's transactions
$leaderboard                    # Top users by tipped amount
$leaderboard total_received     # Top users by received
$daily                          # Claim daily bonus (once per day)
```

### Tipping Commands (Need Balance)
```
$tip @user ltc 0.001                    # Send tip
$tip @user ltc 0.001 "nice shot!"      # Tip with message
$luckytip ltc 0.001                    # Tip random user
$rain ltc 0.01                         # Rain 0.01 LTC on 10 random users
$rain ltc 0.01 5                       # Rain on 5 users
$airdrop ltc 0.01                      # 1 winner gets 0.01 LTC
$airdrop ltc 0.1 5                     # 5 winners split 0.1 LTC
$airdrop ltc 0.1 5 120                 # Airdrop lasts 2 minutes
```

### Admin Commands
```
$addbalance @user ltc 1.0               # Add 1 LTC to user
$addbalance @user sol 5.0               # Add 5 SOL to user
$removebalance @user ltc 0.5            # Remove 0.5 LTC
$freeze @user                           # Freeze account
$unfreeze @user                         # Unfreeze account
$maintenance                            # Toggle maintenance mode
```

---

## 🐛 TROUBLESHOOTING

### "DISCORD_TOKEN not found"
- [ ] Check `.env` file exists (not `.env.example`)
- [ ] Check token is pasted correctly
- [ ] Check no extra spaces: `DISCORD_TOKEN=token` (not `DISCORD_TOKEN = token`)
- [ ] Restart bot after editing `.env`

### "Bot won't respond to commands"
- [ ] Bot is online in Discord server
- [ ] Bot role is above user roles (for moderation commands)
- [ ] Bot has "Send Messages" permission in channel
- [ ] Try `$help` first
- [ ] Check bot logs for errors

### "Database error"
- [ ] Delete `tippy.db` and restart (will create fresh)
- [ ] Check folder has write permissions
- [ ] Try: `sqlite3 tippy.db "SELECT 1"` (should return 1)

### "Commands on cooldown"
- This is normal! Each command has cooldown:
  - Tip: 5 seconds
  - Daily: 24 hours
  - Rain: 10 minutes
  - Airdrop: 20 minutes

### "AttributeError: 'NoneType'"
- [ ] Make sure `.env` is properly loaded
- [ ] Restart bot
- [ ] Check `.env` syntax

---

## 📦 PROJECT FILES

```
✅ bot.py                   Main bot file (START HERE)
✅ requirements.txt         Python dependencies
✅ .env.example            Environment template (COPY TO .env)
✅ SETUP.md                Detailed setup guide
✅ FASTDUMP.md             This file!
✅ README.md               Project overview
✅ Dockerfile              Docker deployment
✅ Procfile                Heroku deployment

📁 database/
  ✅ db_manager.py         Database operations
  ✅ __init__.py

📁 cogs/
  ✅ help.py               Help command
  ✅ wallet.py             Balance & profile
  ✅ tip.py                Tipping system
  ✅ utility.py            Rain, airdrop, daily
  ✅ admin.py              Admin commands
  ✅ __init__.py

📁 utils/
  ✅ embeds.py             Professional embed styling
  ✅ __init__.py

📁 views/
  ✅ __init__.py
```

---

## 💾 DATABASE TABLES

Automatic creation on first run:

```
📊 users              → User profiles, balances, stats
🏷️  wallets           → Deposit addresses (LTC, SOL)
📝 transactions       → Transaction history
💰 tips               → Tip records
🎉 airdrops          → Airdrop records
🌧️  rains            → Rain event records
⏱️  cooldowns        → Command cooldown tracking
📅 daily_claims      → Daily reward claims
⚙️  settings         → Guild settings
```

View data:
```bash
sqlite3 tippy.db
> .tables
> SELECT * FROM users;
> SELECT * FROM transactions;
```

---

## 🚀 DEPLOYMENT OPTIONS

### Option 1: Railway (Recommended)
```bash
# Deploy automatically from GitHub
1. Push to GitHub
2. Connect repo to Railway
3. Add DISCORD_TOKEN as environment variable
4. Deploy!
```

### Option 2: Heroku
```bash
# Requires Procfile (included)
heroku create tippy-bot
heroku config:set DISCORD_TOKEN=your_token
git push heroku main
```

### Option 3: Docker
```bash
docker build -t tippy-bot .
docker run -e DISCORD_TOKEN=your_token tippy-bot
```

### Option 4: VPS (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install python3.11 git
git clone repo
cd Tip.cc
pip install -r requirements.txt
nohup python bot.py > bot.log 2>&1 &
```

---

## ⚠️ SECURITY CHECKLIST

- [ ] `.env` is in `.gitignore` (never commit!)
- [ ] Token is secret (never share in screenshots)
- [ ] Admin IDs are correct
- [ ] Database has permissions restricted
- [ ] Bot has minimal required permissions
- [ ] No debug logging in production
- [ ] Validate user input (already done)
- [ ] Error messages don't expose internals

---

## 📊 PERFORMANCE TIPS

- Bot uses **async/await** for speed ✅
- Database operations are **async** ✅
- Cooldowns prevent spam ✅
- Efficient SQL queries ✅
- No blocking operations ✅

---

## 🎯 QUICK REFERENCE

```bash
# Copy template
cp .env.example .env

# Edit with your settings
nano .env  # or use your editor

# Install
pip install -r requirements.txt

# Run
python bot.py

# Check database
sqlite3 tippy.db ".tables"

# View logs
cat bot.log
```

---

## ✨ YOU'RE READY!

Once you complete the checklist above, your Tippy bot is production-ready! 🎉

**Need help?** Check `SETUP.md` for detailed info or open an issue on GitHub.

**Good luck! 🚀**
