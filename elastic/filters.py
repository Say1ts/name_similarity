def ngram(name: str):
    return {
        "match": {
            "latin.ngram": {
              "query": name,
              "boost": 1
            }
        }
    }


def phonetic(name: str):
    return {
        "match": {
            "latin.phonetic": {
              "query": name,
              "boost": 0.7
            }
        }
    }


def fuzzy(name: str):
    return {
        "fuzzy": {
            "latin": {
                "value": name
            }
        }
    }


def query_with_type(conditions: tuple, types: list):
    if types:
        must = [
            {
                "terms": {
                    "type": types
                }
            }
        ]
    else:
        must = []
    must.extend(conditions)
    return {
        "bool": {
            "must": must
        }
    }


def keyword_name(name: str, types):
    q = {
        "match": {
            "name": name
        }
    }
    return query_with_type((q,), types)


def ngram_and_phonetic(name: str, types):
    return query_with_type(
        conditions=(
            ngram(name), phonetic(name)
        ),
        types=types
    )


filters = {
    'ngram': ngram,
    'phonetic': phonetic,
    'fuzzy': fuzzy,
    'ngram_and_phonetic': ngram_and_phonetic,
    'keyword_name': keyword_name
}
