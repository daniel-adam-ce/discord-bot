import discord
import random
import asyncio

from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get

class monkey_commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print('monkey ready')

    # Commands
    
    @commands.command()
    async def monkey(self, ctx):
        monkey = genMonkey()
        await ctx.message.add_reaction('\u2705')
        await ctx.send(f'{monkey}')
    
    @commands.command()
    async def addMonkey(self, ctx, link):
        addMonkey(str(link))
        if ctx.author.guild_permissions.manage_roles:
            await ctx.message.add_reaction('\u2705')
        else:
            await ctx.message.add_reaction('\u274c')

def addMonkey(link):
    f = open('monkey.txt','r')
    monkey_file = f.readlines()

    monkey_file.append(link + '\n')
    #print(monkey_file)
    with open('monkey.txt','w') as log:
        for i in range(len(monkey_file)):
            log.write((monkey_file[i]))
    return

def genMonkey():
        f = open('monkey.txt','r')
        monkey_file = f.readlines()
        num = random.randint(0, (len(monkey_file)-1))
        return str(monkey_file[num])

def setup(client):
    client.add_cog(monkey_commands(client))


