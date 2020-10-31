from fastapi import APIRouter, Request

from app.database.models import Documents


router = APIRouter()


@router.get('/{id}')
async def get_document(id: int, request: Request):
    document = await Documents.get(id=id).prefetch_related('pages')
    base_url = str(request.base_url).rstrip('/')

    result = {
        'id': document.id,
        'type': document.type,
        'pages': [{
            'id': p.id,
            'url': f'{base_url}/v1/pages/{p.id}',
            'entities': p.entities,
            'page_num': p.number,
            'text': p.text
        } for p in document.pages]
    }

    return {'result': result}
