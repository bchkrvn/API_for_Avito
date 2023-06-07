# MARKET

## Описание:
В данном проекте была реализована серверная часть для сайта с 
объявлениями с использованием Django, DRF, Djoser, Postgres.  
Были написаны тесты с использованием PyTest.

# #Используемые технологии:
- Python
- Django
- Postgres
- DRF
- Djoser
- PyTest

## Возможности:
- Регистрация, авторизация и аутентификация пользователя
- Сброс пароля через почту
- Создание и редактирование объявлений
- Поиск объявлений по названию
- Комментирование объявлений

## Как запустить проект:
1) Сделать копию данного репозитория:  
`git clone ...`

2) Для того, чтобы запустить сервер, необходимо создать виртуально окружение на локальной машине:  
`python -m venv venv`

3) После этого активировать виртуальное окружение:  
`venv\Scripts\activate.bat`

4) Настроить переменную окружения в файле .env:  
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=skymarket
DB_USER=skymarket
DB_PASSWORD=skymarket
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
EMAIL_PORT=...
DEBUG=1
```

4) Перейти в папку **market_postgres** запустить *frontend* и *postgres* командой:  
`docker-compose up -d`

5) Перейти в папку **market** и выполнить миграции:  
`python3 manage.py migrate`

6) При желании загрузить данные в БД:  
`python3 manage.py loadall`

7) Запустить *backend* командой:  
`python3 manage.py runserver`

## Документация
Для того, чтобы просмотреть документацию к проекту, запустите сервер и перейдите по ссылке:  
`/api/docs`

## Тестирование
Для того, чтобы протестировать сервер, необходимо воспользоваться следующей командой:  
`pytest`