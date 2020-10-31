from fastapi import APIRouter

from app.database.models import Files, Pages


router = APIRouter()


DOCTYPES = {
    'technical_passport': 'Технический паспорт',
    'contract': 'Договор аренды',
    'operation_start_permission': 'Разрешение на ввод в эксплуатацию',
    'construction_permission': 'Разрешение на строительство',
    'AGR_certificate': 'Свидетельство AГР'
}


def format_files(files):
    return [{
        'id': f.id,
        'name': f.name,
        'date': f.created_at.strftime("%m-%d-%Y, %H:%M:%S"),
        'documents': [{
            'id': d.id,
            'type': DOCTYPES.get(d.type, d.type),
        } for d in f.documents]
    } for f in files]


@router.get('')
async def get_files():
    files = await Files.all().prefetch_related('documents').order_by('-created_at')
    result = format_files(files)
    return {'result': result}


@router.get('/search/{query}')
async def get_files(query: str):
    res = await Pages.search_text(query=query)
    files = await Files.filter(id__in=res).prefetch_related('documents')
    result = format_files(files)
    return {'result': result}
