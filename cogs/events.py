import platform
import os

from modules.database import read

import discord
from discord.ext import commands

class Events(commands.Cog, name="events"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        bot = self.bot
        bot.logger.info(f"Logged in as {self.bot.user.name}!")
        bot.logger.info(f"discord.py version: {discord.__version__}")
        bot.logger.info(f"python version: {platform.python_version()}")
        bot.logger.info(f"Running on: {platform.system()} {platform.release()}, {os.name}")
        #sybc slash commands
        if (bot.config["sync_commands_globally"] == True):
            bot.logger.info("Syncing commands globally...")
            await bot.tree.sync()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        bot = self.bot
        bot.usr_logger.info(f"{member.id} joined!")
        


async def setup(bot):
    await bot.add_cog(Events(bot))
