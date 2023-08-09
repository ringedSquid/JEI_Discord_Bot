import os
from typing import Dict
from pathlib import Path

import aiosqlite

DATA_PATH = f"{Path(__file__).parent.parent.parent}/data/database.db"

#Add a user, adds them to the verified then adds them to the specialized tables
#Data contains name, rank, discord id, syep or jei id
async def add_user(data: Dict)-> bool:
#{'rank': 'intern', 'discord_id': 454739909295734804, 'f_name': 'Jofn', 'l_name': 'wdawd', 'syep_id': '1234515'}

    print(data)
    insert_seq = ""
    insert_tup = ()
    default_tup = (
        data["discord_id"],
        data["f_name"],
        data["l_name"],
        data["rank"]
    )

    match data["rank"]:
        #key will be hashed already
        case "admin":
            insert_seq = "admins(discord_id, f_name, l_name, jei_id, key) VALUES (?, ?, ?, ?, ?)"
            insert_tup = (
                data["discord_id"],
                data["f_name"],
                data["l_name"],
                data["jei_id"],
                data["key"],
            )
        case "intern":
            insert_seq = "interns(discord_id, f_name, l_name, syep_id) VALUES (?, ?, ?, ?)"
            insert_tup = (
                data["discord_id"],
                data["f_name"],
                data["l_name"],
                data["syep_id"],
            )
        case "instructor":
            insert_seq = "interns(discord_id, f_name, l_name, jei_id) VALUES (?, ?, ?, ?)"
            insert_tup = (
                data["discord_id"],
                data["f_name"],
                data["l_name"],
                data["jei_id"],
            )
        case _:
            return False

    async with aiosqlite.connect(DATA_PATH) as db:
        await db.execute(f"INSERT INTO {insert_seq}", insert_tup)
        await db.execute("INSERT INTO verified(discord_id, f_name, l_name, rank) VALUES (?, ?, ?, ?)", default_tup,) 
        await db.commit()
        return True

#delete a user
async def del_user(id: int)-> bool:
    #find groups user is a part of
    rank = None
    table = None

    async with aiosqlite.connect(DATA_PATH) as db:
        async with(db.execute("SELECT rank FROM verified WHERE discord_id=?", (id,))) as cursor: 
            rank = await cursor.fetchone()
            if (rank == None): 
                return False

            rank = rank[0]
            
    match rank:
        case "admin":
            table = "admins"
        case "intern":
            table = "interns"
        case "instructor":
            table = "instructors"
        case _:
            return False
    
    async with aiosqlite.connect(DATA_PATH) as db:
        await db.execute(f"DELETE FROM verified, {table} WHERE discord_id=?", (id,))
        await db.commit()
        return True





