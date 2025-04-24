from typing import Annotated, Optional

from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[Optional[int], Query(1, description="Номер страницы", ge=1)]
    per_page: Annotated[Optional[int], Query(None, description="Количество отелей на странице", ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]
