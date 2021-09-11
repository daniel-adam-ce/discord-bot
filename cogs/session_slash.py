
import os, json, discord, datetime
from psycopg2 import sql
from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from misc import connect

if os.path.exists('misc/config.json'):
    f = open('misc/config.json')
    data = json.load(f)
    f.close()
GUILD_ID= data['guild_id']

class check_session_slash(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print('help slash ready')

    # Commands
    
    @cog_ext.cog_slash (
        name='session', 
        description='Check to see how long the first ten users have been in a voice channel. Or, check only one user.',
        guild_ids=[GUILD_ID],
        options = [
            create_option(
                name = "member",
                description= "Optional: select a specific member to check.",
                option_type = 6,
                required = False
            )
        ]
    )
    async def session(self, ctx: SlashContext, member: discord.Member = None):
        #print(ctx.guild.voice_channels, member)
        con = connect.connect()
        cur = con.cursor()
        try:
            if member.voice != None:
                query = 'SELECT anon_id FROM users WHERE discord_id = %s LIMIT 1'
                cur.execute(query, (member.id,))
                a_id = cur.fetchone()
                #print(a_id)
                if a_id != None:
                    query = sql.SQL('SELECT start_time FROM {table} ORDER BY start_time DESC LIMIT 1').format(table = sql.Identifier(f'user_{a_id[0]}'))
                    cur.execute(query)
                    start_time = cur.fetchone()
                    #print(start_time)
                    if start_time != None:
                        now_time = datetime.datetime.now().replace(microsecond=0)
                        duration = now_time - start_time[0]


                        embed=discord.Embed(title = "Session Data", description = f'Member: {member.mention}',color=discord.Color.blurple())
                        embed.set_author(name="monke bot", icon_url="https://cdn.discordapp.com/avatars/769067829403844648/ce370be164e7746872ae1e5e74af648d.webp?size=128")
                        embed.add_field(name="Session Time", value=f'{duration}', inline=False)
                        embed.add_field(name="Join Time", value=f'{start_time[0].strftime("%H:%M:%S - %b %d, %Y PST")}', inline=True)
                        await ctx.send(embed=embed)
                    else:
                        raise ValueError(f'{member.display_name} has never joined a voice channel - no data found.')
                else:
                    raise ValueError(f'{member.display_name} has never joined a voice channel - no data found.')
            else:
                raise ValueError(f'{member.display_name} is not connected to a voice channel.')
                    
        except Exception as ex:
            await ctx.send(f'Something went wrong: {ex}')
            con.rollback()
        finally:
            con.commit()
            cur.close()
            con.close()



def setup(client):
    client.add_cog(check_session_slash(client))

