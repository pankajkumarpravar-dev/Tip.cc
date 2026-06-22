import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import logging
from database.db_manager import DatabaseManager
import asyncio
import sys
from pathlib import Path

# Load environment variables
load_dotenv()

# Create data directory for database
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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
        db_manager = DatabaseManager(db_path=str(data_dir / 'tippy.db'))
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
        try:
            await db_manager.check_expired_airdrops()
        except Exception as e:
            logger.error(f'Error syncing airdrops: {e}')

async def load_cogs():
    """Load all cogs"""
    cogs_dir = 'cogs'
    loaded = 0
    failed = 0
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'✅ Loaded cog: {filename}')
                loaded += 1
            except Exception as e:
                logger.error(f'❌ Failed to load {filename}: {e}')
                failed += 1
    
    logger.info(f'📊 Loaded {loaded} cogs, {failed} failed')

async def main():
    """Start the bot"""
    try:
        async with bot:
            await load_cogs()
            token = os.getenv('DISCORD_TOKEN')
            if not token:
                raise ValueError("❌ DISCORD_TOKEN not found in environment variables")
            logger.info("🚀 Starting Tippy bot...")
            await bot.start(token)
    except Exception as e:
        logger.error(f'❌ Failed to start bot: {e}')
        sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⛔ Bot shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f'❌ Fatal error: {e}')
        sys.exit(1)
