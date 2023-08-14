import json
import time
import os
import asyncio
import sys
import logging
from typing import Dict

from modules.logs import LoggingFormatter 

import discord
import aiosqlite
from discord.ext import commands
from discord.ext.commands import Bot

#dir the project is contained in
PATH = os.path.realpath(os.path.dirname(__file__))
LOG_PATH = f"{PATH}/etc/logs"
DEBUG = True

#initialize logs
def init_logs(log_path: str, filename: str, w_mode: str, name: str) -> logging.Logger:
    #init logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    #stdout
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LoggingFormatter())

    #to files
    file_handler = logging.FileHandler(
        filename = f"{LOG_PATH}/{filename}",
        encoding = "utf-8",
        mode = w_mode 
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
    if (os.path.exists(f"{PATH}/settings/config.json") == False):
        sys.exit("ERROR: Config file does not exist!")

    with open(f"{PATH}/settings/config.json", 'r') as file:
        config = json.load(file)
        file.close()

    return config 

#initialize the bot
def init_bot(config) -> Bot:
    #init intents
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    #init bot
    bot = Bot(
        command_prefix = config["prefix"],
        intents = intents,
        help_commmand = None,
    )
    
    return bot

#init sql database
async def init_db(bot) -> None:
    async with aiosqlite.connect(
        f"{PATH}/data/database.db"
    ) as db:
        with open(
            f"{PATH}/data/schema.sql"
        ) as file:
            await db.executescript(file.read())
        await db.commit()
    
    bot.logger.info("Database initalized!")

#load all extensions
async def load_cogs(bot) -> None:
    for file in os.listdir(f"{PATH}/cogs/"):
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

    logger = init_logs(LOG_PATH, "log0.log", 'w', "bot")
    usr_logger = init_logs(LOG_PATH, "usr_log0.log", 'a', "usr")
    verify_logger = init_logs(LOG_PATH, "verify_log0.log", 'a', "ver")
    
    #init bot
    bot = init_bot(config)
    bot.config = config
    bot.logger = logger
    bot.usr_logger = usr_logger
    bot.verify_logger = verify_logger
    bot.config = config
    
    @bot.command()
    async def sync(ctx: commands.Context):
        bot.tree.copy_global_to(guild=ctx.guild)
        await bot.tree.sync(guild=ctx.guild)
        await ctx.send(content = "YPYUPUPYUP")

    asyncio.run(load_cogs(bot))
    asyncio.run(init_db(bot))
    bot.run(config["token"])

    
if (__name__ == "__main__"):
    main()



