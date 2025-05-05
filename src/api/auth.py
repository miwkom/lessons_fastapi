from fastapi import APIRouter, HTTPException, Response, Request

from src.DB import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post('/register')
async def register_user(
        data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email,
                            hashed_password=hashed_password,
                            first_name=data.first_name,
                            last_name=data.last_name,
                            )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}


@router.post('/login')
async def login_user(
        data: UserLogin,
        response: Response
):
    async with async_session_maker() as session:
        try:
            user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверен")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get('/verify_cookie')
async def verify_cookie(
        request: Request
):
    cookie = request.cookies.get("access_token")
    return {"cookie": f"{cookie or None}"}
