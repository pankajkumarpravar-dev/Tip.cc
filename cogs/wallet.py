import discord
from discord.ext import commands
from utils.embeds import EmbedFactory, COLOR_SUCCESS, COLOR_ERROR, COLOR_INFO
from bot import db_manager
import os

class BalanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='balance')
    async def balance(self, ctx):
        """Check your crypto balance"""
        try:
            user = await db_manager.get_or_create_user(ctx.author.id, ctx.author.name)
            ltc_balance = await db_manager.get_user_balance(ctx.author.id, 'ltc')
            sol_balance = await db_manager.get_user_balance(ctx.author.id, 'sol')
            
            ltc_emoji = os.getenv('LTC_EMOJI', '<:stolen_emoji_blaze:1517930529637400698>')
            sol_emoji = os.getenv('SOL_EMOJI', '◎')
            
            embed = EmbedFactory.create_embed(
                title="💰 Your Balance",
                description=f"**{ctx.author.name}'s Wallet**",
                color=COLOR_INFO,
                fields=[
                    {'name': f'Litecoin (LTC) {ltc_emoji}', 'value': f'```{ltc_balance:.8f} LTC```', 'inline': True},
                    {'name': f'Solana (SOL) {sol_emoji}', 'value': f'```{sol_balance:.8f} SOL```', 'inline': True}
                ]
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='profile')
    async def profile(self, ctx, user: discord.User = None):
        """View user profile"""
        target_user = user or ctx.author
        try:
            user_data = await db_manager.get_or_create_user(target_user.id, target_user.name)
            if not user_data:
                embed = EmbedFactory.error("User not found")
                await ctx.send(embed=embed)
                return
            
            user_id, username, ltc_bal, sol_bal, total_tipped, total_received, total_deposited, total_withdrawn, daily, created_at, is_frozen = user_data
            
            ltc_emoji = os.getenv('LTC_EMOJI', '<:stolen_emoji_blaze:1517930529637400698>')
            
            embed = EmbedFactory.create_embed(
                title="👤 User Profile",
                description=f"**{username}**",
                color=COLOR_INFO,
                fields=[
                    {'name': 'User ID', 'value': f'`{user_id}`', 'inline': True},
                    {'name': 'Status', 'value': '🔒 Frozen' if is_frozen else '✅ Active', 'inline': True},
                    {'name': 'Account Created', 'value': created_at, 'inline': True},
                    {'name': f'Total Tipped {ltc_emoji}', 'value': f'`{total_tipped:.8f}`', 'inline': True},
                    {'name': 'Total Received', 'value': f'`{total_received:.8f}`', 'inline': True},
                    {'name': 'Total Deposited', 'value': f'`{total_deposited:.8f}`', 'inline': True}
                ]
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BalanceCog(bot))
