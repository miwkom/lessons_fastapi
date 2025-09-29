from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.exceptions import (
    DataProcessingErrorsException,
    DataProcessingErrorsHTTPException,
)
from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    try:
        ImagesService().upload_image(file, background_tasks)
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
