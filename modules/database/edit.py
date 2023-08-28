import os
from typing import Dict, List, Optional
from pathlib import Path

import aiosqlite

DATA_PATH = f"{Path(__file__).parent.parent.parent}/data/database.db"

#Add a user, adds them to the verified then adds them to the specialized tables
#Data contains name, rank, discord id, syep or jei id
async def add_user(data: Dict)-> bool:
    insert_seq = ""
    insert_tup = ()
    default_tup = (
        data["discord_id"],
        data["f_name"],
        data["l_name"],
        data["rank"]
    )

    if (data["rank"] ==  "admin"):
        insert_seq = "admins(discord_id, f_name, l_name, id, key) VALUES (?, ?, ?, ?, ?)"
        insert_tup = (
            data["discord_id"],
            data["f_name"],
            data["l_name"],
            data["id"],
            data["key"],
        )

    else:
        insert_seq = f"{data['rank']}s(discord_id, f_name, l_name, id) VALUES (?, ?, ?, ?)"
        insert_tup = (
            data["discord_id"],
            data["f_name"],
            data["l_name"],
            data["id"],
        )

    async with aiosqlite.connect(DATA_PATH) as db:
        await db.execute(f"INSERT INTO {insert_seq}", insert_tup)
        await db.execute("INSERT INTO verified(discord_id, f_name, l_name, rank) VALUES (?, ?, ?, ?)", default_tup,) 
        await db.commit()
        return True

#delete a user
async def del_user(id: int) -> bool:
    #find groups user is a part of
    rank = None

    async with aiosqlite.connect(DATA_PATH) as db:
        async with(db.execute("SELECT rank FROM verified WHERE discord_id=?", (id,))) as cursor: 
            rank = await cursor.fetchone()
            if (rank == None): 
                return False

            rank = rank[0]
            
    async with aiosqlite.connect(DATA_PATH) as db:
        await db.execute("DELETE FROM verified WHERE discord_id=?", (id,))
        await db.execute(f"DELETE FROM {rank}s WHERE discord_id=?", (id,))
        await db.commit()
        return True

async def sync_users(discord_ids: List[int]) -> int:
    deleted_members = 0
    database_members = None
    async with aiosqlite.connect(DATA_PATH) as db:
        async with(db.execute("SELECT discord_id from VERIFIED")) as cursor:
            database_members = await cursor.fetchall()

    for member in database_members:
        if (int(member[0]) not in discord_ids):
            deleted_members += 1
            if (await del_user(member[0]) == False):
                return -1

    return deleted_members

            


