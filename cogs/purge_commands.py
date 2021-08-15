import discord
import random
import asyncio

from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get

class purge_commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is ready')

    # Commands
    
    @commands.command()
    async def purge(self, ctx, num):
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.add_reaction('\u2705')
            await ctx.channel.purge(limit=int(num) + 1)
        else:
            await ctx.message.add_reaction('\u274c')
            await ctx.send("u dont got da powa bro")


def setup(client):
    client.add_cog(purge_commands(client))

