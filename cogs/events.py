import platform
import os

from modules.database import read, edit
from modules.guild import roles
import modules.forms as forms
import modules.embeds as embeds


import discord
from discord.ext import commands
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
        await member.send(
            embed=embeds.inital_verify_embed(),
            view=forms.verify_view(bot.get_channel(bot.verify_channel), await roles.get_roles(member.guild))
        )

    @app_commands.command(name="verify_test", description="test verify")
    async def verify_test(self, interaction: discord.Interaction):
        bot = self.bot
        await interaction.response.send_message(
            embed=embeds.inital_verify_embed(),
            ephemeral=True,
            view=forms.verify_view(bot.get_channel(bot.verify_channel), await roles.get_roles(interaction.guild))
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        bot = self.bot
        bot.usr_logger.info(f"{member.name} <@{member.id}> left!")
        await edit.del_user(member.id)


async def setup(bot):
    await bot.add_cog(Events(bot))
