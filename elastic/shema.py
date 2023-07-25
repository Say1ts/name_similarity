from enum import Enum
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel
from format.parser import *


class Filter(Enum):
    FUZZY = 'fuzzy'
    NGRAM = 'ngram'
    PHONETIC = 'phonetic'
    NGRAM_AND_PHONETIC = 'ngram_and_phonetic'
    KEYWORD_NAME = 'keyword_name'


class RecordType(Enum):
    BRAND_NAME = 'brand_name'
    OTHER_NAME = 'other_name'
    LEGAL_NAME = 'legal_name'
    SITE = 'site'
    INSTAGRAM = 'instagram'
    EMAIL = 'email'
    TELEGRAM = 'telegram'
    VK = 'vk'
    FACEBOOK = 'facebook'
    YOUTUBE = 'youtube'


class RecordRequest(BaseModel):
    name: str
    name_type: Optional[RecordType]


convertor_dict = {
    'brand_name': {'name': None, 'searchable': None},
    'other_name': {'name': None, 'searchable': None},
    'legal_name': {'name': None, 'searchable': from_legal},
    'site': {'name': to_domains, 'searchable': to_main_domains},
    'email': {'name': to_domains, 'searchable': from_email},
    'instagram': {'name': from_instagram, 'searchable': from_instagram},
    'telegram': {'name': from_telegram, 'searchable': from_telegram},
    'vk': {'name': from_vk, 'searchable': from_vk},
    'facebook': {'name': from_facebook, 'searchable': from_facebook},
    'youtube': {'name': from_youtube, 'searchable': from_youtube},
}

url_types = ('site', 'instagram', 'email', 'telegram', 'vk', 'facebook', 'youtube')
# common_name_types = ('brand_name', 'other_name', 'legal_name')


def convert_input(raw_name: str, record_type: str):
    if record_type in url_types:
        name_method = convertor_dict[record_type]['name']
        searchable_method = convertor_dict[record_type]['searchable']

        name = parse_url(raw_name, method=name_method)
        searchable = parse_url(raw_name, method=searchable_method)

        if name is None or searchable is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid query. There is no payload in the query: {raw_name}")
    else:
        name = searchable = raw_name.strip()
        if record_type == 'legal_name':
            searchable = from_legal(name)
    return name, searchable
