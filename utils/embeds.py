# utils/embeds.py
import nextcord

# Palette de couleurs prédéfinies
COLOR_SUCCESS = 0x00ff00  # Vert
COLOR_ERROR = 0xff0000    # Rouge
COLOR_INFO = 0x3498db     # Bleu
COLOR_WARNING = 0xf1c40f  # Jaune

def create_embed(ctx, embed_type="info", title="", description="", fields=None, thumbnail=None):
    """
    Crée un embed stylisé avec des paramètres communs
    """
    # Déterminer la couleur en fonction du type
    color_mapping = {
        "success": COLOR_SUCCESS,
        "error": COLOR_ERROR,
        "info": COLOR_INFO,
        "warning": COLOR_WARNING
    }
    
    embed = nextcord.Embed(
        title=f"{get_emoji(embed_type)} {title}",
        description=description,
        color=color_mapping.get(embed_type, COLOR_INFO)
    )
    
    # Ajouter des champs si spécifiés
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
    
    # Ajouter une miniature
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    # Footer personnalisé avec l'auteur
    embed.set_footer(
        text=f"Demandé par {ctx.author.display_name}",
        icon_url=ctx.author.avatar.url
    )
    
    return embed

def get_emoji(embed_type):
    """
    Retourne un emoji correspondant au type d'embed
    """
    emoji_mapping = {
        "success": "✅",
        "error": "❌",
        "info": "ℹ️",
        "warning": "⚠️"
    }
    return emoji_mapping.get(embed_type, "")

# Embeds spécialisés
def error_embed(ctx, message):
    return create_embed(
        ctx,
        embed_type="error",
        title="Erreur",
        description=f"**{message}**",
        fields=[("Besoin d'aide ?", f"Utilisez `{ctx.prefix}help`", False)]
    )

def success_embed(ctx, message):
    return create_embed(
        ctx,
        embed_type="success",
        title="Succès",
        description=f"**{message}**"
    )

def music_embed(ctx, title, description):
    return create_embed(
        ctx,
        embed_type="info",
        title=f"🎵 {title}",
        description=description,
        color=0x1db954  # Vert Spotify
    )

def welcome_embed(member):
    embed = nextcord.Embed(
        title=f"🎉 Bienvenue {member.display_name} !",
        description="Merci de rejoindre notre serveur !",
        color=0xffd700  # Or
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(
        name="Règles",
        value="Lisez les règles dans <#ID_SALON_RÈGLES>",
        inline=False
    )
    return embed