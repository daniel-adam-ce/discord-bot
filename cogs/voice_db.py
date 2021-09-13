
import datetime
from psycopg2 import sql
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
        
        
        con = connect.connect()
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users (anon_id BIGSERIAL PRIMARY KEY, discord_id BIGINT NOT NULL, total_time INTERVAL)')
        cur.execute('SELECT discord_id FROM users WHERE discord_id = %s', (member.id,))
        id_exists = cur.fetchone()

        if before.channel == None and after.channel != None:
            print(datetime.datetime.now().replace(microsecond=0), member.display_name, before.channel, after.channel)
            if (id_exists is None):
                cur.execute('INSERT INTO users (discord_id) VALUES (%s)', (member.id, ))

            cur.execute('SELECT anon_id FROM users WHERE discord_id = %s', (member.id, ))
            a_id = cur.fetchone()[0]
            cur.execute(sql.SQL('CREATE TABLE IF NOT EXISTS {} (row_id BIGSERIAL PRIMARY KEY, start_time TIMESTAMP NOT NULL, end_time TIMESTAMP, duration INTERVAL)').format(sql.Identifier(f'user_{a_id}')))
            
            query = sql.SQL('SELECT row_id, start_time, end_time FROM {table} ORDER BY row_id DESC LIMIT 1').format(table = sql.Identifier(f'user_{a_id}'))
            cur.execute(query)
            data = cur.fetchone()
            if data != None and data[0] != None and data[1] != None and data[2] == None:
                # print('yes', data)
                time = datetime.datetime.now().replace(microsecond=0)
                query = sql.SQL('UPDATE {table} SET start_time = %s WHERE row_id = %s').format(table = sql.Identifier(f'user_{a_id}'))
                cur.execute(query, (time, data[0]))
            else:
                time = datetime.datetime.now().replace(microsecond=0)
                query = sql.SQL('INSERT INTO {table} (start_time) VALUES (%s)').format(table = sql.Identifier(f'user_{a_id}'))
                cur.execute(query, (time,))

        elif after.channel == None and before.channel != None: 
            print(datetime.datetime.now().replace(microsecond=0), member.display_name, before.channel, after.channel)
            cur.execute('SELECT anon_id FROM users WHERE discord_id = %s', (member.id, ))
            a_id = cur.fetchone()
            if a_id != None:
                a_id = a_id[0]
                query = sql.SQL('SELECT count(*) FROM {table}').format(table = sql.Identifier(f'user_{a_id}'))
                cur.execute(query)
                num = cur.fetchone()
                # print(num)
                if num != None:
                    query = sql.SQL('SELECT row_id, start_time, end_time FROM {table} ORDER BY row_id DESC LIMIT 1').format(table = sql.Identifier(f'user_{a_id}'))
                    cur.execute(query)

                    row_start = cur.fetchone()
                    if row_start[2] == None:
                        time = datetime.datetime.now().replace(microsecond=0)
                        query = sql.SQL('UPDATE {table} SET end_time = %s, duration = %s WHERE row_id = %s').format(table = sql.Identifier(f'user_{a_id}'))
                        duration = time - row_start[1]
                        duration = duration - datetime.timedelta(microseconds=duration.microseconds)
                        cur.execute(query, (time, duration, row_start[0]))
                        query = sql.SQL('SELECT SUM (duration) AS total FROM {table}').format(table = sql.Identifier(f'user_{a_id}'))
                        cur.execute(query)

                        total = cur.fetchone()[0]

                        # print(type(total), total)
                        total = total - datetime.timedelta(microseconds=total.microseconds)
                        query = sql.SQL('UPDATE users SET total_time = %s WHERE anon_id = %s')
                        cur.execute(query, (total, a_id))

        con.commit()
        cur.close()
        con.close()

    
    


def setup(client):
    client.add_cog(voice_db(client))
