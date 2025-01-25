import json
import nextcord
from nextcord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        with open("commands.json", "r") as f:
            commands_data = json.load(f)
        
        embed = nextcord.Embed(
            title="📚 Liste des commandes",
            description="Utilisez `!help` pour voir ce message",
            color=0x00ff00
        )
        
        for category, commands in commands_data.items():
            value = "\n".join(
                f"**{cmd}** : {info['description']}\n*Usage* : `{info['usage']}`"
                for cmd, info in commands.items()
            )
            embed.add_field(name=f"===={category}====", value=value, inline=False)
        
        await ctx.send(embed=embed)

# Fonction setup obligatoire
def setup(bot):
    bot.add_cog(HelpCommands(bot))