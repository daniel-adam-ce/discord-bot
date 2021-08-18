import discord, json, os, datetime
from psycopg2 import sql
from discord.ext import commands   
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
        query = 'SELECT total_time, first_record, anon_id FROM users WHERE discord_id = %s'
        cur.execute(query, (user.id,))
        times = cur.fetchone()
        total_time = 'N/A'
        first_record = 'N/A'
        average = 'N/A'
        if times != None:
            total_time = times[0]
            first_record = times[1]
            total_time = total_time - datetime.timedelta(microseconds=total_time.microseconds)
            # https://stackoverflow.com/questions/18470627/how-do-i-remove-the-microseconds-from-a-timedelta-object
            a_id = times[2]
            query = sql.SQL('SELECT count(*) from {table}').format(table = sql.Identifier(f'user_{a_id}'))
            cur.execute(query)
            num = cur.fetchone()[0]
            average = total_time / num
            average = average - datetime.timedelta(microseconds=average.microseconds)
        embed=discord.Embed (
            title="Voice Data", 
            colour = discord.Colour.blurple(), 
        )

        # print(time, type(time))
        embed.set_author(name = 'Daniel Adam', icon_url = self.image_url)
        embed.add_field(name= "User", value=f'{user.mention}', inline=False)
        embed.add_field(name="Time Spent in Voice Channels", value=total_time, inline=False)
        embed.add_field(name='Average Time Spend Per Session', value=f'{average}', inline = False)
        embed.add_field(name="First record", value = f'{first_record} PST', inline = False)

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

