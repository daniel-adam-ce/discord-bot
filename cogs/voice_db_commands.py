import discord
import random
import asyncio
import psycopg2
import json
import os
from datetime import datetime
from psycopg2 import sql
import datetime
from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get
from discord_slash import cog_ext
from misc import connect

class voice_db_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        if os.path.exists('misc/config.json'):
            f = open('misc/config.json')
            data = json.load(f)
            f.close()

        self.image_url = data['image_url']

    @commands.Cog.listener()
    async def on_ready(self):
        print('voice db ready')

    @commands.command()
    async def voiceCheckUser(self, ctx, user: discord.Member):
        print(user.display_name)
        
        con = connect.connect()
        cur = con.cursor()
        query = 'SELECT total_time FROM users WHERE discord_id = %s'
        cur.execute(query, (user.id,))
        time = cur.fetchone()
        if time != None:
            time = time[0]
            time = time - datetime.timedelta(microseconds=time.microseconds)
            # https://stackoverflow.com/questions/18470627/how-do-i-remove-the-microseconds-from-a-timedelta-object
        else:
            time = 'N/A'
        embed=discord.Embed (
            title="Voice Data", 
            colour = discord.Colour.blurple(), 
        )

        # print(time, type(time))
        embed.set_author(name = 'Daniel Adam', icon_url = self.image_url)
        embed.add_field(name= "User", value=f'{user.mention}', inline=False)
        embed.add_field(name="Time Spent in Voice Channels", value=time, inline=False)

        con.commit()
        cur.close()
        con.close()
        await ctx.send(embed=embed)
    
    @commands.command()
    async def voiceCheckAll(self, ctx):
        # embed=discord.Embed (
        #     title="Voice Data", 
        #     description=f'Top 10 Users', 
        #     colour = discord.Colour.blurple(), 
        #     image = "misc/icon.png"
        # )
        await ctx.send("this doesn't do anything right now")

def setup(client):
    client.add_cog(voice_db_commands(client))


# https://cdn.discordapp.com/avatars/769067829403844648/ce370be164e7746872ae1e5e74af648d.webp?size=128
