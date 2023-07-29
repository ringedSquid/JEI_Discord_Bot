import json
import time
import os
import asyncio
import sys
import logging
from typing import Dict


from modules.logs import LoggingFormatter 

import discord
from discord.ext.commands import Bot, Context

LOG_PATH = "etc/logs/"
CWD = os.getcwd()
DEBUG = True

#initialize logs
def init_logs(log_path) -> logging.Logger:
    #init logger
    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)

    #stdout
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LoggingFormatter())

    #to files
    file_handler = logging.FileHandler(
        filename = log_path + "log0.log",
        encoding = "utf-8",
        mode = 'w'
    )
    file_handler.setFormatter(LoggingFormatter())

    #add handlers
    logger.addHandler(file_handler)

    #only enable output to console in debug mode
    if (DEBUG == True): 
        logger.addHandler(console_handler)

    return logger

#Inits config and sets up bot
def init_config() -> Dict:
    config = {}
    #Check for config and open
    if (os.path.exists("settings/config.json") == False):
        sys.exit("ERROR: Config file does not exist!")

    with open("settings/config.json", "r") as file:
        config = json.load(file)
        file.close()

    return config 

#initialize the bot
def init_bot(config) -> Bot:
    #init bot
    bot = Bot(
        command_prefix = config["prefix"],
        intents = discord.Intents.default(),
        help_commmand = None,
    )
    
    return bot

#load all extensions
async def load_cogs(bot) -> None:
    for file in os.listdir("cogs/"):
        if (file.endswith(".py")):
            try:
                await bot.load_extension(f"cogs.{file[:-3]}")
                bot.logger.info(f"Loaded extension {file[:-3]}!") 
                
            except Exception as exc:
                bot.logger.error(f"Failed to load extension {file[:-3]}!\n{exc}")
        

def main():
    #load config file
    config = init_config()

    #init logging
    if (os.path.exists(LOG_PATH) == False):
        os.mkdir(LOG_PATH)

    logger = init_logs(LOG_PATH)
    
    #init bot
    bot = init_bot(config)
    bot.logger = logger
    bot.config = config

    asyncio.run(load_cogs(bot))
    bot.run(config["token"])

    
if (__name__ == "__main__"):
    main()



