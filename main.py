import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(
    command_prefix="!",
    intents=nextcord.Intents.all(),
    help_command=None
)

# Charger tous les Cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user.name}")

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))