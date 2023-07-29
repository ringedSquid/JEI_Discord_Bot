import platform
import os

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


async def setup(bot):
    await bot.add_cog(Events(bot))
