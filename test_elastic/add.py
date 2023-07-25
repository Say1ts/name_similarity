# from elasticsearch import Elasticsearch
#
#
# es = Elasticsearch('http://localhost:9200')
#
# index_name = 'my-index'
# document = {
#     'name': 'Alazany',
#     'type': 'brand_name'
# }
#
# response = es.index(index=index_name, document=document)
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch('http://localhost:9200')
index_name = 'my-index'

# Создание списка записей для индексации
documents = [
    {'name': 'Alazany', 'type': 'brand_name'},
    {'name': 'Алазани', 'type': 'other_name'},
    {'name': 'Alazany Restaurants', 'type': 'legal_name'},
    {'name': 'Lazany Corp', 'type': 'brand_name'}
]

# Подготовка списка операций для метода bulk()
actions = [
    {'_index': index_name, '_source': document}
    for document in documents
]

success, _ = bulk(es, actions)

if success:
    print("Записи успешно добавлены в Elasticsearch.")
else:
    print("Ошибка при добавлении записей в Elasticsearch.")
