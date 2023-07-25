# Описание проекта
Микросервис предназначен для создания базы имен из различных источников с последующим проведением поиска по этим именам.

Поддерживаемые источники:
```python
class RecordType(Enum):
    NAME = 'name'
    SITE = 'site'
    INSTAGRAM = 'instagram'
    EMAIL = 'email'
    TELEGRAM = 'telegram'
    VK = 'vk'
    FACEBOOK = 'facebook'
    YOUTUBE = 'youtube'
```

Сервис поддерживает кириллицу. Символы транслитерируются в латиницу для нормализации. Затем поиск производится по заданным фильтрам:
```python
class Filter(Enum):
    FUZZY = 'fuzzy'
    NGRAM = 'ngram'
    PHONETIC = 'phonetic'
    NGRAM_AND_PHONETIC = 'ngram_and_phonetic'
    KEYWORD_NAME = 'keyword_name'
```






[https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html]
```sh
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.7.1
docker run \
	--name es-node01 \
    --restart unless-stopped \
	--net elastic \
	-p 9200:9200 -p 9300:9300 \
	-e "xpack.security.enabled=false" \
	-e "discovery.type=single-node"\
	-t docker.elastic.co/elasticsearch/elasticsearch:8.7.1
```


```
✅ Elasticsearch security features have been automatically configured!  
✅ Authentication is enabled and cluster connections are encrypted.  
  
ℹ️  Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):  
 Tf=U9PIBM+cbqPibmjUg  
  
ℹ️  HTTP CA certificate SHA-256 fingerprint:  
 9b38f838a1207e386e790d9001ff2b73476dbbe7c2173fad921e5d8b96a44901  
  
ℹ️  Configure Kibana to use this cluster:  
• Run Kibana and click the configuration link in the terminal when Kibana starts.  
• Copy the following enrollment token and paste it into Kibana in your browser (valid for the next 30 minutes):  
 eyJ2ZXIiOiI4LjcuMSIsImFkciI6WyIxNzIuMTkuMC4yOjkyMDAiXSwiZmdyIjoiOWIzOGY4MzhhMTIwN2UzODZlNzkwZDkwMDFmZjJiNzM0NzZkYmJlN2MyMTczZmFkOTIxZTVkOGI5NmE0NDkwMSIsImtleSI6IjZvQjVVWWdCUGxxa0wzTWtyZkF1OnRGR3kyM0pMUURDOFlId2s0cEFSYUEifQ==  
  
ℹ️ Configure other nodes to join this cluster:  
• Copy the following enrollment token and start new Elasticsearch nodes with `bin/elasticsearch --enrollment-token <token>` (valid for the next 30 minutes):  
 eyJ2ZXIiOiI4LjcuMSIsImFkciI6WyIxNzIuMTkuMC4yOjkyMDAiXSwiZmdyIjoiOWIzOGY4MzhhMTIwN2UzODZlNzkwZDkwMDFmZjJiNzM0NzZkYmJlN2MyMTczZmFkOTIxZTVkOGI5NmE0NDkwMSIsImtleSI6IjY0QjVVWWdCUGxxa0wzTWtyZkF1Ok1IcV9nNG9KUWdDX3lQWXc1MmpXbkEifQ==  
  
 If you're running in Docker, copy the enrollment token and run:  
 `docker run -e "ENROLLMENT_TOKEN=<token>" docker.elastic.co/elasticsearch/elasticsearch:8.7.1
 ```


```sh

docker pull docker.elastic.co/kibana/kibana:8.7.1
docker run \
	--name kib-01 \
    --restart unless-stopped \
	--net elastic \
	-e "ELACTICSERACH_HOSTS=http://elasticsearch:9200" \
	-d \
	-p 5601:5601 docker.elastic.co/kibana/kibana:8.7.1 
	
```

Получить код верификации из кибаны
docker exec -it kib-01 bin/kibana-verification-code