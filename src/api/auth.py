from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    DataProcessingErrorsHTTPException,
    DataProcessingErrorsException,
    UserNotFoundHTTPException,
    UserNotFoundException,
    UnauthorizedHTTPException,
    UnauthorizedException,
)
from src.schemas.users import UserRequestAdd, UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    try:
        await AuthService(db).register_user(data)
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserLogin,
    response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data, response)
    except UserNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    except UnauthorizedException as ex:
        raise UnauthorizedHTTPException from ex
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    try:
        user = await AuthService(db).get_self(user_id)
    except UserNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    return user


@router.get("/logout")
async def logout(
    response: Response,
):
    try:
        await AuthService().logout_user(response)
    except UserNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    return {"status": "OK"}
