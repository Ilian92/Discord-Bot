import nextcord
import yt_dlp
import asyncio
from nextcord.ext import commands

# Configuration yt-dlp
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ffmpeg_options = {'options': '-vn'}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}

    async def disconnect_after_timeout(self, guild_id):
        await asyncio.sleep(300)
        if guild_id in self.voice_clients:
            vc, _ = self.voice_clients[guild_id]
            if vc.is_connected() and not vc.is_playing():
                await vc.disconnect()
            del self.voice_clients[guild_id]

    @commands.command()
    async def musique(self, ctx, url: str):
        if not ctx.author.voice:
            await ctx.send("🚫 Vous devez être dans un salon vocal !")
            return

        channel = ctx.author.voice.channel
        guild_id = ctx.guild.id

        if guild_id in self.voice_clients:
            vc, task = self.voice_clients[guild_id]
            task.cancel()
            if vc.channel != channel:
                await vc.move_to(channel)
        else:
            vc = await channel.connect()

        data = await self.bot.loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        url = data['url']
        
        vc.play(
            nextcord.FFmpegPCMAudio(url, **ffmpeg_options),
            after=lambda e: self.bot.loop.create_task(self.on_play_end(guild_id))
        )

        task = self.bot.loop.create_task(self.disconnect_after_timeout(guild_id))
        self.voice_clients[guild_id] = (vc, task)
        await ctx.send(f"🎵 Lecture de : **{data['title']}**")

    async def on_play_end(self, guild_id):
        if guild_id in self.voice_clients:
            vc, task = self.voice_clients[guild_id]
            task.cancel()
            new_task = self.bot.loop.create_task(self.disconnect_after_timeout(guild_id))
            self.voice_clients[guild_id] = (vc, new_task)

def setup(bot):
    bot.add_cog(MusicCommands(bot))