import re
from typing import Tuple, Optional

from elasticsearch import Elasticsearch

from elastic.queries import get_search_query, check_existence
from elastic.shema import Filter, url_types, convertor_dict, convert_input, RecordRequest
from services.duration_measurer import execution_time_decorator
from format.transliteration.from_cyrillic import to_latin_from_cyrillic

es = Elasticsearch(
    hosts=[{"scheme": "http", "host": "localhost", "port": 9200}])


@execution_time_decorator
def search_similar(request: RecordRequest, filter_type: Filter, types: Optional[Tuple]):
    search_query = request.name
    if request.name_type:
        _, search_query = convert_input(search_query, request.name_type.value)
    search_query = re.sub(r'[._-]', ' ', search_query)
    print(search_query)

    latin = to_latin_from_cyrillic(search_query)
    query = get_search_query(latin, filter_type, types)
    return es.search(index="my-index", body=query)


def create_record(name: str, record_type: str):
    name, searchable = convert_input(name, record_type)
    exist = check_existence(es, name, record_type)
    if not exist:
        searchable = to_latin_from_cyrillic(searchable)
        document = {'name': name, 'latin': searchable, 'type': record_type}
        return es.index(index="my-index", body=document)
    else:
        print("Document with such brand_name already exists.")
        return {
            'success': False,
            'message': f'{name} already exists'
        }

# def create_record(name: str, record_type: str):
#     if record_type == 'site':
#         name = parse_url(name, to_domains)
#
#     exist = check_existence(es, name, record_type)
#     if not exist:
#         latin = to_latin_from_cyrillic(name)
#         document = {'name': name, 'latin': latin, 'type': record_type}
#         return es.index(index="my-index", body=document)
#     else:
#         print("Document with such brand_name already exists.")
#         return {
#             'success': False,
#             'message': f'{name} already exists'
#         }
