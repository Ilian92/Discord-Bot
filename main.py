import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Charge le token depuis .env

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user.name}")

@bot.command()
# Si on écrit "!ping" le bot répondra "Pong 🏓". La commande que le doit écrire correspond au "command_prefix" défini plus haut et du nom de la fonction ci-dessous.
async def ping(ctx):
    await ctx.send("Pong 🏓")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Tu n'as pas la permission !")

bot.run(os.getenv("TOKEN"))