import discord
from discord.ext import commands
from utils.embeds import EmbedFactory, COLOR_ERROR, COLOR_SUCCESS
from bot import db_manager
import os

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, ctx):
        admin_ids = os.getenv('ADMIN_IDS', '').split(',')
        return str(ctx.author.id) in admin_ids or ctx.author.guild_permissions.administrator

    @commands.command(name='addbalance')
    async def addbalance(self, ctx, user: discord.User, coin: str, amount: float):
        """[ADMIN] Add balance to user"""
        if not self.is_admin(ctx):
            embed = EmbedFactory.error("Permission Denied", "You don't have permission to use this command")
            await ctx.send(embed=embed)
            return
        
        try:
            await db_manager.get_or_create_user(user.id, user.name)
            await db_manager.update_user_balance(user.id, coin.lower(), amount)
            await db_manager.add_transaction(user.id, 'admin_add', coin.upper(), amount, f"Added by {ctx.author.name}")
            
            embed = EmbedFactory.success(
                "Balance Added",
                f"Added {amount:.8f} {coin.upper()} to {user.mention}"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='removebalance')
    async def removebalance(self, ctx, user: discord.User, coin: str, amount: float):
        """[ADMIN] Remove balance from user"""
        if not self.is_admin(ctx):
            embed = EmbedFactory.error("Permission Denied", "You don't have permission to use this command")
            await ctx.send(embed=embed)
            return
        
        try:
            await db_manager.get_or_create_user(user.id, user.name)
            await db_manager.update_user_balance(user.id, coin.lower(), -amount)
            await db_manager.add_transaction(user.id, 'admin_remove', coin.upper(), amount, f"Removed by {ctx.author.name}")
            
            embed = EmbedFactory.success(
                "Balance Removed",
                f"Removed {amount:.8f} {coin.upper()} from {user.mention}"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='freeze')
    async def freeze(self, ctx, user: discord.User):
        """[ADMIN] Freeze user account"""
        if not self.is_admin(ctx):
            embed = EmbedFactory.error("Permission Denied", "You don't have permission to use this command")
            await ctx.send(embed=embed)
            return
        
        try:
            await db_manager.freeze_user(user.id)
            embed = EmbedFactory.success(
                "User Frozen",
                f"{user.mention}'s account has been frozen"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='unfreeze')
    async def unfreeze(self, ctx, user: discord.User):
        """[ADMIN] Unfreeze user account"""
        if not self.is_admin(ctx):
            embed = EmbedFactory.error("Permission Denied", "You don't have permission to use this command")
            await ctx.send(embed=embed)
            return
        
        try:
            await db_manager.unfreeze_user(user.id)
            embed = EmbedFactory.success(
                "User Unfrozen",
                f"{user.mention}'s account has been unfrozen"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

    @commands.command(name='maintenance')
    async def maintenance(self, ctx):
        """[ADMIN] Set bot to maintenance mode"""
        if not self.is_admin(ctx):
            embed = EmbedFactory.error("Permission Denied", "You don't have permission to use this command")
            await ctx.send(embed=embed)
            return
        
        try:
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="🔧 Maintenance Mode"
                )
            )
            embed = EmbedFactory.success("Maintenance Mode", "Bot is now in maintenance mode")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedFactory.error("Error", str(e))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
