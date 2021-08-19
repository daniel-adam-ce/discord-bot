import discord
import random
import asyncio
import os, json
from discord_slash import SlashCommand
from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get

#cringe = False

client = commands.Bot(command_prefix = ".")

@client.command()
async def load(ctx,extension):
    try:
        if ctx.author.guild_permissions.manage_roles:
            client.load_extension(f'cogs.{extension}')
            await ctx.message.add_reaction('\u2705')
        else:
            await ctx.message.add_reaction('\u274c')
    except Exception as ex:
        await ctx.send(f'Something went wrong: {ex}')

@client.command()
async def unload(ctx,extension):
    try:
        if ctx.author.guild_permissions.manage_roles:
            client.unload_extension(f'cogs.{extension}')
            await ctx.message.add_reaction('\u2705')
        else:
            await ctx.message.add_reaction('\u274c')
    except Exception as ex:
        await ctx.send(f'Something went wrong: {ex}')
    
@client.command()
async def reload(ctx, extension):
    try:
        if ctx.author.guild_permissions.manage_roles:
            client.unload_extension(f'cogs.{extension}')
            await ctx.message.add_reaction('\u2705')
        else:
            await ctx.message.add_reaction('\u274c')
        if ctx.author.guild_permissions.manage_roles:
            client.load_extension(f'cogs.{extension}')
            await ctx.message.add_reaction('\u2611')
        else:
            await ctx.message.add_reaction('\u2716')
    except Exception as ex:
        await ctx.send(f'Something went wrong: {ex}')




if os.path.exists('misc/config.json'):
    f = open('misc/config.json')
    data = json.load(f)
    f.close()

token = data['token']


slash = SlashCommand(client, sync_commands=True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
client.run(token)