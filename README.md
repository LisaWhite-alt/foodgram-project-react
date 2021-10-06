[![foodgram-app workflow](https://github.com/LisaWhite-alt/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/LisaWhite-alt/foodgram-project-react/actions/workflows/foodgram_workflow.yml)


# Foodgram

## Описание проекта

Сайт «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии

* Docker
* Docker-compose
* Python 3.8.5
* Django 2.2.19
* djangorestframework 3.12.4
* готовый frontend на React

### Проект берем отсюда

[Ссылка:](https://github.com/LisaWhite-alt/foodgram-project-react)

### Добавить в Secrets GitHub Actions переменные окружения

```python
DB_HOST
DB_NAME
DB_PORT
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
PASSPHRASE
POSTGRES_PASSWORD
POSTGRES_USER
SSH_KEY
USER
SECRET_KEY
```

### Поместить на сервер:

docker-compose.yaml
/nginx
/docs

### Команда для запуска

push в репозиторий в ветки master или main

### Команда для создания суперпользователя

`sudo docker exec -it <CONTAINER ID> python manage.py createsuperuser`


### Заполнение базы данных

`sudo docker exec -it <CONTAINER ID> python manage.py loaddata fixtures.json`

### Адрес для проверки работоспособности

[Ссылка:](https://lisatube.co.vu)

### Данные на администратора

Логин: admin
Пароль: 12345admin

### Автор

Богомолова Екатерина