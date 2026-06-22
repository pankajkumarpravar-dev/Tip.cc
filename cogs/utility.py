import discord
from discord.ext import commands
from utils.embeds import EmbedFactory, COLOR_SUCCESS, COLOR_ERROR, COLOR_INFO
from bot import db_manager
import os
import random
from datetime import datetime, timedelta

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rain')
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def rain(self, ctx, coin: str, amount: float, participant_limit: int = 10):
        """Rain crypto on active users"""
        if amount <= 0:
            embed = EmbedFactory.error("Invalid Amount", "Amount must be greater than 0")
            await ctx.send(embed=embed)
            return
        
        try:
            user = await db_manager.get_or_create_user(ctx.author.id, ctx.author.name)
            user_balance = await db_manager.get_user_balance(ctx.author.id, coin.lower())
            
            if user_balance < amount:
                embed = EmbedFactory.error("Insufficient Balance", f"You only have {user_balance:.8f} {coin.upper()}")
                await ctx.send(embed=embed)
                return
            
            # Get active members
            members = [m for m in ctx.guild.members if not m.bot and m.id != ctx.author.id]
            selected = random.sample(members, min(participant_limit, len(members)))
            
            amount_per_user = amount / len(selected)
            
            for member in selected:
                await db_manager.update_user_balance(member.id, coin.lower(), amount_per_user)
                await db_manager.get_or_create_user(member.id, member.name)
            
            await db_manager.update_user_balance(ctx.author.id, coin.lower(), -amount)
            
            rain_id = await db_manager.create_rain(ctx.author.id, coin.upper(), amount, len(selected), ctx.guild.id, ctx.channel.id)
            
            ltc_emoji = os.getenv('LTC_EMOJI', '<:stolen_emoji_blaze:1517930529637400698>')
            emoji = ltc_emoji if coin.lower() == 'ltc' else '◎'
            
            embed = EmbedFactory.success(
                "🌧️ It's Raining!",
                f"{emoji} **{amount:.8f} {coin.upper()}** rained on **{len(selected)}** lucky members!\n\nEach got: `{amount_per_user:.8f} {coin.upper()}`"
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='airdrop')
    @commands.cooldown(1, 1200, commands.BucketType.user)
    async def airdrop(self, ctx, coin: str, amount: float, winners: int = 1, duration: int = 60):
        """Create an airdrop"""
        if amount <= 0 or winners <= 0:
            embed = EmbedFactory.error("Invalid Input", "Amount and winners must be greater than 0")
            await ctx.send(embed=embed)
            return
        
        try:
            user = await db_manager.get_or_create_user(ctx.author.id, ctx.author.name)
            user_balance = await db_manager.get_user_balance(ctx.author.id, coin.lower())
            
            if user_balance < amount:
                embed = EmbedFactory.error("Insufficient Balance", f"You only have {user_balance:.8f} {coin.upper()}")
                await ctx.send(embed=embed)
                return
            
            expires_at = datetime.utcnow() + timedelta(seconds=duration)
            amount_per_winner = amount / winners
            
            airdrop_id = await db_manager.create_airdrop(
                ctx.author.id, coin.upper(), amount_per_winner, amount, winners,
                ctx.guild.id, ctx.channel.id, expires_at
            )
            
            await db_manager.update_user_balance(ctx.author.id, coin.lower(), -amount)
            
            ltc_emoji = os.getenv('LTC_EMOJI', '<:stolen_emoji_blaze:1517930529637400698>')
            emoji = ltc_emoji if coin.lower() == 'ltc' else '◎'
            
            embed = EmbedFactory.create_embed(
                title="🎉 Airdrop Started!",
                description=f"{emoji} **{amount:.8f} {coin.upper()}** airdrop by **{ctx.author.name}**",
                color=COLOR_INFO,
                fields=[
                    {'name': 'Per Winner', 'value': f'`{amount_per_winner:.8f}`', 'inline': True},
                    {'name': 'Winners', 'value': f'`{winners}`', 'inline': True},
                    {'name': 'Duration', 'value': f'`{duration}s`', 'inline': True}
                ]
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='daily')
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """Claim your daily bonus"""
        try:
            user = await db_manager.get_or_create_user(ctx.author.id, ctx.author.name)
            
            # Daily reward: 0.001 LTC
            daily_amount = 0.001
            
            await db_manager.update_user_balance(ctx.author.id, 'ltc', daily_amount)
            await db_manager.claim_daily(ctx.author.id, daily_amount)
            
            ltc_emoji = os.getenv('LTC_EMOJI', '<:stolen_emoji_blaze:1517930529637400698>')
            
            embed = EmbedFactory.success(
                "Daily Bonus Claimed!",
                f"You received {ltc_emoji} **{daily_amount:.8f} LTC**\n\nCome back tomorrow for more!"
            )
            await ctx.send(embed=embed)
        
        except commands.CommandOnCooldown:
            embed = EmbedFactory.error("Already Claimed", "You can only claim your daily bonus once per day!")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='transactions')
    async def transactions(self, ctx, user: discord.User = None):
        """View transaction history"""
        target_user = user or ctx.author
        try:
            txs = await db_manager.get_user_transactions(target_user.id, limit=10)
            
            if not txs:
                embed = EmbedFactory.info("No Transactions", "This user has no transaction history")
                await ctx.send(embed=embed)
                return
            
            description = ""
            for tx in txs:
                tx_id, user_id, tx_type, coin, amount, desc, status, tx_hash, confirmations, created_at = tx
                description += f"`{tx_type.upper()}` {coin} **{amount:.8f}** - {status}\n"
            
            embed = EmbedFactory.create_embed(
                title="📊 Transaction History",
                description=description[:2000],
                color=COLOR_INFO
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx, sort_by: str = "total_tipped"):
        """View top users"""
        try:
            users = await db_manager.get_leaderboard(sort_by=sort_by, limit=10)
            
            if not users:
                embed = EmbedFactory.info("No Users", "No users in leaderboard yet")
                await ctx.send(embed=embed)
                return
            
            description = ""
            for idx, user_data in enumerate(users, 1):
                user_id, username, stat, ltc_bal, sol_bal = user_data
                description += f"{idx}. **{username}** - `{stat:.8f}`\n"
            
            embed = EmbedFactory.create_embed(
                title="🏆 Leaderboard",
                description=description[:2000],
                color=COLOR_INFO,
                footer_text=f"Sorted by {sort_by}"
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
