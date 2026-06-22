# Setup Instructions for Tippy Bot

## 📋 Pre-Launch Checklist

Before launching your Tippy cryptocurrency tipping bot, you need to complete these steps:

### 1. **Create Discord Application & Bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and name it "Tippy"
   - Go to "Bot" section and click "Add Bot"
   - Copy the token
   - Enable these Intents:
     - ✅ Message Content Intent
     - ✅ Server Members Intent
     - ✅ Guilds Intent
   - Save the token securely

### 2. **Get OAuth2 URL for Invite Link**
   - Go to OAuth2 → URL Generator
   - Select scopes: `bot`
   - Select permissions:
     - Send Messages
     - Embed Links
     - Read Message History
     - Manage Messages
     - Add Reactions
   - Copy the generated URL and use it to invite the bot to your test server

### 3. **Setup Environment Variables (.env)**
   ```bash
   # Copy .env.example to .env
   cp .env.example .env
   
   # Edit .env and fill in:
   DISCORD_TOKEN=your_bot_token_here
   
   # Optional (for blockchain integration):
   LITECOIN_API_KEY=get_from_blockchair.com
   SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
   SOLANA_API_KEY=get_from_alchemy_or_quicknode
   
   # Admin settings (your Discord ID):
   ADMIN_IDS=your_discord_id
   
   # Bot settings:
   LTC_EMOJI=<:stolen_emoji_blaze:1517930529637400698>
   SOL_EMOJI=◎
   
   # Cooldowns (in seconds) - Optional, defaults provided:
   TIP_COOLDOWN=5
   WITHDRAW_COOLDOWN=300
   RAIN_COOLDOWN=600
   AIRDROP_COOLDOWN=1200
   ```

### 4. **Install Dependencies**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install requirements
   pip install -r requirements.txt
   ```

### 5. **API Keys to Get (Optional but Recommended)**

   **For Litecoin deposit detection:**
   - Sign up at [Blockchair](https://blockchair.com/api)
   - Get API key for LTC blockchain monitoring
   - Add to `LITECOIN_API_KEY` in .env

   **For Solana integration:**
   - Sign up at [Alchemy](https://www.alchemy.com/) or [QuickNode](https://www.quicknode.com/)
   - Get a Solana RPC endpoint
   - Add to `SOLANA_RPC_URL` in .env

### 6. **Database Setup**
   - The bot automatically creates `tippy.db` (SQLite) on first run
   - For PostgreSQL (production), update `DATABASE_URL` in .env:
     ```
     DATABASE_URL=postgresql://user:password@localhost:5432/tippy
     ```

### 7. **Start the Bot**
   ```bash
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

### 8. **Test Commands in Discord**
   ```
   $help                    # View all commands
   $balance                 # Check balance
   $profile                 # View profile
   $tip @user ltc 0.001     # Send tip
   $rain ltc 0.01           # Rain crypto
   $daily                   # Claim daily bonus
   ```

### 9. **Admin Setup (Optional)**
   - Get your Discord ID (enable Developer Mode in Discord → right-click yourself → Copy User ID)
   - Add your ID to `ADMIN_IDS` in .env
   - Use admin commands:
     ```
     $addbalance @user ltc 0.1     # Add test balance
     $freeze @user                  # Freeze account
     $unfreeze @user                # Unfreeze account
     ```

### 10. **Customize Settings**
   - Edit LTC emoji: Change `LTC_EMOJI` to your custom emoji
   - Adjust cooldowns in .env if needed
   - Modify daily reward in `cogs/utility.py` line 85 if desired

---

## 🚀 Production Deployment

When ready for production:

1. **Use PostgreSQL instead of SQLite**
   - Better for multiple bot instances
   - Update `DATABASE_URL` in .env

2. **Deploy on hosting service:**
   - [Heroku](https://www.heroku.com/) (free tier available)
   - [Railway](https://railway.app/)
   - [Replit](https://replit.com/)
   - Your own VPS

3. **Setup cryptocurrency node monitoring:**
   - Connect to Litecoin/Solana nodes
   - Implement deposit detection
   - Setup withdrawal processing

4. **Security:**
   - Use environment variables for all secrets
   - Enable 2FA on Discord app
   - Use strong database passwords
   - Regular backups of database

---

## 📊 Database Schema

The bot creates these tables automatically:
- **users** - User profiles and balances
- **wallets** - Deposit addresses
- **transactions** - Transaction history
- **tips** - Tip records
- **airdrops** - Airdrop records
- **rains** - Rain event records
- **settings** - Guild-specific settings
- **cooldowns** - Command cooldowns
- **daily_claims** - Daily bonus claims

---

## 🆘 Troubleshooting

**Bot won't start:**
- Check `DISCORD_TOKEN` is correct
- Ensure all requirements installed: `pip install -r requirements.txt`
- Check Python version (3.8+)

**Commands not working:**
- Ensure bot has message permissions in the channel
- Check bot role is high enough in role hierarchy
- Try `$help` to see available commands

**Database errors:**
- Delete `tippy.db` and restart (will create fresh)
- Check database write permissions
- For PostgreSQL, verify connection string

**Blockchain integration issues:**
- Verify API keys are correct
- Check RPC URL is accessible
- Ensure rate limits aren't exceeded

---

## 📚 Features Included

✅ User wallet management (LTC & SOL)
✅ Balance checking and profiles
✅ User-to-user tipping
✅ Rain distribution
✅ Airdrop system
✅ Lucky tipping
✅ Daily bonuses
✅ Transaction history
✅ Leaderboard
✅ Admin controls
✅ Professional blue embeds
✅ Error handling
✅ Cooldown system
✅ Fully async

---

## 📝 Commands Reference

```
💰 Wallet:
  $balance          - Check your balance
  $profile [user]   - View profile

💸 Tipping:
  $tip @user coin amount [message]     - Send tip
  $luckytip coin amount                - Tip random user
  $rain coin amount [limit]            - Rain crypto
  $airdrop coin amount [winners] [sec] - Create airdrop

📊 Stats:
  $transactions [user] - View transactions
  $leaderboard [sort]  - View leaderboard
  $daily              - Claim daily bonus

👑 Admin:
  $addbalance @user coin amount    - Add balance
  $removebalance @user coin amount - Remove balance
  $freeze @user                    - Freeze account
  $unfreeze @user                  - Unfreeze account
  $maintenance                     - Toggle maintenance mode

❓ Help:
  $help [command] - Show help
```

---

**Good luck with your Tippy bot! 🎉**
