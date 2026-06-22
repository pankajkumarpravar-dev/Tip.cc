# Tippy - Discord Cryptocurrency Tipping Bot

🚀 **Professional Discord bot for tipping Litecoin (LTC) and Solana (SOL)**

## Features

✅ **Wallet Management**
- Check balances (LTC & SOL)
- View user profiles
- Transaction history

✅ **Tipping System**
- User-to-user tipping
- Lucky tipping (random users)
- Batch tipping with rain
- Airdrops with winners

✅ **Gamification**
- Daily bonuses
- Leaderboards
- Cooldown system
- Progress tracking

✅ **Admin Controls**
- Add/remove balances
- Freeze/unfreeze accounts
- Maintenance mode
- Admin logs

✅ **Professional Design**
- Blue embed theme (#3498DB)
- Fast async responses
- Error handling
- Clean interface

## Installation

See `SETUP.md` for complete installation and deployment instructions.

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/pankajkumarpravar-dev/Tip.cc.git
cd Tip.cc

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env with your Discord token

# 4. Run bot
python bot.py
```

## Commands

### 💰 Wallet
```
$balance              - Check your balance
$profile [@user]      - View profile
$deposit              - Generate deposit address
$withdraw             - Withdraw crypto
```

### 💸 Tipping
```
$tip @user coin amount [message]    - Send tip
$luckytip coin amount                - Tip random user
$rain coin amount [limit]            - Rain on users
$airdrop coin amount [winners] [sec] - Create airdrop
```

### 📊 Stats
```
$transactions [@user]  - View transactions
$leaderboard [sort]    - View top users
$daily                 - Claim daily bonus
```

### 👑 Admin
```
$addbalance @user coin amount      - Add balance
$removebalance @user coin amount   - Remove balance
$freeze @user                      - Freeze account
$unfreeze @user                    - Unfreeze account
$maintenance                       - Toggle maintenance
```

## Technology Stack

- **Language**: Python 3.8+
- **Framework**: discord.py 2.3.2
- **Database**: SQLite (development) / PostgreSQL (production)
- **Async**: aiohttp, aiosqlite
- **Blockchain**: Litecoin, Solana

## Project Structure

```
Tippy/
├── bot.py                 # Main bot entry
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── SETUP.md              # Setup guide
├── database/
│   └── db_manager.py     # Database operations
├── cogs/
│   ├── help.py          # Help commands
│   ├── wallet.py        # Balance & profile
│   ├── tip.py           # Tipping commands
│   ├── utility.py       # Rain, airdrop, daily
│   └── admin.py         # Admin commands
├── utils/
│   ├── embeds.py        # Embed factory
│   └── validators.py    # Input validation
└── views/               # Interactive components
```

## Configuration

Edit `.env` file:

```env
DISCORD_TOKEN=your_token_here
LTC_EMOJI=<:custom_emoji:123456>
ADMIN_IDS=your_discord_id
TIP_COOLDOWN=5
RAIN_COOLDOWN=600
AIRDROP_COOLDOWN=1200
```

## Database

Automatic SQLite database creation with tables:
- `users` - User profiles & balances
- `wallets` - Deposit addresses
- `transactions` - Transaction history
- `tips` - Tip records
- `airdrops` - Airdrop records
- `rains` - Rain event records
- `cooldowns` - Command cooldowns
- `daily_claims` - Daily reward claims

## Deployment

Supported platforms:
- Railway
- Heroku
- VPS (Debian/Ubuntu)
- Docker containers

See `SETUP.md` for deployment instructions.

## Security

⚠️ **Important**:
- Never commit `.env` file
- Use strong database passwords
- Enable 2FA on Discord app
- Keep bot token secret
- Regular database backups

## License

MIT License - feel free to fork and modify

## Support

For issues or questions, open a GitHub issue or contact the maintainer.

---

**Made with ❤️ for the crypto community**
