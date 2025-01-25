import os
import json
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Charge le token depuis .env

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user.name}")

# commande "!ping"
@bot.command()
# Si on écrit "!ping" le bot répondra "Pong 🏓". La commande que le doit écrire correspond au "command_prefix" défini plus haut et du nom de la fonction ci-dessous.
async def ping(ctx):
    await ctx.send("Pong 🏓")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Tu n'as pas la permission !")

# commande "!clear"
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)  # +1 pour inclure la commande
    await ctx.send(f"🧹 {amount} messages supprimés !", delete_after=3)

# Charge les commandes depuis le JSON
with open("commands.json", "r") as f:
    commands_data = json.load(f)

@bot.command()
async def help(ctx):
    # Crée un Embed stylisé
    embed = nextcord.Embed(
        title="📚 Liste des commandes",
        description="Toutes les commandes disponibles :",
        color=0x00ff00
    )
    
    # Ajoute chaque commande dans l'Embed
    for cmd, info in commands_data.items():
        embed.add_field(
            name=f"**{info['usage']}**",
            value=f"*{info['description']}*",
            inline=False
        )
    
    # Envoie l'Embed
    await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN")) 