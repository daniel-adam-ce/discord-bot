import discord
import random
import asyncio
import os
import json
from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

if os.path.exists('misc/config.json'):
    f = open('misc/config.json')
    data = json.load(f)
    f.close()
GUILD_ID= data['guild_id']

class purge_commands_slash(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print('purge slash ready')

    # Commands
    
    @cog_ext.cog_slash (
        name='purge', 
        description='Deletes messages',
        guild_ids=[GUILD_ID]
    )
    async def purge(self, ctx: SlashContext, num: int):
        # print('test')
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.purge(limit=int(num))
            await ctx.send(content=f'{num} messages deleted.')
        else:
            await ctx.send(content="You lack permissions.")


def setup(client):
    client.add_cog(purge_commands_slash(client))

