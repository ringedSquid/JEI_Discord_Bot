from typing import Dict, Union
from modules.database import read, edit
import modules.embeds as embeds

import discord

from discord import SelectOption, Thread, ui, user 
from discord.ext.commands import Bot

#buttons for admins to confirm
class verify_confirm_view(discord.ui.View):
    #this class will hold the user data and the message id so that
    #the embed can be edited
    def __init__(self, data: Dict, user: discord.Member, roles: Dict):
        super().__init__()
        self.roles = roles
        self.data = data
        self.user = user

    @ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await edit.add_user(self.data)
        self.user = interaction.guild.get_member(self.user.id)
        await self.user.add_roles(self.roles[f"{self.data['rank'].lower()}"])
        await self.user.send(embed=embeds.success_embed_1("Verification Approved!", "You can now access the server!"))
        
        await interaction.response.send_message(
            embed=embeds.success_embed_1(
                "Success!", 
                f"{self.data['f_name']} {self.data['l_name']} has been verified as {self.data['rank']}."
            ),
            ephemeral=True
        )

        await interaction.message.edit(
            content=None,
            view=None,
            embed=embeds.confirm_verify_success_embed(self.data, True, self.user, interaction.user)
        )
        
        self.stop()

    @ui.button(label="Reject", style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user = interaction.guild.get_member(self.user.id)

        await interaction.response.send_message(
            embed=embeds.success_embed_1(
                "Success!", 
                f"{self.data['f_name']} {self.data['l_name']} has been rejected!"
            ),
            ephemeral=True
        )

        await interaction.message.edit(
            content=None,
            view=None,
            embed=embeds.confirm_verify_success_embed(self.data, False, self.user, interaction.user)
        )
        
        self.stop()

#Select form for role select
class verify_view(discord.ui.View):
    def __init__(self, verify_channel: Union[discord.abc.GuildChannel, discord.Thread, discord.abc.PrivateChannel], roles: Dict):
        super().__init__()
        self.verify_channel = verify_channel
        self.roles = roles
        self.type = None

    @ui.select(
        placeholder = "select your role",
        options = [
            discord.SelectOption(label="Intern", value="intern"),
            discord.SelectOption(label="Volunteer", value="volunteer"),
            discord.SelectOption(label="Instructor", value="instructor"),
            discord.SelectOption(label="Admin", value="admin")
        ]
    )

    async def select_type(self, interaction:discord.Interaction, select_item: discord.ui.Select):
        self.type = select_item.values[0]
        match self.type:
            case "intern":
                await interaction.response.send_modal(verify_modal_syep(self.type, self.roles, self.verify_channel))
            case "volunteer":
                await interaction.response.send_modal(verify_modal_jei(self.type, self.roles, self.verify_channel))
            case "instructor":
                await interaction.response.send_modal(verify_modal_jei(self.type, self.roles, self.verify_channel))
            case "admin":
                await interaction.response.send_modal(verify_modal_admin(self.type, self.roles, self.verify_channel))

#form for admins
class verify_modal_admin(ui.Modal, title="verify"):
    def __init__(
            self, 
            type: str, roles: Dict,
            verify_channel: Union[discord.abc.GuildChannel, discord.Thread, discord.abc.PrivateChannel]
        ):
        super().__init__()
        self.verify_channel = verify_channel
        self.type = type
        self.roles = roles

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
        placeholder = "BSDJD0",
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
        discord_exists = await read.discord_exists("intern", interaction.user.id)
        id_exists = await read.id_exists("intern", jei_id)

        #Check if user exists
        if ((" " not in name.strip()) and (len(name.split(" ")) != 2)):
            embed = embeds.error_embed_1("Invalid Name Format!", "Please list your first and last name. e.g John Doe")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        #Check if passwords match
        elif (key != confirm_key):
            embed = embeds.error_embed_1("Passwords Do Not Match!", "Please make sure that your password entries match.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif (discord_exists == True):
            embed = embeds.error_embed_1("Discord User Already Exists!", "")
            await interaction.response.send_message(embed=embed)

        elif (id_exists == True):
            embed = embeds.error_embed_1("JEI ID Already Exists!", "")
            await interaction.response.send_message(embed=embed)


        elif ((discord_exists == False) and (id_exists == False)):
            data = {
                "rank" : self.type,
                "discord_id" : interaction.user.id,
                "f_name" : name.split(" ")[0],
                "l_name" : name.split(" ")[1],
                "id" : jei_id
            }

            embed = embeds.confirm_verify_embed(data, interaction.user)
            view = verify_confirm_view(data, interaction.user, self.roles)
            await self.verify_channel.send(content=f"<@&{self.roles['admin'].id}>", embed=embed, view=view)

            embed = embeds.success_embed_1("Submission Successful!", "Please wait for admins to process your submission.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        self.stop()

#Form for instructors
class verify_modal_jei(ui.Modal, title="verify"):
    def __init__(
            self, 
            type: str, roles: Dict,
            verify_channel: Union[discord.abc.GuildChannel, discord.Thread, discord.abc.PrivateChannel]
        ):
        super().__init__()
        self.verify_channel = verify_channel
        self.type = type
        self.roles = roles

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
        placeholder = "BSDJD0",
        default = None,
        required = True,
        max_length = 6,
        min_length = 6,
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = str(self.name)
        jei_id = str(self.jei_id)
        discord_exists = await read.discord_exists(self.type, interaction.user.id)
        id_exists = await read.id_exists(self.type, jei_id)

        #Check if user exists
        if ((" " not in name.strip()) and (len(name.split(" ")) != 2)):
            embed = embeds.error_embed_1("Invalid Name Format!", "Please list your first and last name. e.g John Doe")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif (discord_exists == True):
            embed = embeds.error_embed_1("Discord User Already Exists!", "")
            await interaction.response.send_message(embed=embed)

        elif (id_exists == True):
            embed = embeds.error_embed_1("JEI ID Already Exists!", "")
            await interaction.response.send_message(embed=embed)


        elif ((discord_exists == False) and (id_exists == False)):
            data = {
                "rank" : self.type,
                "discord_id" : interaction.user.id,
                "f_name" : name.split(" ")[0],
                "l_name" : name.split(" ")[1],
                "id" : jei_id
            }

            embed = embeds.confirm_verify_embed(data, interaction.user)
            view = verify_confirm_view(data, interaction.user, self.roles)
            await self.verify_channel.send(content=f"<@&{self.roles['admin'].id}>", embed=embed, view=view)

            embed = embeds.success_embed_1("Submission Successful!", "Please wait for admins to process your submission.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        self.stop()

#form for interns
class verify_modal_syep(ui.Modal, title="verify"):
    def __init__(
            self, 
            type: str,
            roles: Dict,
            verify_channel: Union[discord.abc.GuildChannel, discord.Thread, discord.abc.PrivateChannel], 
            ):
        super().__init__()
        self.verify_channel = verify_channel
        self.roles = roles
        self.type = type

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

        discord_exists = await read.discord_exists(self.type, interaction.user.id)
        id_exists = await read.id_exists(self.type, syep_id)

        #Check if user exists
        if ((" " not in name.strip()) and (len(name.split(" ")) != 2)):
            embed = embeds.error_embed_1("Invalid Name Format!", "Please list your first and last name. e.g John Doe")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif (discord_exists == True):
            embed = embeds.error_embed_1("Discord User Already Exists!", "")
            await interaction.response.send_message(embed=embed)

        elif (id_exists == True):
            embed = embeds.error_embed_1("SYEP ID Already Exists!", "")
            await interaction.response.send_message(embed=embed)

        elif ((discord_exists == False) and (id_exists == False)):
            data = {
                "rank" : "intern",
                "discord_id" : interaction.user.id,
                "f_name" : name.split(" ")[0],
                "l_name" : name.split(" ")[1],
                "id" : syep_id
            }

            #Send embed to admins
            embed = embeds.confirm_verify_embed(data, interaction.user)
            view = verify_confirm_view(data, interaction.user, self.roles)
            await self.verify_channel.send(content=f"<@&{self.roles['admin'].id}>", embed=embed, view=view)

            embed = embeds.success_embed_1("Submission Successful!", "Please wait for admins to process your submission.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        self.stop()






            

