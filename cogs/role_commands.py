import discord
import random
import asyncio

from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get

class role_commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is ready')

    # Commands
    
    @commands.command()
    async def addRole(self, ctx, role: discord.Role, user: discord.Member):
        if ctx.author.guild_permissions.manage_messages:
            await user.add_roles(role)
            await ctx.message.add_reaction('\u2705')
        else:
            await ctx.message.add_reaction('\u274c')
            #await ctx.send('u dont got da powa bro')

    @commands.command()
    async def removeRole(self, ctx, role: discord.Role, user: discord.Member):
        print(role, user)
        if ctx.author.guild_permissions.manage_messages:
            await user.remove_roles(role)
            await ctx.message.add_reaction('\u2705')
        else:
            await ctx.message.add_reaction('\u274c')
            #await ctx.send('u dont go da powa bro')


def setup(client):
    client.add_cog(role_commands(client))



