import os
from hashlib import sha256
from pathlib import Path

import aiosqlite

DATA_PATH = f"{Path(__file__).parent.parent.parent}/data/database.db"

#Check if unique id already exists (interns, instructors, admins)
async def id_exists(type: str, id: str) -> bool:
    id = id.strip()

    async with aiosqlite.connect(DATA_PATH) as db:
        async with db.execute(
            f"SELECT * FROM {type}s WHERE id=?", (id,) 
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None

#Check if discord user exists in specified table
async def discord_exists(type: str, discord_id: int) -> bool:
    specialized = True 
    verified = False

    async with aiosqlite.connect(DATA_PATH) as db:
        if (type != ""):
            specialized = False
            async with db.execute(
                f"SELECT * FROM {type}s WHERE discord_id=?", (discord_id,) 
            ) as cursor:
                specialized = await cursor.fetchone()
            
        async with db.execute(
            f"SELECT * FROM verified WHERE discord_id=?", (discord_id,) 
        ) as cursor:
            verified = await cursor.fetchone()

    return ((verified != None) and (specialized != None))

#Check if password is correct for sepcified user
async def admin_check_psk(psk: str, discord_id: int) -> bool:
    psk = sha256(psk.strip().encode("utf-8")).hexdigest()

    async with aiosqlite.connect(DATA_PATH) as db:
        async with db.execute(
            f"SELECT * FROM admins WHERE discord_id=? AND key=?", (discord_id, psk) 
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None











