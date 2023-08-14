from pathlib import Path

import gspread

from modules.database import read
import modules.embeds as embeds

import gspread_asyncio
import asyncio
import discord
from google.oauth2.service_account import Credentials

ACC_PATH = f"{Path(__file__).parent.parent.parent}/settings/service_account.json"

AGCM = gspread.service_account(filename=Path(ACC_PATH))

async def get_formals(sheetname, user: discord.Member) -> discord.Embed:
    sh = None
    ws = None
    data = {}

    id = await read.get_id("instructor", user.id)
    if (id == None):
        return embeds.error_embed_1("User does not have a schedule set up!", "")

    agc = AGCM

    try:
        sh = agc.open(sheetname)
        ws = sh.get_worksheet(0)
    except gspread_asyncio.gspread.WorksheetNotFound:
        return embeds.error_embed_1(
            'Cannot find worksheet: "OFFICIAL"', 
            "Please create this worksheet in the google form!"
        )
    except Exception as exc:
        print(exc)
        return embeds.error_embed_1(
            "Could not interact with Google Sheets!",
            "Something went wrong!"
        )
  
    sel_row = ws.find(id[0])
    sel_row = ws.row_values(sel_row.row)

    key_row = ["ID", "Name", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for i in range(2, len(sel_row)):
        if (sel_row[i]) == None:
            break

        parsed = [x.strip().split(":", 1) for x in sel_row[i].split(",")]
        parsed = [[x[0], x[1].split("-")] for x in parsed]
        d = {}
        for y in parsed:
            d[y[0]] = {
                "start_time" : y[1][0],
                "end_time" :y[1][1]
            }

        data[key_row[i]] = d
    
    return embeds.formals_embed(user, id[0], data)

    



      





    pass
