import discord
import random
import asyncio
import psycopg2
from datetime import datetime
from psycopg2 import sql
from datetime import datetime
from discord.ext import commands   
from discord.ext.commands import has_role
from discord.utils import get
from misc import connect

class voice_db(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('voice db ready')

    @commands.Cog.listener('on_voice_state_update')
    async def detector(self, member, before, after):
        print(member.id, before.channel, after.channel)
        
        con = connect.connect()
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users (anon_id BIGSERIAL PRIMARY KEY, discord_id BIGINT NOT NULL, total_time INTERVAL)')
        cur.execute('SELECT discord_id FROM users WHERE discord_id = %s', (member.id,))
        id_exists = cur.fetchone()

        if before.channel == None and after.channel != None:
            if (id_exists is None):
                cur.execute('INSERT INTO users (discord_id) VALUES (%s)', (member.id, ))

            cur.execute('SELECT anon_id FROM users WHERE discord_id = %s', (member.id, ))
            a_id = cur.fetchone()[0]
            cur.execute(sql.SQL('CREATE TABLE IF NOT EXISTS {} (row_id BIGSERIAL PRIMARY KEY, start_time TIMESTAMP NOT NULL, end_time TIMESTAMP, duration INTERVAL)').format(sql.Identifier(f'user_{a_id}')))
            
            time = datetime.now()
            query = sql.SQL('INSERT INTO {table} (start_time) VALUES (%s)').format(table = sql.Identifier(f'user_{a_id}'))
            cur.execute(query, (time,))

        elif after.channel == None and before.channel != None: 
            cur.execute('SELECT anon_id FROM users WHERE discord_id = %s', (member.id, ))
            a_id = cur.fetchone()
            if a_id != None:
                a_id = a_id[0]
                query = sql.SQL('SELECT count(*) FROM {table}').format(table = sql.Identifier(f'user_{a_id}'))
                cur.execute(query)
                num = cur.fetchone()[0]
                # print(num)
                if num > 0:

                    query = sql.SQL('SELECT row_id, start_time, end_time FROM {table} ORDER BY row_id DESC LIMIT 1').format(table = sql.Identifier(f'user_{a_id}'))
                    cur.execute(query)

                    row_start = cur.fetchone()
                    if row_start[2] == None:
                        time = datetime.now()
                        query = sql.SQL('UPDATE {table} SET end_time = %s, duration = %s WHERE row_id = %s').format(table = sql.Identifier(f'user_{a_id}'))
                        cur.execute(query, (time, time - row_start[1], row_start[0]))
                        query = sql.SQL('SELECT SUM (duration) AS total FROM {table}').format(table = sql.Identifier(f'user_{a_id}'))
                        cur.execute(query)

                        total = cur.fetchone()
                        query = sql.SQL('UPDATE users SET total_time = %s WHERE anon_id = %s')
                        cur.execute(query, (total, a_id))

        con.commit()
        cur.close()
        con.close()

    
    


def setup(client):
    client.add_cog(voice_db(client))
