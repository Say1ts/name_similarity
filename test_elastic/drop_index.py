from elasticsearch import Elasticsearch

# Создание экземпляра Elasticsearch
es = Elasticsearch(
    hosts=[{"scheme": "http", "host": "localhost", "port": 9200}]
)

# Указание имени индекса, который нужно удалить
index_name = 'my-index'

# Удаление индекса
response = es.indices.delete(index=index_name)

# Проверка успешного удаления индекса
if response['acknowledged']:
    print(f"Индекс {index_name} успешно удален.")
else:
    print(f"Ошибка при удалении индекса {index_name}.")