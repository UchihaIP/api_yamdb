# Проект YaMDb
## Описание проекта 

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). 

На одно произведение пользователь может оставить только один отзыв.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
  git clone https://github.com/UchihaIP/api_yamdb.git 
  cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```bash
  python3 -m venv env source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```bash
  python3 -m pip install --upgrade pip
  pip install -r requirements.txt
```
Выполнить миграции:
```bash
  python3 manage.py migrate
```
Запустить менеджер на добавление данных в БД:
```bash
  python3 manage.py load_csv_users
  python3 manage.py load_csv_reviews
```
Запустить проект:
```bash
  python3 manage.py runserver
```
## API Reference

#### Регистрация нового пользователя

```http
  POST /api/v1/auth/signup/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required** |
| `username` | `string` | **Required** |


#### Получение JWT-токена

```http
  POST /api/v1/auth/token/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required** |
| `confirmation_code`      | `string` | **Required** |


#### Получение списка всех категорий

```http
  GET /api/v1/categories/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `search`      | `string` | Поиск по названию категории |

#### Добавление нового отзыва

```http
  POST /api/v1/titles/{title_id}/reviews/

```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title_id`      | `integer` | **Required** ID произведения |
| `text`      | `string` | **Required** Текст отзыва |
| `score`      | `integer` | **Required** Оценка от 1 до 10 |






## Running Tests

Для запуска тестов, введите команду

```bash
  pytest
```


## Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

## Author

- [Рифат Хасанов](https://github.com/UchihaIP)   (Teamlead)
- [Виталий Лукьнов](https://github.com/VitaliiLuki) (Developer)
- [Роман Агеев](https://github.com/Gegins) (Developer)

