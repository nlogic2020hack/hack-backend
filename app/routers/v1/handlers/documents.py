from fastapi import APIRouter

from app.database.models import Documents
from settings.config import settings

router = APIRouter()


@router.get('/{id}')
async def get_document(id: int):
    document = await Documents.get(id=id).prefetch_related('pages')

    result = {
        'id': document.id,
        'type': document.type,
        'pages': [{
            'id': p.id,
            'url': f'{settings.BACKEND_URL}/v1/pages/{p.id}',
            'entities': p.entities,
            'page_num': p.number,
            'text': p.text
        } for p in document.pages]
    }

    return {'result': result}
