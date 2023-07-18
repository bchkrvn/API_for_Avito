# MARKET

## Описание:
В данном проекте была реализована серверная часть для сайта с 
объявлениями с использованием Django, DRF, Djoser, Postgres.  
Были написаны тесты с использованием PyTest.

## Используемые технологии:
- Python
- Django
- Postgres
- DRF
- Djoser
- PyTest

## Возможности:
Видео на Youtube:  
[![Watch the video](https://img.youtube.com/vi/lqaQyRieQt8/maxresdefault.jpg)](https://youtu.be/lqaQyRieQt8)
- Регистрация, авторизация и аутентификация пользователя
- Сброс пароля через почту
- Создание и редактирование объявлений
- Поиск объявлений по названию
- Комментирование объявлений

## Как запустить проект:
1) Скопируйте репозиторий:    
`git clone https://github.com/bchkrvn/Market-API.git`


2) Перейдите в папку **docker** создайте переменный окружения в файле .docker_env 
```
SECRET_KEY=...
DB_ENGINE=...
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=...
EMAIL_HOST=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
EMAIL_PORT=...
DEBUG=...
```

3) Запустите приложение с помощью команды:  
`docker-compose up -d`


## Документация
Для того, чтобы просмотреть документацию к проекту, запустите сервер и перейдите по ссылке:  
`/api/docs`

## Тестирование
Для того, чтобы протестировать сервер, необходимо воспользоваться следующей командой:  
`pytest`