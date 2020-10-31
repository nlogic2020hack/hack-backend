from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.database.models import Pages


router = APIRouter()


@router.get('/{id}')
async def get_files(id: int):
    page_db = await Pages.get(id=id)
    return FileResponse(page_db.path, media_type='image/png')
