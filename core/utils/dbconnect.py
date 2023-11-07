from typing import List

import aiosqlite


class Request:


    async def create_table_triggersbot(self):
        async with aiosqlite.connect('triggerbot.db') as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS trigger_table
                 (name_trigger TEXT PRIMARY KEY NOT NULL,
                  value_trigger TEXT)''')
            await db.commit()


    async def create_table_users(self):
        async with aiosqlite.connect('users.db') as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS datausers
                 (user_id INT PRIMARY KEY NOT NULL,
                  user_name TEXT)''')
            await db.commit()


    async def add_user_id_name(self, user_id, user_name):
        async with aiosqlite.connect('users.db') as db:
            query = f"INSERT INTO datausers (user_id, user_name) VALUES ({user_id},'{user_name}')" \
                    f" ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
            await db.execute(query)
            await db.commit()


    async def add_trigger(self, name_trigger, value_trigger):
        async with aiosqlite.connect('triggerbot.db') as db:
            query = f"INSERT INTO trigger_table(name_trigger, value_trigger) VALUES ('{name_trigger}', '{value_trigger}')" \
                    f"ON CONFLICT (name_trigger)" \
                    f"DO UPDATE SET value_trigger=trigger_table.value_trigger || '\r\n' || excluded.value_trigger"
            # await db.execute("INSERT INTO trigger_table(name_trigger, value_trigger) VALUES (?, ?)", (name_trigger, value_trigger))
            await db.execute(query)
            await db.commit()


    async def get_triggers(self):
        async with aiosqlite.connect('triggerbot.db') as db:
            query = f'SELECT name_trigger FROM trigger_table ORDER BY name_trigger'
            result_list = await db.execute_fetchall(query)
            return '\r\n'.join([f"`#{result[0]}`" for result in result_list])


    async def get_values(self, name_trigger):
        async with aiosqlite.connect('triggerbot.db') as db:
            query = f"SELECT value_trigger FROM trigger_table WHERE name_trigger='{name_trigger}'"
            cursor = await db.execute(query)
            res = await cursor.fetchone()
            return res[0]

