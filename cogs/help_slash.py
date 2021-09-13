
import os, json, discord
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

class help_slash(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('help slash ready')

    
    @cog_ext.cog_slash (
        name='help', 
        description='Information about the bot',
        guild_ids=[GUILD_ID],
    )
    async def help(self, ctx: SlashContext):
        embed=discord.Embed(title="", description="Primary purpose of this bot is to create a database project using PostgreSQL - more information can be found [here](https://github.com/daniel-adam-ce/discord-bot).", color=discord.Color.blurple())
        embed.set_author(name="monke bot", url="https://github.com/daniel-adam-ce/discord-bot", icon_url="https://cdn.discordapp.com/avatars/769067829403844648/ce370be164e7746872ae1e5e74af648d.webp?size=128")
        embed.add_field(name="Commands", value="/purge - Deletes messages.\n/monkey - Show or add monkeys\n/voicedb - See voice channel data for the selected user (main command).", inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(help_slash(client))

