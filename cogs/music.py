import discord
from discord.ext import commands
import asyncio

from youtube_dl import YoutubeDL
from asyncio import run_coroutine_threadsafe

YT_OPTS={'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class Music(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.music_queue = []
        self.iteror = iter(self.music_queue)
        self.voicer = None
    # Events
    # @commands.Cog.listener()
    # async def event_name(self)

    #Commands
    @commands.command()
    async def search(self,ctx, *, query):
        try:
            vchnl = ctx.author.voice.channel
        except AttributeError:
            await ctx.send(f'Please join a voice channel')
        else:
            vchnl = ctx.author.voice.channel
            vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            author = ctx.author
            channel = ctx.channel
            if vc and vc.is_connected():
                await vc.move_to(vchnl)
            else:
                vc = await vchnl.connect() 
            with YoutubeDL(YT_OPTS) as yt:
                embed=discord.Embed(title="Searching...", color=0xff0000)
                await ctx.send(embed=embed, delete_after=2)
                searches = yt.extract_info(f"ytsearch5:{query}", download=False)['entries']
                embed=discord.Embed(title="YouTube Song Search", description="Choose a song from the list below", color=0xff0000)
                count = 1
                for search in searches:
                    embed.add_field(name=f"{count}. {search['title']}", value=f"{search['webpage_url']}", inline=False)
                    count+=1
                embed.set_footer(text="enter the song number to start playing")
                await ctx.send(embed=embed, delete_after=10)

                def check(user):
                    usr = user.author.name+'#'+user.author.discriminator
                    chnl = user.channel.name
                    return str(usr) == str(author) and str(chnl) == str(channel)

                try:
                    msg = await self.bot.wait_for('message',check=check,timeout=10)
                except asyncio.TimeoutError:
                    await ctx.send(f'⏲ **No song was chosen**')
                else:
                    try:
                        choice = int(msg.content)
                    except ValueError:
                        await ctx.send(f'😒 **Invalid Choice**', delete_after=10)
                    else:
                        self.music_queue.append(searches[choice-1]['webpage_url'])
                        self.player(vc,ctx)                       

    @commands.command()
    async def play(self,ctx,*,query):
        try:
            vchnl = ctx.author.voice.channel
        except AttributeError:
            await ctx.send(f'❌ **Please join a voice channel**')
        else:
            vchnl = ctx.author.voice.channel
            vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if vc and vc.is_connected():
                await vc.move_to(vchnl)
            else:
                vc = await vchnl.connect() 
            with YoutubeDL(YT_OPTS) as yt:
                searches = yt.extract_info(f"ytsearch:{query}", download=False)['entries']
                self.music_queue.append(searches[0]['webpage_url'])
                self.player(vc,ctx)

    @commands.command()
    async def stop(self,ctx):
        vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if vc:
            vc.stop()
            await vc.disconnect()
            await ctx.send(f'⏹ **Stopped playing & left the voice channel**')
        else:
            await ctx.send(f'❌ **No audio is being played**')
   
    def player(self,vc,ctx):
        if not vc.is_playing():
            try:
                page = next(self.iteror)
            except StopIteration:
                print('Queue empty')
                run_coroutine_threadsafe(vc.disconnect(), self.bot.loop)
                run_coroutine_threadsafe(self.send_status(discord.Embed(title="Finished queue", description="No more songs to play", color=0xff0000),ctx), self.bot.loop)
            else:
                with YoutubeDL(YT_OPTS) as yt:
                    song_info = yt.extract_info(page, download=False)
                    embed=discord.Embed(title="▶ Now Playing...", description=song_info["title"], color=0xff0000)   
                    embed.set_thumbnail(url=song_info['thumbnails'][0]['url'])
                    embed.set_footer(text=song_info["webpage_url"])               
                    vc.play(discord.FFmpegPCMAudio(song_info["formats"][0]["url"],**FFMPEG_OPTIONS), after = lambda e:self.player(vc,ctx))
                    vc.source = discord.PCMVolumeTransformer(vc.source)
                    vc.source.volume = 1
                    run_coroutine_threadsafe(self.send_status(embed,ctx), self.bot.loop)
        else:
            run_coroutine_threadsafe(self.send_status(discord.Embed(title="Music queued!", color=0xff0000),ctx), self.bot.loop)

    async def send_status(self, embed, ctx):
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Music(bot))