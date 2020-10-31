from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.database.models import Pages


router = APIRouter()


@router.get('/{id}', include_in_schema=False)
async def get_pages(id: int):
    page_db = await Pages.get(id=id)
    return FileResponse(page_db.path, media_type='image/png')
