import discord
from os import listdir
from discord.ext import commands
from typing import Awaitable


class Bot:
    bot: commands.Bot

    def __init__(self, prefix="!") -> None:
        self.bot = commands.Bot(command_prefix=prefix, intents=self.get_intents())

    def load(self) -> None:
        for filename in listdir("./cogs"):
            if filename.endswith(".py"):
                self.bot.load_extension(f"cogs.{filename[:-3]}")

    def get_intents(self) -> discord.Intents:
        intents = discord.Intents.default()
        intents.members = True
        intents.guilds = True
        intents.messages = True
        return intents

    def activate(self, token) -> Awaitable[None]:
        self.load()
        return self.bot.start(token)

    def get_bot(self) -> commands.Bot:
        return self.bot
