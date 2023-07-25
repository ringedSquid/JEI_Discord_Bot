import discord
import json
import time
import os
from discord.ext.commands import Bot

bot = None
CONFIG = {}

def init():
    #Check for config and open
    if (os.path.exists("settings/config.json") == False):
        return "NO_CONFIG"

    with open("settings/config.json", "r") as file:
        CONFIG = json.load(file)
        file.close()

    #Init bot
    bot = Bot {
        command_prefix=CONFIG["prefix"],
        intents = discord.intents.default()
    }

    bot.run(CONFIG["token"])











if (__name__ == "__main__"):
    init()


