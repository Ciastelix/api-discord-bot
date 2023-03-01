import asyncio
from app.bot import Bot
from os import environ
from dotenv import load_dotenv
from cogs.commands import Commands
from app.schemas import UserSchema
from fastapi import Depends, APIRouter
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from app.services import UserService

router = APIRouter()


@router.get("/")
async def root():
    return {"Hello": "World!"}


@router.post("/users", tags=["users"], name="Create User")
@inject
async def create_user(
    user: UserSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return {"users": user_service.add_user(user)}


@router.get("/users/{nick}", tags=["user"], name="Get User By Nick")
@inject
async def get_user(
    nick: str, user_service: UserService = Depends(Provide[Container.user_service])
):
    return {"users": user_service.get(nick)}


@router.get("/users", tags=["user"], name="Get All Users")
@inject
def get_list(
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return {"users": user_service.get_all()}


@router.get("/roles", tags=["roles"], name="Get All Roles")
async def get_roles():
    return {"roles": await bot.get_roles()}


@router.delete("/users", tags=["user"], name="Delete User")
@inject
@router.on_event("startup")
async def startup_event():
    global bot
    bot = Bot()
    load_dotenv()
    asyncio.create_task(bot.activate(environ.get("BOT_TOKEN")))
    bot = Commands(bot.get_bot())
    await asyncio.sleep(4)
