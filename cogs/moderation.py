from modules.database import read, edit
import modules.embeds as embeds

import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Moderation(bot))
