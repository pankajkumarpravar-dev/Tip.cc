import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import logging
from database.db_manager import DatabaseManager
import asyncio

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Tippy')

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix='$',
    intents=intents,
    help_command=None,
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="crypto tips | $help"
    )
)

# Database instance
db_manager = None

@bot.event
async def on_ready():
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
        await db_manager.initialize()
    logger.info(f'✅ Tippy is online as {bot.user}')
    logger.info(f'🔗 Connected to {len(bot.guilds)} servers')
    sync_airdrop_timers.start()

@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You don't have permission to use this command.",
            color=0xe74c3c
        )
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title="❌ Bot Missing Permissions",
            description="I don't have the required permissions to execute this command.",
            color=0xe74c3c
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Missing Arguments",
            description=f"Missing required argument: `{error.param.name}`\n\nUse `$help {ctx.command}` for more info.",
            color=0xe74c3c
        )
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="❌ Invalid Argument",
            description="One or more arguments are invalid. Use `$help` for correct usage.",
            color=0xe74c3c
        )
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="⏰ Command on Cooldown",
            description=f"Please wait **{error.retry_after:.1f}s** before using this command again.",
            color=0xf39c12
        )
    else:
        logger.error(f'Unhandled error: {error}')
        embed = discord.Embed(
            title="❌ An Error Occurred",
            description="An unexpected error occurred. Please try again later.",
            color=0xe74c3c
        )
    
    try:
        await ctx.send(embed=embed, delete_after=10)
    except:
        pass

@tasks.loop(minutes=5)
async def sync_airdrop_timers():
    """Sync airdrop timers"""
    if db_manager:
        await db_manager.check_expired_airdrops()

async def load_cogs():
    """Load all cogs"""
    cogs_dir = 'cogs'
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'✅ Loaded cog: {filename}')
            except Exception as e:
                logger.error(f'❌ Failed to load {filename}: {e}')

async def main():
    """Start the bot"""
    async with bot:
        await load_cogs()
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            raise ValueError("DISCORD_TOKEN not found in .env file")
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
