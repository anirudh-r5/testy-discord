import discord
from discord.ext import commands
import asyncio

class Basic(commands.Cog):
    def __init__(self,client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    # async def event_name(self)
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.client.user} has connected to Discord!')

    #Commands
    # @commands.Command()
    # async def command_name(self,ctx)
    @commands.command(name='create-channel')
    @commands.has_guild_permissions(manage_channels=True)
    async def create_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name,category=discord.utils.get(ctx.guild.categories, name='Text Channels'))

    @commands.command(name='close')
    async def logout(self,ctx):
        guild = ctx.guild
        await ctx.send(f'See you later :)')
        await self.client.close()
        print(f'Disconnected from {guild}')

def setup(client):
    client.add_cog(Basic(client))