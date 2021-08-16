import discord
import random
import asyncio
import os 
import json
# import youtube_dl
import shutil

from discord_slash import SlashCommand
from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get

#cringe = False

client = commands.Bot(command_prefix = ".")

@client.command()
async def load(ctx,extension):
    if ctx.author.guild_permissions.manage_roles:
        client.load_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('\u2705')
    else:
        await ctx.message.add_reaction('\u274c')

@client.command()
async def unload(ctx,extension):
    if ctx.author.guild_permissions.manage_roles:
        client.unload_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('\u2705')
    else:
        await ctx.message.add_reaction('\u274c')
    
@client.command()
async def reload(ctx, extension):
    if ctx.author.guild_permissions.manage_roles:
        client.unload_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('\u2705')
    else:
        await ctx.message.add_reaction('\u274c')
    if ctx.author.guild_permissions.manage_roles:
        client.load_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('\u2705')
    else:
        await ctx.message.add_reaction('\u274c')




if os.path.exists('misc/config.json'):
    f = open('misc/config.json')
    data = json.load(f)
    f.close()

token = data['token']


slash = SlashCommand(client, sync_commands=True)
# @slash.slash(name="test", description="This is just a test command, nothing more.", guild_ids=[203376646319767553])
# async def test(ctx):
#   await ctx.send(content="Hello World!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
client.run(token)