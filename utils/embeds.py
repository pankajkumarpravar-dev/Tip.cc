import discord
from datetime import datetime

COLOR_SUCCESS = 0x2ecc71
COLOR_ERROR = 0xe74c3c
COLOR_WARNING = 0xf39c12
COLOR_INFO = 0x3498db
COLOR_SECONDARY = 0x9b59b6

class EmbedFactory:
    """Factory for creating consistent embeds"""
    
    @staticmethod
    def create_embed(
        title: str = None,
        description: str = None,
        color: int = COLOR_INFO,
        thumbnail: str = None,
        image: str = None,
        fields: list = None,
        footer_text: str = None,
        footer_icon: str = None,
        author_name: str = None,
        author_icon: str = None,
        timestamp: bool = False
    ) -> discord.Embed:
        """Create a professional embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.utcnow() if timestamp else None
        )
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        
        if image:
            embed.set_image(url=image)
        
        if fields:
            for field in fields:
                embed.add_field(
                    name=field.get('name'),
                    value=field.get('value'),
                    inline=field.get('inline', False)
                )
        
        if author_name:
            embed.set_author(name=author_name, icon_url=author_icon)
        
        if footer_text:
            embed.set_footer(text=footer_text, icon_url=footer_icon)
        else:
            embed.set_footer(text="Tippy • Crypto Tipping Bot")
        
        return embed
    
    @staticmethod
    def success(title: str, description: str = None, **kwargs) -> discord.Embed:
        """Create a success embed"""
        return EmbedFactory.create_embed(
            title=f"✅ {title}",
            description=description,
            color=COLOR_SUCCESS,
            **kwargs
        )
    
    @staticmethod
    def error(title: str, description: str = None, **kwargs) -> discord.Embed:
        """Create an error embed"""
        return EmbedFactory.create_embed(
            title=f"❌ {title}",
            description=description,
            color=COLOR_ERROR,
            **kwargs
        )
    
    @staticmethod
    def warning(title: str, description: str = None, **kwargs) -> discord.Embed:
        """Create a warning embed"""
        return EmbedFactory.create_embed(
            title=f"⚠️ {title}",
            description=description,
            color=COLOR_WARNING,
            **kwargs
        )
    
    @staticmethod
    def info(title: str, description: str = None, **kwargs) -> discord.Embed:
        """Create an info embed"""
        return EmbedFactory.create_embed(
            title=f"ℹ️ {title}",
            description=description,
            color=COLOR_INFO,
            **kwargs
        )
