import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name = 'load')
async def load(ctx,exten):
    try:
        bot.load_extension(f'cogs.{exten}')
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f'The **{exten}** extension is already loaded')
    except commands.ExtensionNotFound:
        await ctx.send(f'The **{exten}** extension is not found')
    except commands.ExtensionFailed:
        await ctx.send(f'The **{exten}** extension conatains an error')
    except commands.NoEntryPointError:
        await ctx.send(f'The **{exten}** extension conatains an error')
    else:
        await ctx.send(f'The **{exten}** extension has been loaded')

@bot.command(name = 'unload')
async def unload(ctx,exten):
    try:
        bot.unload_extension(f'cogs.{exten}')
    except commands.ExtensionNotLoaded:
        await ctx.send(f"The **{exten}** extension hasn't been loaded")
    else:
        await ctx.send(f'The **{exten}** extension has been unloaded')

@bot.command(name = 'reload')
async def reload(ctx,exten):
    try:
        bot.reload_extension(f'cogs.{exten}')
    except commands.ExtensionNotLoaded:
        await ctx.send(f"The **{exten}** extension hasn't been loaded")
    except commands.ExtensionNotFound:
        await ctx.send(f'The **{exten}** extension is not found')
    except commands.ExtensionFailed:
        await ctx.send(f'The **{exten}** extension conatains an error')
    except commands.NoEntryPointError:
        await ctx.send(f'The **{exten}** extension conatains an error')
    else:
        await ctx.send(f'The **{exten}** extension has been reloaded')



for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
bot.run(TOKEN)