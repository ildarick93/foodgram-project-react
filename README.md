# Foodgram

## Описание
Проект Foodgram - сервис для публикации рецептов пользователей.
Пользователь может создать свой рецепт с индвидуальным набором ингредиентов. Можно подписываться на авторов рецептов.
Каждому рецепту можно присвоить определеные тэги, добавлять рецепты в избранное и в список покупок. Список покупок можно скачать для удобства. 

## Технологии
* Python 
* Git 
* Docker 
* CI/CD 
* Django REST Framework 
* PostgreSQL 
* API

## Подготовка к запуску проекта:
1. Склонируйте репозиторий на локальную машину
```python
git clone https://github.com/ildarick93/foodgram-project-react
```
## Для работы с удаленным сервером (Ubuntu):
### 1. Выполните вход на свой удаленный сервер
### 2. Установите Docker на сервер:
```python
sudo apt install docker.io 
```
### 3. Установите docker-compose на сервер:
```python
sudo curl -L "https://github.com/docker/compose/releases/download/<version>/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
P.S. В ссылке вместо version необходимо вписать актуальную версию без кавычек
### 4. Локально отредактируйте файл foodgram-project-react/infra/nginx.conf и в строке server_name впишите свой IP
### 5. Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```python
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
### 6. На сервере создайте файл .env (nano .env) и заполните переменные окружения или создайте этот файл локально и скопируйте файл по аналогии с предыдущим пунктом:
```python
SECRET_KEY=<секретный ключ проекта django>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных postgres>
DB_USER=<имя пользователя БД>
DB_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432
```
### 7. Создайте на сервере файл pg.env для работы с контейнером postgres и поместите в него значения переменных окружения:
```python
POSTGRES_PASSWORD=<пароль для базы данных> - обязательный параметр
DB_NAME=<название базы данных> - необязательный параметр (по умолчанию - postgres)
POSTGRES_USER=<имя пользователя> - необязательный параметр (по умолчанию - postgres)
```
### 8. На сервере соберите образ:
```python
sudo docker-compose up -d --build
```
### 9. После успешной сборки на сервере выполните команды (только после первого деплоя):

## Автор
Саляхов Ильдар Флюрович

Telegram: @ildarick
