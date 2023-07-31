import os

import aiosqlite

DATA_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../data/database.db"

#Check if user already exists
async def is_existing(f_name: str, l_name: str) -> bool:
    f_name = f_name.strip()
    l_name = l_name.strip()

    async with aiosqlite.connect(DATA_PATH) as db:
        async with db.execute(
            "SELECT * FROM verified WHERE f_name=? AND l_name=?", (f_name, l_name)
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None





