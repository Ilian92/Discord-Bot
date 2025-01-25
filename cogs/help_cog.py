import json
from nextcord.ext import commands
from utils.embeds import create_embed

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        with open("commands.json", "r") as f:
            commands_data = json.load(f)

        fields = []
        for cmd, info in commands_data.items():
            fields.append((f"`{info['usage']}`", info["description"], False))

        embed = create_embed(
            ctx,
            embed_type="info",
            title="Liste des commandes",
            description="Utilisez le préfixe `!` devant chaque commande",
            fields=fields
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCommands(bot))