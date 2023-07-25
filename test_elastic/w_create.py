from elasticsearch import Elasticsearch

# Создаем подключение
es = Elasticsearch(
    hosts=[{"scheme": "http", "host": "localhost", "port": 9200}])

# Определение анализаторов
analysis = {
    "analyzer": {
        "ngram_analyzer": {
            "type": "custom",
            "tokenizer": "ngram_tokenizer",
            "filter": ["lowercase"]
        },
        "phonetic_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["phonetic_filter"]
        },
        "fuzzy_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase"]
        }
    },
    "tokenizer": {
        "ngram_tokenizer": {
            "type": "ngram",
            "min_gram": 2,
            "max_gram": 3
        }
    },
    "filter": {
        "phonetic_filter": {
            "type": "phonetic",
            "encoder": "doublemetaphone"
        }
    }
}

# Определение маппинга
mapping = {
    "properties": {
        "name": {
            "type": "text",
            "fields": {
                "ngram": {
                    "type": "text",
                    "analyzer": "ngram_analyzer"
                },
                "phonetic": {
                    "type": "text",
                    "analyzer": "phonetic_analyzer"
                },
                "fuzzy": {
                    "type": "text",
                    "analyzer": "fuzzy_analyzer"
                }
            }
        },
        "type": {
            "type": "keyword"
        }
    }
}

# Создаем индекс с определенными анализаторами и маппингом
es.indices.create(
    index='my-index',
    body={
        "settings": {
            "analysis": analysis
        },
        "mappings": mapping
    }
)
