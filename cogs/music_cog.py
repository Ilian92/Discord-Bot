import os
import asyncio
import aiohttp
import nextcord
from nextcord.ext import commands
from yt_dlp import YoutubeDL
from collections import deque

# Options yt-dlp et FFmpeg
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'cookiesfrombrowser': ('chrome',),
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ffmpeg_options = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ytdl = YoutubeDL(ytdl_format_options)
        self.voice_clients = {}  # {guild_id: voice_client}
        self.queues = {}  # {guild_id: deque}
        self.current_song = {}  # {guild_id: song_info}

    async def is_music_video(self, video_id):
        """
        Vérifie si une vidéo YouTube est de la catégorie 'Music' en utilisant l'API YouTube.
        """
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            raise ValueError("La clé API YouTube n'est pas configurée dans .env")

        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Erreur API YouTube : {response.status}")
                    return False

                data = await response.json()
                if "items" in data and data["items"]:
                    category_id = data["items"][0]["snippet"]["categoryId"]
                    return category_id == "10"  # ID de la catégorie "Music"
                return False

    async def check_empty_voice_channel(self, guild_id):
        """
        Vérifie si le bot est seul dans le salon vocal et se déconnecte si c'est le cas.
        """
        if guild_id in self.voice_clients:
            vc = self.voice_clients[guild_id]
            if vc.is_connected() and len(vc.channel.members) == 1:  # Seul le bot est dans le salon
                await vc.disconnect()
                del self.voice_clients[guild_id]
                if guild_id in self.queues:
                    del self.queues[guild_id]
                if guild_id in self.current_song:
                    del self.current_song[guild_id]

    async def play_next(self, guild_id):
        """
        Joue la prochaine musique dans la file d'attente.
        """
        if guild_id in self.queues and self.queues[guild_id]:
            song_info = self.queues[guild_id].popleft()
            self.current_song[guild_id] = song_info
            vc = self.voice_clients[guild_id]

            vc.play(
                nextcord.FFmpegOpusAudio(song_info['url'], **ffmpeg_options),
                after=lambda e: self.bot.loop.create_task(self.on_play_end(guild_id))
            )
            await self.bot.get_channel(song_info['channel_id']).send(f"🎵 Lecture de : **{song_info['title']}**")
        else:
            await self.check_empty_voice_channel(guild_id)

    async def on_play_end(self, guild_id):
        """
        Gère la fin de la lecture et passe à la musique suivante.
        """
        if guild_id in self.voice_clients:
            await self.play_next(guild_id)

    @commands.command()
    async def play(self, ctx, url: str):
        """
        Ajoute une musique à la file d'attente ou la joue directement.
        """
        # Vérifie si l'utilisateur est dans un salon vocal
        if not ctx.author.voice:
            await ctx.send("🚫 Vous devez être dans un salon vocal !")
            return

        # Extrait l'ID de la vidéo YouTube
        try:
            data = await self.bot.loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
            video_id = data["id"]
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de l'extraction de l'ID de la vidéo : {e}")
            return

        # Vérifie si la vidéo est de la catégorie "Music"
        if not await self.is_music_video(video_id):
            await ctx.send("❌ Seules les vidéos de musique sont autorisées !")
            return

        # Ajoute la musique à la file d'attente
        guild_id = ctx.guild.id
        if guild_id not in self.queues:
            self.queues[guild_id] = deque()

        song_info = {
            'url': data['url'],
            'title': data['title'],
            'channel_id': ctx.channel.id
        }
        self.queues[guild_id].append(song_info)

        # Affiche la position dans la file d'attente
        position = len(self.queues[guild_id])
        await ctx.send(f"🎵 **{data['title']}** a été ajouté à la file d'attente (position {position}).")

        # Si aucune musique n'est en cours de lecture, commence la lecture
        if guild_id not in self.voice_clients or not self.voice_clients[guild_id].is_playing():
            channel = ctx.author.voice.channel
            if guild_id in self.voice_clients:
                vc = self.voice_clients[guild_id]
                if vc.channel != channel:
                    await vc.move_to(channel)
            else:
                vc = await channel.connect()
                self.voice_clients[guild_id] = vc

            await self.play_next(guild_id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        Déconnecte le bot s'il est seul dans le salon vocal.
        """
        if member != self.bot.user:
            guild_id = member.guild.id
            await self.check_empty_voice_channel(guild_id)

def setup(bot):
    bot.add_cog(MusicCommands(bot))