from tortoise.models import Model
from tortoise.fields import (
    DatetimeField, IntField, CharField,
    ForeignKeyField, CASCADE,
    JSONField, TextField
)
from tortoise.transactions import in_transaction
import asyncpg

class Files(Model):
    name = CharField(max_length=128)
    content_type = CharField(max_length=128)
    path = CharField(max_length=256)
    created_at = DatetimeField(auto_now=True)

    class Meta:
        table = 'files'


class Documents(Model):
    type = CharField(max_length=128)
    file = ForeignKeyField('models.Files', related_name='documents', on_delete=CASCADE)

    created_at = DatetimeField(auto_now=True)

    class Meta:
        table = 'documents'


class Pages(Model):
    entities = JSONField()
    text = TextField()
    number = IntField()
    path = CharField(max_length=256)

    document = ForeignKeyField('models.Documents', related_name='pages', on_delete=CASCADE)

    created_at = DatetimeField(auto_now=True)

    @staticmethod
    async def create_index():
        async with in_transaction('default') as conn:
            await conn.execute_query(
                "create index if not exists idx_gin_text "
                "on pages "
                "using gin (to_tsvector('russian', text));"
            )

    @staticmethod
    async def search_text(query):
        async with in_transaction('default') as conn:
            sql_query = (
                "select * "
                "from ( "
                "   select distinct on (f.id) f.id, ts_rank(to_tsvector(text), plainto_tsquery($1)) as dist "
                "   from pages p "
                "       join documents d on d.id = p.document_id "
                "       join files f on f.id = d.file_id "
                "       where to_tsvector(text) @@ plainto_tsquery($2) "
                "   ) as itd "
                "order by dist desc;"
            )

            res = await conn.execute_query(sql_query, (query, query))

        return [dict(r)['id'] for r in res[1]]

    class Meta:
        table = 'pages'


