from elasticsearch import Elasticsearch

# Установите подключение к Elasticsearch
es = Elasticsearch('http://localhost:9200')
index_name = 'my-index'

query = {
  "query": {
    "match_all": {}
  }
}

response = es.search(index=index_name, body=query)

for hit in response['hits']['hits']:
    source = hit['_source']
    print(source)
