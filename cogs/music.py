import discord
from discord.ext import commands
import json
import asyncio

from youtube_dl import YoutubeDL

YT_OPTS={'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

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
                embed=discord.Embed(title="Searching...", color=0x002aff)
                await ctx.send(embed=embed, delete_after=2)
                searches = yt.extract_info(f"ytsearch5:{query}", download=False)['entries']
                embed=discord.Embed(title="YouTube Song Search", description="Choose a song from the list below, you picky pickle", color=0x002aff)
                count = 1
                for search in searches:
                    embed.add_field(name=f"{count}. {search['title']}", value=f"{search['webpage_url']}", inline=False)
                    print(f'{search["title"]}\t{search["webpage_url"]}')
                    count+=1
                embed.set_footer(text="enter the song number to start playing")
                await ctx.send(embed=embed)

                def check(user):
                    usr = user.author.name+'#'+user.author.discriminator
                    chnl = user.channel.name
                    return str(usr) == str(author) and str(chnl) == str(channel)

                try:
                    msg = await self.bot.wait_for('message',check=check,timeout=10)
                except asyncio.TimeoutError:
                    await ctx.send(f'Request Timed Out')
                else:
                    try:
                        choice = int(msg.content)
                    except ValueError:
                        await ctx.send(f'Invalid Choice')
                    else:
                        with YoutubeDL(YT_OPTS) as yt:
                            song_info = yt.extract_info(searches[choice-1]['webpage_url'], download=False)               
                            vc.play(discord.FFmpegPCMAudio(song_info["formats"][0]["url"],**FFMPEG_OPTIONS))
                            vc.source = discord.PCMVolumeTransformer(vc.source)
                            vc.source.volume = 1

    @commands.command()
    async def play(self,ctx,*,query):
        try:
            vchnl = ctx.author.voice.channel
        except AttributeError:
            await ctx.send(f'Please join a voice channel')
        else:
            vchnl = ctx.author.voice.channel
            vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if vc and vc.is_connected():
                await vc.move_to(vchnl)
            else:
                vc = await vchnl.connect() 
            with YoutubeDL(YT_OPTS) as yt:
                searches = yt.extract_info(f"ytsearch:{query}", download=False)['entries']
                print(f'{searches[0]["title"]}\t{searches[0]["webpage_url"]}')
                song_info = yt.extract_info(searches[0]['webpage_url'], download=False)               
                vc.play(discord.FFmpegPCMAudio(song_info["formats"][0]["url"],**FFMPEG_OPTIONS))
                vc.source = discord.PCMVolumeTransformer(vc.source)
                vc.source.volume = 1

    @commands.command()
    async def stop(self,ctx):
        vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if vc:
            vc.stop()
            await vc.disconnect()
            await ctx.send(f'Stopped playing')

def setup(bot):
    bot.add_cog(Music(bot))