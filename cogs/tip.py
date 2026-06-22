import discord
from discord.ext import commands
from utils.embeds import EmbedFactory, COLOR_SUCCESS, COLOR_ERROR
from bot import db_manager
import os

class TipCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tip')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tip(self, ctx, user: discord.User, coin: str, amount: float, *, message: str = None):
        """Tip someone crypto"""
        if user.id == ctx.author.id:
            embed = EmbedFactory.error("Invalid", "You cannot tip yourself!")
            await ctx.send(embed=embed)
            return
        
        if user.bot:
            embed = EmbedFactory.error("Invalid", "You cannot tip bots!")
            await ctx.send(embed=embed)
            return
        
        if amount <= 0:
            embed = EmbedFactory.error("Invalid Amount", "Amount must be greater than 0")
            await ctx.send(embed=embed)
            return
        
        try:
            sender = await db_manager.get_or_create_user(ctx.author.id, ctx.author.name)
            receiver = await db_manager.get_or_create_user(user.id, user.name)
            
            sender_balance = await db_manager.get_user_balance(ctx.author.id, coin.lower())
            
            if sender_balance < amount:
                embed = EmbedFactory.error("Insufficient Balance", f"You only have {sender_balance:.8f} {coin.upper()}")
                await ctx.send(embed=embed)
                return
            
            await db_manager.update_user_balance(ctx.author.id, coin.lower(), -amount)
            await db_manager.update_user_balance(user.id, coin.lower(), amount)
            await db_manager.add_tip(ctx.author.id, user.id, coin.upper(), amount, message, ctx.guild.id, ctx.channel.id)
            
            ltc_emoji = os.getenv('LTC_EMOJI', '<:stolen_emoji_blaze:1517930529637400698>')
            emoji = ltc_emoji if coin.lower() == 'ltc' else '◎'
            
            embed = EmbedFactory.success(
                "Tip Sent!",
                f"**{ctx.author.name}** tipped {emoji} **{amount:.8f} {coin.upper()}** to **{user.name}**\n\n{message if message else ''}",
                footer_text=f"Tipped by {ctx.author.name}"
            )
            await ctx.send(embed=embed)
            
            try:
                dm_embed = EmbedFactory.success(
                    "You received a tip!",
                    f"**{ctx.author.name}** tipped you {emoji} **{amount:.8f} {coin.upper()}**\n\n{message if message else ''}"
                )
                await user.send(embed=dm_embed)
            except:
                pass
        
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='luckytip')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def luckytip(self, ctx, coin: str, amount: float):
        """Tip a random user in the server"""
        if amount <= 0:
            embed = EmbedFactory.error("Invalid Amount", "Amount must be greater than 0")
            await ctx.send(embed=embed)
            return
        
        members = [m for m in ctx.guild.members if not m.bot and m.id != ctx.author.id]
        if not members:
            embed = EmbedFactory.error("No Members", "No eligible members to tip")
            await ctx.send(embed=embed)
            return
        
        import random
        lucky_user = random.choice(members)
        
        try:
            sender = await db_manager.get_or_create_user(ctx.author.id, ctx.author.name)
            receiver = await db_manager.get_or_create_user(lucky_user.id, lucky_user.name)
            
            sender_balance = await db_manager.get_user_balance(ctx.author.id, coin.lower())
            
            if sender_balance < amount:
                embed = EmbedFactory.error("Insufficient Balance", f"You only have {sender_balance:.8f} {coin.upper()}")
                await ctx.send(embed=embed)
                return
            
            await db_manager.update_user_balance(ctx.author.id, coin.lower(), -amount)
            await db_manager.update_user_balance(lucky_user.id, coin.lower(), amount)
            await db_manager.add_tip(ctx.author.id, lucky_user.id, coin.upper(), amount, "Lucky Tip!", ctx.guild.id, ctx.channel.id)
            
            ltc_emoji = os.getenv('LTC_EMOJI', '<:stolen_emoji_blaze:1517930529637400698>')
            emoji = ltc_emoji if coin.lower() == 'ltc' else '◎'
            
            embed = EmbedFactory.success(
                "🍀 Lucky Tip Sent!",
                f"**{lucky_user.mention}** is lucky! They received {emoji} **{amount:.8f} {coin.upper()}** from **{ctx.author.name}**!"
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TipCog(bot))
