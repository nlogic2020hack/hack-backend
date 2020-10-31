from nlogic.fastapi.app import compile_routers

from .handlers import files, process, documents, pages

routers = [
    {'router': files.router, 'tags': ['files'], 'prefix': '/files', 'disable_check_headers': True},
    {'router': process.router, 'tags': ['process'], 'prefix': '/process', 'disable_check_headers': True},
    {'router': documents.router, 'tags': ['documents'], 'prefix': '/documents', 'disable_check_headers': True},
    {'router': pages.router, 'tags': ['documents'], 'prefix': '/pages', 'disable_check_headers': True},
]
compiled_routers = compile_routers(routers=routers, root_prefix='/v1')
