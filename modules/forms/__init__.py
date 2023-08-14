from os import walk
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
    def __init__(self, data: Dict, user: discord.Member, roles: Dict, bot: Bot):
        super().__init__()
        self.roles = roles
        self.data = data
        self.user = user
        self.bot = bot

    @ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (interaction.user.get_role(self.roles["admin"].id) != None):
            user = interaction.guild.get_member(self.user.id)
            data = self.data

            await edit.add_user(self.data)
            self.bot.verify_logger.info(
                f"{user.name} ({data['f_name']} {data['l_name']}) has been verified as {data['rank']} by {interaction.user}"
            )
            await user.add_roles(self.roles[f"{data['rank'].lower()}"])
            await user.edit(nick=f"{data['f_name']} {data['l_name']}")
            await user.send(embed=embeds.success_embed_1("Verification Approved!", "You can now access the server!"))
            
            await interaction.response.send_message(
                embed=embeds.success_embed_1(
                    "Success!", 
                    f"{data['f_name']} {data['l_name']} has been verified as {data['rank']}."
                ),
                ephemeral=True
            )

            await interaction.message.edit(
                content=None,
                view=None,
                embed=embeds.confirm_verify_success_embed(data, True, user, interaction.user)
            )

            self.stop()
            
        else:
            await interaction.response.send_message(
                embed=embeds.error_embed_1(
                    "Invalid Permissions!", 
                    "You must be an admin to process this query."
                ),
                ephemeral=True
            )
        

    @ui.button(label="Reject", style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (interaction.user.get_role(self.roles["admin"].id) != None):
            user = interaction.guild.get_member(user.id)
            data = self.data
            self.bot.verify_logger.info(
                f"{user.name} ({data['f_name']} {data['l_name']}) has been rejected from {data['rank']} by {interaction.user}"
            )
            await interaction.response.send_message(
                embed=embeds.success_embed_1(
                    "Success!", 
                    f"{data['f_name']} {data['l_name']} has been rejected!"
                ),
                ephemeral=True
            )

            await interaction.message.edit(
                content=None,
                view=None,
                embed=embeds.confirm_verify_success_embed(data, False, user, interaction.user)
            )

            self.stop()

        else:
            await interaction.response.send_message(
                embed=embeds.error_embed_1(
                    "Invalid Permissions!", 
                    "You must be an admin to process this query."
                ),
                ephemeral=True
            )
        
#Select form for role select
class verify_view(discord.ui.View):
    def __init__(
            self, 
            verify_channel: Union[discord.abc.GuildChannel, 
            discord.Thread, discord.abc.PrivateChannel], 
            roles: Dict, bot: Bot
        ):
        super().__init__()
        self.verify_channel = verify_channel
        self.roles = roles
        self.type = None
        self.bot = bot

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
                await interaction.response.send_modal(verify_modal_syep(self.type, self.roles, self.verify_channel, self.bot))
            case "volunteer":
                await interaction.response.send_modal(verify_modal_jei(self.type, self.roles, self.verify_channel, self.bot))
            case "instructor":
                await interaction.response.send_modal(verify_modal_jei(self.type, self.roles, self.verify_channel, self.bot))
            case "admin":
                await interaction.response.send_modal(verify_modal_admin(self.type, self.roles, self.verify_channel, self.bot))

#form for admins
class verify_modal_admin(ui.Modal, title="verify"):
    def __init__(
            self, 
            type: str, roles: Dict,
            verify_channel: Union[discord.abc.GuildChannel, discord.Thread, discord.abc.PrivateChannel],
            bot: Bot
        ):
        super().__init__()
        self.verify_channel = verify_channel
        self.type = type
        self.roles = roles
        self.bot = bot

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
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif (id_exists == True):
            embed = embeds.error_embed_1("JEI ID Already Exists!", "")
            await interaction.response.send_message(embed=embed, ephemeral=True)


        elif ((discord_exists == False) and (id_exists == False)):
            data = {
                "rank" : self.type,
                "discord_id" : interaction.user.id,
                "f_name" : name.split(" ")[0],
                "l_name" : name.split(" ")[1],
                "id" : jei_id
            }

            embed = embeds.confirm_verify_embed(data, interaction.user)
            view = verify_confirm_view(data, interaction.user, self.roles, self.bot)
            await self.verify_channel.send(content=f"<@&{self.roles['admin'].id}>", embed=embed, view=view)

            embed = embeds.success_embed_1("Submission Successful!", "Please wait for admins to process your submission.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        self.stop()

#Form for instructors
class verify_modal_jei(ui.Modal, title="verify"):
    def __init__(
            self, 
            type: str, roles: Dict,
            verify_channel: Union[discord.abc.GuildChannel, discord.Thread, discord.abc.PrivateChannel],
            bot: Bot
        ):
        super().__init__()
        self.verify_channel = verify_channel
        self.type = type
        self.roles = roles
        self.bot = bot

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
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif (id_exists == True):
            embed = embeds.error_embed_1("JEI ID Already Exists!", "")
            await interaction.response.send_message(embed=embed, ephemeral=True)


        elif ((discord_exists == False) and (id_exists == False)):
            data = {
                "rank" : self.type,
                "discord_id" : interaction.user.id,
                "f_name" : name.split(" ")[0],
                "l_name" : name.split(" ")[1],
                "id" : jei_id
            }

            embed = embeds.confirm_verify_embed(data, interaction.user)
            view = verify_confirm_view(data, interaction.user, self.roles, self.bot)
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
            bot: Bot
            ):
        super().__init__()
        self.verify_channel = verify_channel
        self.roles = roles
        self.type = type
        self.bot = bot

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
        
        elif (syep_id.isdigit() == False):
            embed = embeds.error_embed_1("Invalid SYEP ID!", "")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif (discord_exists == True):
            embed = embeds.error_embed_1("Discord User Already Exists!", "")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif (id_exists == True):
            embed = embeds.error_embed_1("SYEP ID Already Exists!", "")
            await interaction.response.send_message(embed=embed, ephemeral=True)

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
            view = verify_confirm_view(data, interaction.user, self.roles, self.bot)
            await self.verify_channel.send(content=f"<@&{self.roles['admin'].id}>", embed=embed, view=view)

            embed = embeds.success_embed_1("Submission Successful!", "Please wait for admins to process your submission.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        self.stop()
