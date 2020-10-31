import requests
from nlogic.services import EntityRecognition

from settings.config import settings

er = EntityRecognition(base_url='https://dev.er.nlogic.ai')


def ask_image_manager(file_obj):
    r = requests.post(
        url=settings.IM_URL + '/v1/process',
        files={'file': file_obj},
        timeout=360
    )
    return r.json()


def ask_parser(im_data: dict):
    r = requests.post(
        url=settings.PARSER_URL + '/v1/process',
        json=im_data,
        timeout=360
    )
    return r.json()


def process_pipeline(file_obj):
    im_data = ask_image_manager(file_obj)
    result = ask_parser(im_data=im_data)
    return result
