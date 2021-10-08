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
P.S. В ссылке вместо <version> необходимо вписать актуальную версию
### 4. Локально отредактируйте файл foodgram-project-react/infra/nginx.conf и в строке server_name впишите свой IP
### 5. Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```python
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```



## Автор
Саляхов Ильдар Флюрович

Telegram: @ildarick
