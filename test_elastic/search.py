from elasticsearch import Elasticsearch

# Создаем подключение
es = Elasticsearch(
    hosts=[{"scheme": "http", "host": "localhost", "port": 9200}])
def search(name):
    print(f"\n Search {name.upper()}")
    # Поиск по n-граммам
    ngram_search = {
        "query": {
            "match": {
                "latin.ngram": name
            }
        }
    }

    # Поиск по фонетике
    phonetic_search = {
        "query": {
            "match": {
                "latin.phonetic": name
            }
        }
    }

    # Нечеткий поиск
    fuzzy_search = {
        "query": {
            "fuzzy": {
                "latin": {
                    "value": name
                }
            }
        }
    }

    # Выполнение поиска
    ngram_response = es.search(index="my-index", body=ngram_search)
    phonetic_response = es.search(index="my-index", body=phonetic_search)
    fuzzy_response = es.search(index="my-index", body=fuzzy_search)

    if ngram_response['hits']['total']['value'] > 0:
        print('ngram_response')
        for hit in ngram_response['hits']['hits']:
            print(hit['_source'])
    else:
        print("Нет результатов для данного запроса ngram_response.")

    if phonetic_response['hits']['total']['value'] > 0:
        print('phonetic_response')
        for hit in phonetic_response['hits']['hits']:
            print(hit['_source'])
    else:
        print("Нет результатов для данного запроса phonetic_response.")

    if fuzzy_response['hits']['total']['value'] > 0:
        print('fuzzy_response')
        for hit in fuzzy_response['hits']['hits']:
            print(hit['_source'])
    else:
        print("Нет результатов для данного запроса fuzzy_response.")


search(name='alasony')
search(name='alazany')
