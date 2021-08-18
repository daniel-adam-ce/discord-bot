import discord, json, os, datetime
from psycopg2 import sql
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from misc import connect

if os.path.exists('misc/config.json'):
    f = open('misc/config.json')
    data = json.load(f)
    f.close()
GUILD_ID= data['guild_id']

class voice_db_commands_slash(commands.Cog):
    def __init__(self, client):
        self.client = client
        if os.path.exists('misc/config.json'):
            f = open('misc/config.json')
            data = json.load(f)
            f.close()

        self.image_url = data['image_url']

    @commands.Cog.listener()
    async def on_ready(self):
        print('voice db slash ready')

    @cog_ext.cog_slash (
        name='voicedb',
        description='Check voice data for guild members',
        guild_ids=[GUILD_ID],
        options = [
            create_option(
                name = "option",
                description = "Select user to look at an individual's data. Select all to view all data.",
                option_type = 3,
                required = True,
                choices= [
                    create_choice(
                        name = "user",
                        value = "user"
                    ),
                    create_choice(
                        name = "all",
                        value = "all"
                    )
                ]
            ),
            create_option(
                name = "member",
                description= "Select a member to look at their data (only if the first option is user)",
                option_type = 6,
                required = False
            )
        ]
    )
    async def voicedb(self, ctx: SlashContext, option: int, member: discord.Member = None):
        # print(option, member)

        if option == "user":
            con = connect.connect()
            cur = con.cursor()
            query = 'SELECT total_time, first_record, anon_id FROM users WHERE discord_id = %s'
            cur.execute(query, (member.id,))
            times = cur.fetchone()
            total_time = 'N/A'
            first_record = 'N/A'
            average_duration = 'N/A'
            median_duration = 'N/A'
            average_time_joined = 'N/A'
            median_time_joined = 'N/A'
            if times != None:
                total_time = times[0]
                first_record = times[1]
                total_time = total_time - datetime.timedelta(microseconds=total_time.microseconds)
                # https://stackoverflow.com/questions/18470627/how-do-i-remove-the-microseconds-from-a-timedelta-object
                a_id = times[2]
                # query = sql.SQL('SELECT count(*) from {table}').format(table = sql.Identifier(f'user_{a_id}'))
                query = sql.SQL((
                    "SELECT AVG(duration), PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY duration),"
                    "AVG(EXTRACT(HOUR FROM start_time)),"
                    "PERCENTILE_DISC(0.5) WITHIN GROUP(ORDER BY EXTRACT(HOUR FROM start_time)) FROM {table} WHERE EXTRACT(HOUR FROM duration) >= 2"
                )).format(table = sql.Identifier(f'user_{a_id}'))
                cur.execute(query)
                num = cur.fetchone()
                average_duration = num[0]
                average_duration = average_duration - datetime.timedelta(microseconds=average_duration.microseconds)
                median_duration = num[1]
                median_duration = median_duration - datetime.timedelta(microseconds=median_duration.microseconds)
                average_time_joined=num[2]
                average_time_joined = round(average_time_joined, 1)
                median_time_joined=num[3]
            embed=discord.Embed (
                title="Voice Data", 
                colour = discord.Colour.blurple(), 
            )

            # print(time, type(time))
            embed.set_author(name = 'Daniel Adam', icon_url = self.image_url)
            embed.add_field(name= "User", value=f'{member.mention}', inline=True)
            embed.add_field(name="First record", value = f'{first_record} PST', inline = True)
            embed.add_field(name='\u200b', value = '\u200b', inline= False)
            embed.add_field(name="Total Time Spent in Voice Channels", value=total_time, inline=False)
            embed.add_field(name='\u200b', value = '\u200b', inline= False)
            embed.add_field(name='Average Time Spent Per Session', value=f'{average_duration}', inline = True)
            embed.add_field(name='Median Time Spent Per Session', value=f'{median_duration}', inline = True)
            embed.add_field(name='\u200b', value = '\u200b', inline= False)
            embed.add_field(name='Average Join Time (Hour)', value=f'{average_time_joined}', inline = True)
            embed.add_field(name='Median Join Time (Hour)', value=f'{median_time_joined}', inline = True)

            con.commit()
            cur.close()
            con.close()
            await ctx.send(embed=embed)
        elif option == "all":
            await ctx.send(content='This does not do anything yet')


def setup(client):
    client.add_cog(voice_db_commands_slash(client))

