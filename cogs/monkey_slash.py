from itertools import filterfalse
import discord
import random
import asyncio
import datetime
import os, json
from discord.ext.commands.errors import CommandInvokeError
import psycopg2
from discord_slash import cog_ext, SlashContext
from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get
from misc import connect
from discord_slash.utils.manage_commands import create_choice, create_option
if os.path.exists('misc/config.json'):
    f = open('misc/config.json')
    data = json.load(f)
    f.close()
GUILD_ID= data['guild_id']

class monkey_commands_slash(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print('monkey slashready')

    # Commands
    
    @cog_ext.cog_slash (
        name='monkey', 
        description='monkey',
        guild_ids=[GUILD_ID],
        options = [
            create_option(
                name="option",
                description="type show, add, or all",
                option_type = 3,
                required = True
            ),
            create_option(
                name="link",
                description="link if adding monkey",
                option_type=3,
                required = False
            )   
        ]
    )
    async def monkey(self, ctx: SlashContext, option: str = None, link: str = None):
        con = connect.connect()
        cur = con.cursor()
        #print (option, link)
        if option == 'show' or option == None:

            query = 'SELECT link FROM monkey'
            cur.execute(query)

            links = cur.fetchall()
            #print(links)
            con.commit()
            cur.close()
            con.close()
        
            await ctx.send(f'{links[random.randint(0, (len(links)-1))][0]}')  
        elif option == 'add':
            if 'https' in link:
                time = datetime.datetime.now().replace(microsecond=0)
                try:
                    query = 'INSERT INTO monkey (user_id_added_by, date_added, link) VALUES (%s, %s, %s)'
                    cur.execute(query, (ctx.message.author.id, time, link))
                except Exception: 
                    await ctx.send(content='Something went wrong, monkey might already be added.')
                    cur.close()
                    con.close()
                else:
                    con.commit()
                    cur.close()
                    con.close()
                    await ctx.send(content='Monke added')
            else:
                await ctx.send('The link you sent is invalid.')
        elif option == 'all':
            await ctx.send(content='\'all\' does not do anything atm')
                



def setup(client):
    client.add_cog(monkey_commands_slash(client))


