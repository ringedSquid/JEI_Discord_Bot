import discord

from discord import ui

class verify_modal_instructor(ui.Modal, title="verify"):
    f_name = ui.TextInput(
        label = "First Name",
        style = discord.TextStyle.short,
        placeholder = "",
        default = None,
        required = True,
        max_length = 50,
    )

    l_name = ui.TextInput(
        label = "Last Name",
        style = discord.TextStyle.short,
        placeholder = "",
        default = None,
        required = True,
        max_length = 50,
    )

    age = ui.TextInput(
        label = "Age",
        style = discord.TextStyle.short,
        placeholder = "",
        default = None,
        required = True,
        max_length = 3,
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
    f_name = ui.TextInput(
        label = "First Name",
        style = discord.TextStyle.short,
        placeholder = "",
        default = None,
        required = True,
        max_length = 50,
    )

    l_name = ui.TextInput(
        label = "Last Name",
        style = discord.TextStyle.short,
        placeholder = "",
        default = None,
        required = True,
        max_length = 50,
    )

    age = ui.TextInput(
        label = "Age",
        style = discord.TextStyle.short,
        placeholder = "",
        default = None,
        required = True,
        max_length = 3,
    )

    jei_id = ui.TextInput(
        label = "SYEP ID",
        style = discord.TextStyle.short,
        placeholder = "",
        default = None,
        required = True,
        max_length = 6,
    )
