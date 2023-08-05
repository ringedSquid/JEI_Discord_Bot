import os
from hashlib import sha256

import aiosqlite

DATA_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../data/database.db"

#Check if unique id already exists (interns, instructors, admins)
async def id_exists(type: str, id: str) -> bool:
    id = id.strip()
    table = None
    id_type = None

    match type:
        case "admin":
            table = "admins"
            id_type = "jei_id"
        case "intern":
            table = "interns"
            id_type = "syep_id"
        case "instructor":
            table = "instructors"
            id_type = "jei_id"
        case _:
            return False

    async with aiosqlite.connect(DATA_PATH) as db:
        async with db.execute(
            f"SELECT * FROM {table} WHERE {id_type}=?", (id) 
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None

#Check if discord user exists in specified table
async def discord_exists(type: str, discord_id: int) -> bool:
    table = None
    specialized = False
    verified = False

    match type:
        case "admin":
            table = "admins"
        case "intern":
            table = "interns"
        case "instructor":
            table = "instructors"
        case _:
            return False

    async with aiosqlite.connect(DATA_PATH) as db:
        async with db.execute(
            f"SELECT * FROM {table} WHERE discord_id=?", (discord_id) 
        ) as cursor:
            specialized = await cursor.fetchone()

        async with db.execute(
            f"SELECT * FROM verified WHERE discord_id=?", (discord_id) 
        ) as cursor:
            regular = await cursor.fetchone()

    return (verified and specialized)

#Check if password is correct for sepcified user
async def admin_check_psk(psk: str, discord_id: int) -> bool:
    psk = sha256(psk.strip().encode("utf-8")).hexdigest()

    async with aiosqlite.connect(DATA_PATH) as db:
        async with db.execute(
            f"SELECT * FROM admins WHERE discord_id=? AND key=?", (discord_id, psk) 
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None











