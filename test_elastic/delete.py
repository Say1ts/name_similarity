from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')
index_name = 'my-index'
query = {
    "query": {
        "match_all": {}
    }
}

response = es.delete_by_query(index=index_name, body=query)

if response['deleted']:
    print(f"Удалено {response['deleted']} документов из индекса {index_name}.")
else:
    print("Ни одного документа не удалено.")
