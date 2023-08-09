from typing import Dict, Union
from modules.database import read, edit
import modules.embeds as embeds

import discord

from discord import SelectOption, Thread, ui, user 
from discord.ext.commands import Bot

class verify_confirm_view(discord.ui.View):
    #this class will hold the user data and the message id so that
    #the embed can be edited
    def __init__(self, data: Dict, user: discord.User):
        super().__init__()
        self.data = data
        self.user = user


    @ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=embeds.success_embed_1(
                "Success!", 
                f"{self.data['f_name']} {self.data['l_name']} has been verified as {self.data['rank']}."
            )
        )

        await interaction.message.edit(
            content=None,
            view=None,
            embed=embeds.confirm_verify_success_embed(self.data, True, self.user, interaction.user)
        )
        
        self.stop()

    @ui.button(label="Reject", style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=embeds.error_embed_1(
                "Success!", 
                f"{self.data['f_name']} {self.data['l_name']} has been rejected!"
            )
        )

        await interaction.message.edit(
            content=None,
            view=None,
            embed=embeds.confirm_verify_success_embed(self.data, False, self.user, interaction.user)
        )
        
        self.stop()



class verify_view(discord.ui.View):
    def __init__(self, verify_channel: Union[discord.abc.GuildChannel, discord.Thread, discord.abc.PrivateChannel]):
        super().__init__()
        self.verify_channel = verify_channel
        self.type = None

    @ui.select(
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
                await interaction.response.send_modal(verify_modal_intern(self.verify_channel))
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
        max_length = 6,
        min_length = 6,
    )

    key = ui.TextInput(
        label = "Admin Password",
        style = discord.TextStyle.short,
        placeholder = "e.g $password@123",
        default = None,
        required = True,
        max_length = 20,
    )
    
    confirm_key = ui.TextInput(
        label = "Confirm Password",
        style = discord.TextStyle.short,
        placeholder = "e.g $password@123",
        default = None,
        required = True,
        max_length = 20,
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = str(self.name)
        jei_id = str(self.jei_id)
        key = str(self.key)
        confirm_key = str(self.confirm_key)

        #Check if user exists
        if (len(name.split(" ")) < 2):
            await interaction.response.send_message("BRUH!")

        #Check if passwords match
        if (key != confirm_key):
            await interaction.response.send_message("BRUH!")

        discord_exists = await read.discord_exists("intern", interaction.user.id)
        id_exists = await read.id_exists("intern", jei_id)

        if ((discord_exists == False) and (id_exists == False)):
            data = {
                "rank" : "intern",
                "discord_id" : interaction.user.id,
                "f_name" : name.split(" ")[0],
                "l_name" : name.split(" ")[1],
                "jei_id" : jei_id
            }




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
        min_length = 6,
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = str(self.name)
        jei_id = str(self.jei_id)
        #Check if user exists
        if (len(name.split(" ")) < 2):
            await interaction.response.send_message("BRUH!")

        discord_exists = await read.discord_exists("intern", interaction.user.id)
        id_exists = await read.id_exists("intern", jei_id)

        if ((discord_exists == False) and (id_exists == False)):
            data = {
                "rank" : "intern",
                "discord_id" : interaction.user.id,
                "f_name" : name.split(" ")[0],
                "l_name" : name.split(" ")[1],
                "jei_id" : jei_id
            }



class verify_modal_intern(ui.Modal, title="verify"):
    def __init__(self, verify_channel: Union[discord.abc.GuildChannel, discord.Thread, discord.abc.PrivateChannel]):
        super().__init__()
        self.verify_channel = verify_channel

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
        min_length = 7,
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = str(self.name)
        syep_id = str(self.syep_id)
        #Check if user exists
        if (len(name.split(" ")) < 2):
            await interaction.response.send_message("BRUH!")

        discord_exists = await read.discord_exists("intern", interaction.user.id)
        id_exists = await read.id_exists("intern", syep_id)

        if ((discord_exists == False) and (id_exists == False)):
            data = {
                "rank" : "intern",
                "discord_id" : interaction.user.id,
                "f_name" : name.split(" ")[0],
                "l_name" : name.split(" ")[1],
                "syep_id" : syep_id
            }

            embed = embeds.confirm_verify_embed(data, interaction.user)
            view = verify_confirm_view(data, interaction.user)
            await self.verify_channel.send(embed=embed, view=view)
            await interaction.response.send_message("Success!")




            

