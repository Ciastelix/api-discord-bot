import asyncio
from app.bot import Bot
from os import environ
from dotenv import load_dotenv
from cogs.commands import Commands
from app.schemas import UserSchema
from fastapi import Depends, APIRouter, HTTPException, status
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from app.services import UserService
from typing import Any
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post(
    "/users",
    tags=["user"],
    name="Create User",
    status_code=status.HTTP_201_CREATED,
    response_description="User created",
)
@inject
async def create_user(
    user: UserSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> Any:
    """
    Takes in a user object and adds it to the database.
    nick: str - used as a unique identifier
    group: str - used to determine the role in discord
    name: str - used to determine the name in discord
    """
    try:
        user = user_service.add_user(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"users": user}


@router.get(
    "/users/{nick}",
    tags=["user"],
    name="Get User By Nick",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_user(
    nick: str, user_service: UserService = Depends(Provide[Container.user_service])
) -> Any:
    user = UserSchema.from_orm(user_service.get(nick))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"users": user}


@router.get(
    "/users", tags=["user"], name="Get All New Users", status_code=status.HTTP_200_OK
)
@inject
def get_list(
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> Any:
    users = [UserSchema.from_orm(i) for i in user_service.get_all()]
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return {"users": users}


@router.get(
    "/roles", tags=["roles"], name="Get All Roles", status_code=status.HTTP_200_OK
)
async def get_roles() -> Any:
    roles = await bot.get_roles()
    if not roles:
        raise HTTPException(status_code=404, detail="No roles found")
    return {"roles": roles}


@router.get(
    "/dc/users",
    tags=["user"],
    name="Get All Discord Users",
    status_code=status.HTTP_200_OK,
)
async def get_all_users() -> Any:
    users = await bot.get_all_users()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return {"users": users}

@router.delete("/users",tags=["user"],name="Delete User",status_code=status.HTTP_200_OK)
async def delete_user(nick:str, user_service: UserService = Depends(Provide[Container.user_service]))->None:
    return user_service.delete_user(nick)
    

@inject
@router.on_event("startup")
async def startup_event():
    global bot
    bot = Bot()
    load_dotenv()
    asyncio.create_task(bot.activate(environ.get("BOT_TOKEN")))
    bot = Commands(bot.get_bot())
    await asyncio.sleep(4)
