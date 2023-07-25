from typing import List, Tuple

from fastapi import APIRouter
from elastic import api
from elastic.shema import Filter, RecordType, RecordRequest, convert_input

router = APIRouter()


@router.post("/search_similar/", tags=["Similarity"])
async def search_similar_brand_name(
        request: RecordRequest, types: Tuple[str] = None,
        filter_type: Filter = Filter.NGRAM_AND_PHONETIC):
    return api.search_similar(request, filter_type, types)


@router.post("/create_record/", tags=["Similarity"])
async def create_record(request: RecordRequest, record_type: RecordType):
    return api.create_record(request.name, record_type.value)
