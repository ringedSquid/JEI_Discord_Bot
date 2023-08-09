import platform
import os

from modules.database import read 
import modules.forms as forms

import discord
from discord.ext import commands
from discord.ext.commands import Context 
from discord import app_commands

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
            #await bot.tree.sync()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        bot = self.bot
        bot.usr_logger.info(f"{member.name} <@{member.id}> joined!")
        await member.send(view=forms.verify_view(bot.get_channel(1133458980530835508)))
        #await forms.verify_view().wait()

    @app_commands.command(name="verify_test", description="test verify")
    async def verify_test(self, interaction: discord.Interaction):
        bot = self.bot
        await interaction.response.send_message(view=forms.verify_view(bot.get_channel(1133458980530835508)))




    @commands.Cog.listener()
    async def on_member_remove(self, member):
        bot = self.bot
        bot.usr_logger.info(f"{member.name} <@{member.id}> left!")



async def setup(bot):
    await bot.add_cog(Events(bot))
