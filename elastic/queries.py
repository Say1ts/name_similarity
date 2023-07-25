import enum

from elastic.filters import filters
from elastic.shema import Filter


def get_search_query(name: str, filter_type: Filter, types: tuple, min_score: int = 15):
    if isinstance(filter_type, Filter):
        filter_type = filter_type.value

    query = {
        "query": filters[filter_type](name, types),
        "min_score": min_score
    }
    return query


def check_existence(es, name: str, record_type: str):
    query = get_search_query(
        name, types=(record_type,),
        filter_type=Filter.KEYWORD_NAME,
        min_score=0)
    return es.search(
        index="my-index",
        body=query
    )['hits']['hits']
