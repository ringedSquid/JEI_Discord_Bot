from typing import Dict

import discord

async def get_roles(guild: discord.Guild) -> Dict:
    roles = await guild.fetch_roles()
    roledict = {}
    for role in roles:
        roledict[role.name.lower()] = role

    return roledict

