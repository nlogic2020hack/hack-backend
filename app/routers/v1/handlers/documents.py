from fastapi import APIRouter

from app.database.models import Documents
from settings.config import settings

router = APIRouter()


DOCTYPES = {
    'technical_passport': 'Технический паспорт',
    'contract': 'Договор аренды',
    'operation_start_permission': 'Разрешение на ввод в эксплуатацию',
    'construction_permission': 'Разрешение на строительство',
    'AGR_certificate': 'Свидетельство AГР'
}


@router.get('/{id}')
async def get_document(id: int):
    document = await Documents.get(id=id).prefetch_related('pages')

    result = {
        'id': document.id,
        'type': DOCTYPES.get(document.type, document.type),
        'pages': [{
            'id': p.id,
            'url': f'{settings.BACKEND_URL}/v1/pages/{p.id}',
            'entities': p.entities,
            'page_num': p.number,
            'text': p.text
        } for p in document.pages]
    }

    return {'result': result}
