import platform
import os

from modules.database import read, edit
from modules.guild import roles
from modules.logs import files
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
        bot.logger.info("Syncing users to database")

        #Sync members to database
        member_ids = []
        members = bot.get_guild(bot.guild_id).members
        for i in range(len(members)):
            member_ids.append(members[i].id)

        count = await edit.sync_users(member_ids)
        if (count > -1):
            bot.logger.info(f"Syncing users successful! {count} users removed from database!")
        else:
            bot.logger.error("Syncing users failed!")

        #sync slash commands
        if (bot.config["sync_commands_globally"] == True):
            bot.logger.info("Syncing commands globally...")
            #await bot.tree.sync()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        bot = self.bot
        bot.usr_logger.info(f"{member.name} <@{member.id}> joined!")
        await member.send(
            embed=embeds.inital_verify_embed(),
            view=forms.verify_view(bot.get_channel(bot.verify_channel), await roles.get_roles(member.guild), bot)
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        bot = self.bot
        bot.usr_logger.info(f"{member.name} <@{member.id}> left!")
        if (await read.discord_exists("", member.id) == True):
            await edit.del_user(member.id)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        self.bot.logger.error(error)
        files.stash_log()


async def setup(bot):
    await bot.add_cog(Events(bot))
