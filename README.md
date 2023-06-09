# CargoLocatorAPI
CargoLocatorAPI - это RESTful API сервис, который позволяет искать ближайшие грузовики для перевозки грузов. Он предоставляет функционал для управления и отслеживания грузов, а также для определения текущих местоположений связанных грузовиков.

## Возможности
* Создание нового груза с указанием места загрузки (pick-up), места доставки (delivery), веса и описания.
* Получение списка грузов с указанием места загрузки, места доставки и количества ближайших грузовиков (не более 450 миль).
* Получение информации о конкретном грузе по его идентификатору, включая места загрузки и доставки, вес, описание и список номеров ВСЕХ грузовиков с указанием расстояния до выбранного груза.
* Редактирование местоположения грузовика по его идентификатору с использованием почтового индекса для определения нового местоположения.
* Редактирование груза по его идентификатору, включая изменение веса и описания.
* Удаление груза по его идентификатору.

## Технологии
Сервис разработан с использованием следующих технологий и инструментов:

* `Python (FastAPI)` - мощный фреймворк для разработки веб-приложений.
* `Асинхронность` - использование асинхронных операций для обеспечения высокой производительности.
* `asyncpg` - асинхронный драйвер для работы с PostgreSQL базой данных.
* `PostgreSQL` - стандартная реляционная база данных для хранения информации о грузах и грузовиках.
* `Docker Compose` - инструмент для развертывания и управления контейнеризированными приложениями.
## Установка и запуск
1. Установите Docker и Docker Compose на вашу систему.
2. Склонируйте репозиторий CargoLocatorAPI с помощью следующей команды:
```bash
git clone https://github.com/Koludarov/CargoLocatorAPI.git
```
3. Перейдите в каталог проекта:
```bash
cd CargoLocatorAPI
````
4. Запустите приложение с помощью Docker Compose:
```bash
docker-compose up -d
```
5. API будет доступно по адресу http://localhost:8000/api/v1.
## Документация API
После запуска приложения, документация API будет доступна по адресу http://localhost:8000/docs. В ней вы найдете подробную информацию о доступных эндпоинтах, параметрах запросов и форматах ответов.
## Дополнительно
Реализована фильтрация грузовиков на доступные(вес груза меньше грузоподъемности) и недоступные.

Пример:
```json
"trucks_info": {
        "total": 5,
        "trucks_available": {
          "amount": 2,
          "trucks": [
            {
              "truck_id": "5428U",
              "capacity": 692,
              "distance": 243.9
            },
            {
              "truck_id": "9941U",
              "capacity": 791,
              "distance": 380.5
            }
          ]
        },
        "trucks_not_enough_space": {
          "amount": 3,
          "trucks": [
            {
              "truck_id": "9634V",
              "capacity": 199,
              "distance": 100.8
            },
            {
              "truck_id": "9238W",
              "capacity": 369,
              "distance": 110.1
            },
            {
              "truck_id": "3857L",
              "capacity": 12,
              "distance": 294.6
            }
          ]
        }
      }
```
Реализована фильтрация списка грузов (вес, мили ближайших машин до грузов):

Пример запроса со всеми фильтрами:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/cargos_filtered?weight_more=78&weight_less=305&distance_more=125&distance_less=212' \
  -H 'accept: application/json'
```
Пример запроса для создания груза:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/cargos' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "pickup_zip": "12781",
  "delivery_zip": "02360",
  "weight": 17,
  "description": "Small box"
}'
```
## Лицензия
<a href="https://github.com/Koludarov/CargoLocatorAPI/blob/main/LICENSE">MIT License</a>