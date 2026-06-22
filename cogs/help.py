import discord
from discord.ext import commands
from utils.embeds import EmbedFactory, COLOR_INFO, COLOR_SUCCESS, COLOR_ERROR
from datetime import datetime
import os

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx, command_name: str = None):
        """Get help about commands"""
        if command_name:
            cmd = self.bot.get_command(command_name)
            if cmd:
                embed = EmbedFactory.create_embed(
                    title=f"Help: ${cmd.name}",
                    description=cmd.help or "No description available",
                    color=COLOR_INFO,
                    fields=[{'name': 'Usage', 'value': f"`${cmd.name} {cmd.signature}`", 'inline': False}]
                )
            else:
                embed = EmbedFactory.error("Command not found", f"The command `{command_name}` does not exist.")
        else:
            embed = EmbedFactory.create_embed(
                title="📚 Tippy Command List",
                description="Use `$help <command>` for more info on a command",
                color=COLOR_INFO,
                fields=[
                    {'name': '💰 Wallet Commands', 'value': '`$balance` `$deposit` `$withdraw` `$profile`', 'inline': False},
                    {'name': '💸 Tipping Commands', 'value': '`$tip` `$airdrop` `$rain` `$luckytip`', 'inline': False},
                    {'name': '📊 Stats Commands', 'value': '`$transactions` `$leaderboard` `$daily`', 'inline': False},
                    {'name': '⚙️ Settings', 'value': '`$settings`', 'inline': False},
                    {'name': '👑 Admin Commands', 'value': '`$addbalance` `$removebalance` `$freeze` `$unfreeze`', 'inline': False}
                ]
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
