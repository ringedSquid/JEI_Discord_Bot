from modules.database import read, edit

import discord

from discord import SelectOption, ui

verify_embed = discord.Embed(
    title="Welcome to JEI!", 
    description="Select your role and fill out the form to verify!", 
    color=0xed333b,
    author="JEI "
)

class verify_view(discord.ui.View):
    type = None

    @discord.ui.select(
        placeholder = "select your role",
        options = [
            discord.SelectOption(label="Intern", value="intern"),
            discord.SelectOption(label="Instructor", value="instructor"),
            discord.SelectOption(label="Admin", value="admin")
        ]
    )

    async def select_type(self, interaction:discord.Interaction, select_item: discord.ui.Select):
        self.type = select_item.values[0]
        match self.type:
            case "intern":
                await interaction.response.send_modal(verify_modal_intern())
            case "instructor":
                await interaction.response.send_modal(verify_modal_instructor())
            case "admin":
                await interaction.response.send_modal(verify_modal_admin())


class verify_modal_admin(ui.Modal, title="verify"):
    name = ui.TextInput(
        label = "Full Name",
        style = discord.TextStyle.short,
        placeholder = "e.g John Doe",
        default = None,
        required = True,
        max_length = 100,
    )

    jei_id = ui.TextInput(
        label = "JEI ID",
        style = discord.TextStyle.short,
        placeholder = "",
        default = None,
        required = True,
        max_length = 7,
    )



class verify_modal_instructor(ui.Modal, title="verify"):
    name = ui.TextInput(
        label = "Full Name",
        style = discord.TextStyle.short,
        placeholder = "e.g John Doe",
        default = None,
        required = True,
        max_length = 100,
    )

    jei_id = ui.TextInput(
        label = "JEI ID",
        style = discord.TextStyle.short,
        placeholder = "",
        default = None,
        required = True,
        max_length = 6,
    )

class verify_modal_intern(ui.Modal, title="verify"):
    name = ui.TextInput(
        label = "Full Name",
        style = discord.TextStyle.short,
        placeholder = "e.g John Doe",
        default = None,
        required = True,
        max_length = 100,
    )

    syep_id = ui.TextInput(
        label = "SYEP ID",
        style = discord.TextStyle.short,
        placeholder = "1234567",
        default = None,
        required = True,
        max_length = 7,
    )

    async def on_submit(self, interaction: discord.Interaction):
        #Check if user exists
        if ((self.name == None) or (len(str(self.name).split(" ")) < 2) or self.syep_id == None):
            pass
        if (await read.discord_exists("intern", interaction.user.id) == False):
            data = {
                "rank" : "intern",
                "discord_id" : interaction.user.id,
                "f_name" : str(self.name).split(" ")[0],
                "l_name" : str(self.name).split(" ")[1],
                "syep_id" : str(self.syep_id)
            }
            if (await edit.add_user(data) == True):
                #function to send new interaction to data channel
                await interaction.response.send_message("Cool!")


