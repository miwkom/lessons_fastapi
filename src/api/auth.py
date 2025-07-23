from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    try:
        if len(data.password) > 2:
            hashed_password = AuthService().hash_password(data.password)
        else:
            raise HTTPException(status_code=403, detail="Не правильный пароль")
        if len(data.email) < 1:
            raise HTTPException(status_code=403, detail="Не правильный email")
        email_confirmation = await db.users.get_one_or_none(email=data.email)
        if email_confirmation is None:
            new_user_data = UserAdd(
                email=data.email,
                hashed_password=hashed_password,
                first_name=data.first_name,
                last_name=data.last_name,
            )
        else:
            raise HTTPException(
                status_code=403, detail="Пользователь с таким email существует"
            )
        await db.users.add(new_user_data)
        await db.commit()
    except:  # noqa: E722
        raise HTTPException(status_code=403)
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserLogin,
    response: Response,
):
    try:
        user = await db.users.get_user_with_hashed_password(email=data.email)
    except Exception:
        raise HTTPException(
            status_code=403, detail="Пользователь с таким email не зарегистрирован"
        )
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Не правильный пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.get("/logout")
async def logout(
    response: Response,
):
    AuthService().logout_user(response)
    return {"status": "OK"}
