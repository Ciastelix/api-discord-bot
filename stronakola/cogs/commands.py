import discord
from discord.ext import commands
from discord.ext.audiorec import NativeVoiceClient
from discord.member import Member
from discord.ext import commands, tasks
from discord.user import User
from app.speachtotext import SpeachToText
import datetime as dt
from dotenv import load_dotenv
import asyncio
from os import environ
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from app.services import UserService
from json import dumps, loads


class Commands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord!")
        self.meeting_noti.start()

    @inject
    @commands.Cog.listener()
    async def on_member_join(
        self,
        member: Member,
        user_service: UserService = Depends(Provide[Container.user_service]),
    ):
        load_dotenv()
        nick = f"{member.display_name}#{member.discriminator}"
        usr = user_service.get(nick)
        if not usr:
            await self.send_message(
                member.id, f"Zarejestruj sie na " + environ.get("PAGE_URL")
            )
            await member.kick()
        else:
            guild = await self.bot.fetch_guild(environ.get("GUILD"))
            role = discord.utils.get(
                guild.roles,
                name=usr.group,
            )
            self.bot.add_roles(member, role)
            await member.edit(nick=usr.name)
            user_service.delete(usr.nick)

    async def send_message(self, user_id: int, message: str) -> User | None:
        if await self.if_exists(user_id):
            user = await self.bot.fetch_user(user_id)
            await user.send(message)
            return user
        return None

    async def if_exists(self, user_id: int) -> bool:
        try:
            await self.bot.fetch_user(user_id)
            return True
        except discord.errors.NotFound:
            return False

    async def get_all_users(self) -> list[list[dict[str, str] | dict[str, list[str]]]]:
        load_dotenv()
        guild = await self.bot.fetch_guild(environ.get("GUILD"))
        _users: list[Member] = [
            i async for i in guild.fetch_members(limit=None) if i.nick
        ]
        users: list[list[list[str] | str]] = []
        for i in _users:
            usr = await guild.fetch_member(i.id)
            if usr.nick:
                roles = [i.name for i in usr.roles if i.name != "@everyone"]
                users.append(loads(dumps({"name": usr.nick, "roles": roles})))

        return users

    @tasks.loop(hours=168)
    async def meeting_noti(self):
        load_dotenv()
        message_channel = self.bot.get_channel(environ.get("MAIN_CHANNEL"))
        await message_channel.send("@here zapraszam na spotkanie")

    @meeting_noti.before_loop
    async def before_meeting(self):
        for _ in range(60 * 60 * 24 * 7):
            if dt.datetime.now().hour == 10 + 12:
                return
            await asyncio.sleep(1)

    @commands.command()
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel")
        else:
            channel = ctx.author.voice.channel
            await channel.connect(cls=NativeVoiceClient)

    @commands.command()
    async def rec(self, ctx):
        ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
        embedVar = discord.Embed(
            title="Started the Recording!",
            description="use !stop to stop!",
            color=0x546E7A,
        )
        await ctx.send(embed=embedVar)

    @rec.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(cls=NativeVoiceClient)
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command()
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client.is_recording():
            return
        await ctx.send(f"Stopping the Recording")

        wav_bytes = await ctx.voice_client.stop_record()

        with open("meeting.wav", "wb") as f:
            f.write(wav_bytes)
        await ctx.voice_client.disconnect()
        is_generated = SpeachToText().generate()
        if is_generated:
            with open("meeting.txt") as f:
                await ctx.send(f.read())

        else:
            await ctx.send("Error with Google API")

    async def get_roles(self) -> list[str]:
        return [
            i.name
            for i in (await self.bot.fetch_guild(environ.get("GUILD"))).roles
            if i.name != "@everyone" and i.name != "new-app"  # bot's name
        ]


def setup(bot):
    bot.add_cog(Commands(bot))
