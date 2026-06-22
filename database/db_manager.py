import sqlite3
import aiosqlite
import os
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger('Tippy')

class DatabaseManager:
    def __init__(self, db_path: str = "tippy.db"):
        self.db_path = db_path
        self.connection = None

    async def initialize(self):
        """Initialize database and create tables"""
        try:
            self.connection = await aiosqlite.connect(self.db_path)
            await self.connection.execute("PRAGMA foreign_keys = ON")
            await self.create_tables()
            logger.info("✅ Database initialized successfully")
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise

    async def create_tables(self):
        """Create all required tables"""
        tables = [
            """CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                ltc_balance REAL DEFAULT 0,
                sol_balance REAL DEFAULT 0,
                total_tipped REAL DEFAULT 0,
                total_received REAL DEFAULT 0,
                total_deposited REAL DEFAULT 0,
                total_withdrawn REAL DEFAULT 0,
                daily_claimed TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_frozen INTEGER DEFAULT 0
            )""",
            """CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                ltc_address TEXT UNIQUE,
                sol_address TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )""",
            """CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                coin TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'completed',
                tx_hash TEXT,
                confirmations INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )""",
            """CREATE TABLE IF NOT EXISTS tips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                coin TEXT NOT NULL,
                amount REAL NOT NULL,
                message TEXT,
                guild_id INTEGER,
                channel_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(user_id),
                FOREIGN KEY (receiver_id) REFERENCES users(user_id)
            )""",
            """CREATE TABLE IF NOT EXISTS airdrops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id INTEGER NOT NULL,
                coin TEXT NOT NULL,
                amount_per_winner REAL NOT NULL,
                total_amount REAL NOT NULL,
                winners_count INTEGER DEFAULT 1,
                participants TEXT DEFAULT '[]',
                winners TEXT DEFAULT '[]',
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                message_id INTEGER,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users(user_id)
            )""",
            """CREATE TABLE IF NOT EXISTS rains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id INTEGER NOT NULL,
                coin TEXT NOT NULL,
                amount_total REAL NOT NULL,
                participant_count INTEGER NOT NULL,
                participants TEXT DEFAULT '[]',
                recipients TEXT DEFAULT '[]',
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                message_id INTEGER,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users(user_id)
            )""",
            """CREATE TABLE IF NOT EXISTS settings (
                guild_id INTEGER PRIMARY KEY,
                log_channel_id INTEGER,
                withdraw_channel_id INTEGER,
                prefix TEXT DEFAULT '$',
                custom_welcome TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS cooldowns (
                user_id INTEGER NOT NULL,
                command TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                PRIMARY KEY (user_id, command),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )""",
            """CREATE TABLE IF NOT EXISTS daily_claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )"""
        ]
        
        for table in tables:
            await self.connection.execute(table)
        await self.connection.commit()

    async def get_or_create_user(self, user_id: int, username: str):
        """Get or create a user"""
        async with self.connection.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            user = await cursor.fetchone()
        
        if not user:
            await self.connection.execute(
                "INSERT INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username)
            )
            await self.connection.commit()
            return await self.get_user(user_id)
        return user

    async def get_user(self, user_id: int):
        """Get user by ID"""
        async with self.connection.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchone()

    async def update_user_balance(self, user_id: int, coin: str, amount: float):
        """Update user balance"""
        column = f"{coin.lower()}_balance"
        await self.connection.execute(
            f"UPDATE users SET {column} = {column} + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await self.connection.commit()

    async def get_user_balance(self, user_id: int, coin: str):
        """Get user balance for a specific coin"""
        column = f"{coin.lower()}_balance"
        async with self.connection.execute(
            f"SELECT {column} FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

    async def freeze_user(self, user_id: int):
        """Freeze user account"""
        await self.connection.execute(
            "UPDATE users SET is_frozen = 1 WHERE user_id = ?", (user_id,)
        )
        await self.connection.commit()

    async def unfreeze_user(self, user_id: int):
        """Unfreeze user account"""
        await self.connection.execute(
            "UPDATE users SET is_frozen = 0 WHERE user_id = ?", (user_id,)
        )
        await self.connection.commit()

    async def is_user_frozen(self, user_id: int):
        """Check if user is frozen"""
        async with self.connection.execute(
            "SELECT is_frozen FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else False

    async def create_wallet(self, user_id: int, ltc_address: str = None, sol_address: str = None):
        """Create or update wallet for user"""
        async with self.connection.execute(
            "SELECT id FROM wallets WHERE user_id = ?", (user_id,)
        ) as cursor:
            wallet = await cursor.fetchone()
        
        if wallet:
            if ltc_address:
                await self.connection.execute(
                    "UPDATE wallets SET ltc_address = ? WHERE user_id = ?",
                    (ltc_address, user_id)
                )
            if sol_address:
                await self.connection.execute(
                    "UPDATE wallets SET sol_address = ? WHERE user_id = ?",
                    (sol_address, user_id)
                )
        else:
            await self.connection.execute(
                "INSERT INTO wallets (user_id, ltc_address, sol_address) VALUES (?, ?, ?)",
                (user_id, ltc_address, sol_address)
            )
        await self.connection.commit()

    async def get_wallet(self, user_id: int):
        """Get user wallet"""
        async with self.connection.execute(
            "SELECT * FROM wallets WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchone()

    async def get_wallet_by_address(self, address: str, coin: str):
        """Get wallet by address"""
        column = f"{coin.lower()}_address"
        async with self.connection.execute(
            f"SELECT user_id FROM wallets WHERE {column} = ?", (address,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

    async def add_transaction(self, user_id: int, tx_type: str, coin: str, amount: float, description: str = None, tx_hash: str = None, status: str = "completed"):
        """Add transaction record"""
        await self.connection.execute(
            "INSERT INTO transactions (user_id, type, coin, amount, description, tx_hash, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, tx_type, coin, amount, description, tx_hash, status)
        )
        await self.connection.commit()

    async def get_user_transactions(self, user_id: int, limit: int = 10):
        """Get user transactions"""
        async with self.connection.execute(
            "SELECT * FROM transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        ) as cursor:
            return await cursor.fetchall()

    async def add_tip(self, sender_id: int, receiver_id: int, coin: str, amount: float, message: str = None, guild_id: int = None, channel_id: int = None):
        """Record a tip"""
        await self.connection.execute(
            "INSERT INTO tips (sender_id, receiver_id, coin, amount, message, guild_id, channel_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (sender_id, receiver_id, coin, amount, message, guild_id, channel_id)
        )
        await self.connection.execute(
            "UPDATE users SET total_tipped = total_tipped + ? WHERE user_id = ?",
            (amount, sender_id)
        )
        await self.connection.execute(
            "UPDATE users SET total_received = total_received + ? WHERE user_id = ?",
            (amount, receiver_id)
        )
        await self.connection.commit()

    async def get_user_tips_sent(self, user_id: int, limit: int = 10):
        """Get tips sent by user"""
        async with self.connection.execute(
            "SELECT * FROM tips WHERE sender_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        ) as cursor:
            return await cursor.fetchall()

    async def get_user_tips_received(self, user_id: int, limit: int = 10):
        """Get tips received by user"""
        async with self.connection.execute(
            "SELECT * FROM tips WHERE receiver_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        ) as cursor:
            return await cursor.fetchall()

    async def create_airdrop(self, creator_id: int, coin: str, amount_per_winner: float, total_amount: float, winners_count: int, guild_id: int, channel_id: int, expires_at: datetime):
        """Create airdrop"""
        async with self.connection.execute(
            "INSERT INTO airdrops (creator_id, coin, amount_per_winner, total_amount, winners_count, guild_id, channel_id, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ",
            (creator_id, coin, amount_per_winner, total_amount, winners_count, guild_id, channel_id, expires_at)
        ) as cursor:
            pass
        await self.connection.commit()
        async with self.connection.execute(
            "SELECT last_insert_rowid()"
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

    async def get_airdrop(self, airdrop_id: int):
        """Get airdrop by ID"""
        async with self.connection.execute(
            "SELECT * FROM airdrops WHERE id = ?", (airdrop_id,)
        ) as cursor:
            return await cursor.fetchone()

    async def update_airdrop_participants(self, airdrop_id: int, participants: list):
        """Update airdrop participants"""
        await self.connection.execute(
            "UPDATE airdrops SET participants = ? WHERE id = ?",
            (json.dumps(participants), airdrop_id)
        )
        await self.connection.commit()

    async def check_expired_airdrops(self):
        """Check and process expired airdrops"""
        async with self.connection.execute(
            "SELECT id FROM airdrops WHERE status = 'active' AND expires_at < CURRENT_TIMESTAMP"
        ) as cursor:
            airdrops = await cursor.fetchall()
        for (airdrop_id,) in airdrops:
            await self.connection.execute(
                "UPDATE airdrops SET status = 'expired' WHERE id = ?", (airdrop_id,)
            )
        await self.connection.commit()

    async def create_rain(self, creator_id: int, coin: str, amount_total: float, participant_count: int, guild_id: int, channel_id: int):
        """Create rain"""
        async with self.connection.execute(
            "INSERT INTO rains (creator_id, coin, amount_total, participant_count, guild_id, channel_id) VALUES (?, ?, ?, ?, ?, ?)",
            (creator_id, coin, amount_total, participant_count, guild_id, channel_id)
        ) as cursor:
            pass
        await self.connection.commit()
        async with self.connection.execute(
            "SELECT last_insert_rowid()"
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

    async def get_rain(self, rain_id: int):
        """Get rain by ID"""
        async with self.connection.execute(
            "SELECT * FROM rains WHERE id = ?", (rain_id,)
        ) as cursor:
            return await cursor.fetchone()

    async def get_leaderboard(self, coin: str = "ltc", limit: int = 10, sort_by: str = "total_tipped"):
        """Get leaderboard"""
        valid_sorts = ["total_tipped", "total_received", "ltc_balance", "sol_balance"]
        sort_column = sort_by if sort_by in valid_sorts else "total_tipped"
        
        query = f"SELECT user_id, username, {sort_column}, ltc_balance, sol_balance FROM users WHERE is_frozen = 0 ORDER BY {sort_column} DESC LIMIT ?"
        async with self.connection.execute(query, (limit,)) as cursor:
            return await cursor.fetchall()

    async def claim_daily(self, user_id: int, amount: float):
        """Record daily claim"""
        now = datetime.utcnow()
        await self.connection.execute(
            "INSERT INTO daily_claims (user_id, amount) VALUES (?, ?)",
            (user_id, amount)
        )
        await self.connection.execute(
            "UPDATE users SET daily_claimed = ?, total_received = total_received + ? WHERE user_id = ?",
            (now, amount, user_id)
        )
        await self.connection.commit()

    async def get_last_daily_claim(self, user_id: int):
        """Get last daily claim"""
        async with self.connection.execute(
            "SELECT claimed_at FROM daily_claims WHERE user_id = ? ORDER BY claimed_at DESC LIMIT 1",
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

    async def set_cooldown(self, user_id: int, command: str, seconds: int):
        """Set cooldown for user command"""
        expires_at = datetime.utcnow() + timedelta(seconds=seconds)
        await self.connection.execute(
            "INSERT OR REPLACE INTO cooldowns (user_id, command, expires_at) VALUES (?, ?, ?)",
            (user_id, command, expires_at)
        )
        await self.connection.commit()

    async def get_cooldown(self, user_id: int, command: str):
        """Get remaining cooldown"""
        async with self.connection.execute(
            "SELECT expires_at FROM cooldowns WHERE user_id = ? AND command = ?",
            (user_id, command)
        ) as cursor:
            result = await cursor.fetchone()
        if result:
            expires = datetime.fromisoformat(result[0])
            remaining = (expires - datetime.utcnow()).total_seconds()
            if remaining > 0:
                return remaining
            else:
                await self.connection.execute(
                    "DELETE FROM cooldowns WHERE user_id = ? AND command = ?",
                    (user_id, command)
                )
                await self.connection.commit()
        return 0
