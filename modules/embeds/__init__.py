import datetime
from typing import Dict, Optional, Union

import discord
from discord import Embed, user

def success_embed_1(heading: str, message: str) -> Embed:
    embed = Embed(
        title = heading,
        description = message,
        color = 0x33d17a,
    )

    embed.set_author(name="JEI Bot")
    embed.set_thumbnail(url="https://i.kym-cdn.com/photos/images/original/001/914/058/f9d")
    return embed

def error_embed_1(heading: str, message: str) -> Embed:
    embed = Embed(
        title = heading,
        description = message,
        color = 0xe01b24 
    )

    embed.set_author(name="JEI Bot")
    embed.set_thumbnail(url="https://i.kym-cdn.com/photos/images/original/001/914/058/f9d")
    return embed

def confirm_verify_embed(data: Dict, user: discord.User) -> Embed:
    id_type = None
    f_type = None
    color = 0x00 

    match data["rank"]:
        case "intern":
            id_type = "SYEP ID"
            f_type = "Intern"
            color = 0xf6d32d

        case "instructor":
            id_type = "JEI ID"
            f_type = "Instructor"
            color = 0x62a0ea

        case "admin":
            id_type = "JEI ID"
            f_type = "Admin"
            color = 0x00000

            
    embed = Embed(
        title = f"{data['f_name']} {data['l_name']}",
        description = f"{f_type}",
        color = color,
        timestamp = datetime.datetime.utcnow(),
    )

    embed.set_author(name="Verify User")
    embed.set_thumbnail(url=user.avatar)
    embed.add_field(name=id_type, value=id, inline=True)
    embed.add_field(name="Discord ID", value=str(user.id), inline=True)

    return embed

def confirm_verify_success_embed(data: Dict, result: bool, user: Union[discord.User, discord.Member], admin: Union[discord.User, discord.Member]):
    id_type = None
    f_type = None
    color = 0x00 
    f_result = None

    match data["rank"]:
        case "intern":
            id_type = "SYEP ID"
            f_type = "Intern"

        case "instructor":
            id_type = "JEI ID"
            f_type = "Instructor"

        case "admin":
            id_type = "JEI ID"
            f_type = "Admin"

    if (result == True):
        color = 0x33d17a
        f_result = "Accepted"
    else:
        color = 0xe01b24 
        f_result = "Rejected"

            
    embed = Embed(
        title = f"{data['f_name']} {data['l_name']} {f_result}!",
        description = f"{f_type}",
        color = color,
        timestamp = datetime.datetime.utcnow(),
    )

    embed.set_author(name="Verify User")
    embed.set_thumbnail(url=user.avatar)
    embed.add_field(name=id_type, value=data["syep_id"], inline=True)
    embed.add_field(name="Discord ID", value=user.id, inline=True)
    embed.add_field(name="\u200B", value="\u200B")
    embed.add_field(name="Processed By", value=str(admin.name))

    return embed

