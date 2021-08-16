import discord
import random
import asyncio
import datetime
from discord.ext.commands.errors import CommandInvokeError
import psycopg2
from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get
from misc import connect
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
        # monkey = genMonkey()
        con = connect.connect()
        cur = con.cursor()
        query = 'SELECT link FROM monkey'
        cur.execute(query)

        links = cur.fetchall()
        # print(links)
        con.commit()
        cur.close()
        con.close()
        await ctx.message.add_reaction('\u2705')
        await ctx.send(f'{links[random.randint(0, (len(links)-1))][0]}')
    
    @commands.command()
    async def addMonkey(self, ctx, link: str):
        # addMonkey(str(link))
        
        if ctx.author.guild_permissions.manage_roles:
            con = connect.connect()
            cur = con.cursor()

            time = datetime.datetime.now().replace(microsecond=0)
            try:
                query = 'INSERT INTO monkey (user_id_added_by, date_added, link) VALUES (%s, %s, %s)'
                cur.execute(query, (ctx.message.author.id, time, link))
            except Exception: 
                await ctx.message.add_reaction('\u274c')
                await ctx.send('Something went wrong, monkey might already be added.')
                cur.close()
                con.close()
            else:
                con.commit()
                cur.close()
                con.close()
                await ctx.message.add_reaction('\u2705')
        else:
            await ctx.message.add_reaction('\u274c')
            await ctx.send('You lack permissions.')


def setup(client):
    client.add_cog(monkey_commands(client))


