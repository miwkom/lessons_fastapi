from typing import Annotated, Optional

from fastapi import Query, Depends, HTTPException, Request
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[Optional[int], Query(1, description="Номер страницы", ge=1)]
    per_page: Annotated[Optional[int], Query(None, description="Количество отелей на странице", ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Нет токена доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]
