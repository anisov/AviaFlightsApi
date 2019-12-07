# AviaFlights Api use Flask.

#### Configure and start project use docker.
1) export CURRENT_UID=$(id -u):$(id -g)
2) export PROJECT_DIR='path/to/project'
3) export CODE_FOLDER=avia_flights
4) Create `docker/docker-compose.yml` based on `docker-compose.yml.sample`. 
5) Create `docker/dockerfiles/uwsgi.Dockerfile` based on `docker/dockerfiles/uwsgi.Dockerfile.sample`.
6) Create `docker/docker_data/nginx/nginx.conf `based on `docker/docker_data/nginx/nginx.conf.sample`.
7) Create `docker/docker_data/uwsgi/uwsgi.ini` based on `docker/docker_data/uwsgi/uwsgi.ini.sample`.
8) docker-compose -f docker/docker-compose.yml -p avia_flights build
9) docker-compose -f docker/docker-compose.yml -p avia_flights up -d

#### Stop project.
docker-compose -f docker/docker-compose.yml -p avia_flights down
***
#### Simple Project Start.
1) `cd ./avia_flights`
2) `mkvirtualenv avia_flights -p /usr/bin/python3.7`
3) `workon avia_flights`
4) `pip install -r requirements.txt`
5) `python manage.py runserver`
***
#### Run Tests.
python manage.py test
***
## Project Technical Task

### AviaFlights API

**Introduction**

Данны два XML – это ответы на поисковые запросы, сделанные к одному из партнёров. В ответах лежат варианты перелётов со всей необходимой информацией, чтобы отобразить билет.

На основе этих данных, нужно сделать вебсервис, в котором есть эндпоинты, отвечающие на следующие запросы:

1) Какие варианты перелёта из DXB в BKK мы получили?
2) Самый дорогой/дешёвый, быстрый/долгий и оптимальный варианты
3) В чём отличия между результатами двух запросов (изменение маршрутов/условий)?

Используемые технологии: python 3.7 + Flask + beautifulsoup4
