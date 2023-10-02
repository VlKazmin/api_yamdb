# Проект YaMDb

YaMDb - это проект, который собирает отзывы пользователей на произведения, такие как книги, фильмы и музыка. Произведения разделены на категории, а каждое произведение может быть присвоено одному или нескольким жанрам. Новые жанры могут создаваться только администраторами. Пользователи имеют возможность оставлять текстовые отзывы и ставить оценки произведениям в диапазоне от одного до десяти. Из пользовательских оценок вычисляется средняя оценка произведения, которая определяет его рейтинг.

Проект поддерживает аутентификацию по JWT-токену и предоставляет методы GET, POST, PUT, PATCH и DELETE для взаимодействия с данными. Вся информация предоставляется в формате JSON.

## Стек технологий

- Python
- Django REST Framework
- Simple JWT (работа с JWT-токенами)
- django-filter (фильтрация запросов)
- SQLite (база данных)
- Git (система управления версиями)

## Запуск проекта

Чтобы запустить проект, выполните следующие шаги:

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/VlKazmin/api_yamdb/
   cd api_yamdb
   ```
2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv env
    source env/bin/activate
    ```
3. Установите зависимости из файла requirements.txt:
    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. Выполните миграции:
    ```bash
    python manage.py migrate
    ```
5. Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```
6. Загрузите начальные данные из CSV файлов:
    ```bash
    python manage.py load_csv
    ```
7. Запустите проект:
    ```bash
    python manage.py runserver
    ```

Теперь ваш проект доступен по адресу http://127.0.0.1:8000/.
Полная документация (redoc.yaml) доступна по адресу http://127.0.0.1:8000/redoc/.
Вы также можете запустить тесты с помощью команды pytest, чтобы проверить работу модулей.

## Алгоритм регистрации новых пользователей
Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт **/api/v1/auth/signup/**.
Сервис YaMDb отправляет письмо с кодом подтверждения **(confirmation_code)** на указанный адрес email.
Пользователь отправляет POST-запрос с параметрами username и **confirmation_code** на эндпоинт **/api/v1/auth/token/**, и в ответе на запрос ему приходит token (JWT-токен).
Теперь пользователь может использовать полученный токен для работы с API проекта. После регистрации и получения токена, пользователь может отправить PATCH-запрос на эндпоинт **/api/v1/users/me/** и заполнить свой профиль.

## Ресурсы API YaMDb
Проект предоставляет следующие ресурсы:

* Ресурс **auth**: аутентификация.
* Ресурс **users**: пользователи.
* Ресурс **titles**: произведения, к которым пишут отзывы (фильмы, книги, музыка).
* Ресурс **categories**: категории произведений (фильмы, книги, музыка).
* Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
* Ресурс **reviews**: отзывы на произведения. Отзыв привязан к определенному произведению.
* Ресурс **comments**: комментарии к отзывам. Комментарий привязан к определенному отзыву.

## Кастомная команда load_csv
Добавлена кастомная команда load_csv, которая позволяет загрузить данные из CSV файлов, находящихся в папке static/data, в базу данных. Эти данные включают в себя:

* Категории **(category)**
* Комментарии **(comments)**
* Жанры произведений **(genre_title)**
* Жанры **(genre)**
* Отзывы **(review)**
* Произведения **(titles)**
* Пользователи **(users)**
* Для использования команды **load_csv** выполните ее после миграции и перед запуском сервера. Это позволит инициализировать базу данных начальными данными из CSV файлов

## Пример HTTP-запроса (POST /api/v1/titles/)
```json
{
  "name": "Название произведения",
  "year": 2023,
  "description": "Описание произведения",
  "genre": ["Жанр 1", "Жанр 2"],
  "category": "Категория"
}
```

## Пример ответа от API YaMDb
```json
{
  "id": 1,
  "name": "Название произведения",
  "year": 2023,
  "rating": 0.0,
  "description": "Описание произведения",
  "genre": [
    {
      "name": "Жанр 1",
      "slug": "zhann-1"
    },
    {
      "name": "Жанр 2",
      "slug": "zhann-2"
    }
  ],
  "category": {
    "name": "Категория",
    "slug": "kategoriya"
  }
}
```

Этот пример демонстрирует HTTP-запрос типа POST для создания нового произведения (**titles**). В запросе указаны параметры, такие как название, год выпуска, описание, список жанров и категория произведения. В ответе от API возвращается информация о созданном произведении, включая его уникальный идентификатор (id), название, год выпуска, рейтинг, описание, список жанров и категория.

## Авторы проекта
* Владислав Казьмин (GitHub: [VlKazmin](https://github.com/VlKazmin))
* Андрей Яхутин (GitHub: [Andrei-yakh](https://github.com/Andrei-yakh))
* Иосиф Огир (GitHub: [Iosif477](https://github.com/Iosif477))

