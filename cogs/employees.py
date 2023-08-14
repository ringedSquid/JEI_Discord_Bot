#Any command meant to be run by employees
from modules.guild import roles
from modules.logs import files
import modules.forms as forms
import modules.embeds as embeds

import discord
from discord.ext import commands
from discord import app_commands

class Employees(commands.Cog, name="employees"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="verify", description="verify yourself!")
    async def verify(self, interaction: discord.Interaction):
        bot = self.bot
        await interaction.response.send_message(
            embed=embeds.inital_verify_embed(),
            ephemeral=True,
            view=forms.verify_view(bot.get_channel(bot.config["verify_channel"]), await roles.get_roles(interaction.guild), bot)
        )

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        self.bot.logger.error(error)
        files.stash_log()

async def setup(bot):
    await bot.add_cog(Employees(bot))
