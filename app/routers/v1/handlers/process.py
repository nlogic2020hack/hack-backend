from uuid import uuid4
from pathlib import Path
from shutil import copyfileobj

from fastapi import (
    APIRouter, File, UploadFile
)
from tortoise.transactions import atomic
from nlogic.structures.image import load_from_file
from nlogic.logger import get_logger

from settings.config import FILES_DIR, PAGES_DIR
from app.database.models import Files, Pages, Documents
from utils.api import er, process_pipeline, ask_image_manager, ask_parser


router = APIRouter()
logger = get_logger(__name__)


@atomic()
async def save_file(file: UploadFile, content_type, file_obj):
    file_path = Path(FILES_DIR, str(uuid4()))
    with open(file_path, 'wb') as f:
        copyfileobj(file_obj, f)

    file_obj.seek(0)

    file_db = await Files.create(
        name=file.filename,
        content_type=content_type,
        path=file_path
    )

    return file_db, file_path


@atomic()
async def save_pages_and_documents(pages_objets: list, file_db, bucket_data):
    pages_to_insert = []
    numbers_to_pages_path = {}

    for i, page_obj in enumerate(pages_objets):
        page_path = Path(PAGES_DIR, str(uuid4()))
        page_obj.save(page_path)
        numbers_to_pages_path[i] = page_path.as_posix()

    for doc_id, doc_data in bucket_data['documents'].items():
        doc_obj = await Documents.create(
            type=doc_data['type'],
            file=file_db
        )

        for page_id in doc_data['page_ids']:
            page_data = bucket_data['pages'].get(page_id)
            im_data = bucket_data['image_manager'][page_id]
            page_num = im_data['page_num']
            pages_to_insert.append(Pages(
                entities=page_data['entities'] if page_data else {},
                text=im_data['text'],
                number=page_num,
                document=doc_obj,
                path=numbers_to_pages_path[page_num]
            ))

    await Pages.bulk_create(pages_to_insert)


@atomic()
@router.post('')
async def process(file: UploadFile = File(...)):
    content_type = file.content_type
    file_obj = file.file
    file_db, file_path = await save_file(file, content_type, file_obj)

    try:
        pages = load_from_file(file_path)

        bucket_data = process_pipeline(
            file_obj=file_obj
        )
        # r = er.run_sync_pipeline(
        #     pipeline='pravoru',
        #     file_obj=file_obj,
        #     timeout=600
        # )

        # bucket_data = r.json
        await save_pages_and_documents(
            pages_objets=pages,
            file_db=file_db,
            bucket_data=bucket_data
        )
    except Exception as e:
        logger.error(
            msg='ERROR',
            extra={
                'error': str(e)
            }
        )
        await file_db.delete()
        file_path.unlink()
        return {'result': 'failed'}

    return {'result': bucket_data}
