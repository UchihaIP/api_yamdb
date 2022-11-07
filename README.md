Yatube - это социальная сеть выраженная в виде API,
 в которой реализованы возможности: публиковать и смотреть записи, 
 оставлять комментарии, а так же подписываться на понравившихся авторов.
## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
  git clone https://github.com/UchihaIP/api_final_yatube.git 
  cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:
```bash
  python3 -m venv env 
  source env/bin/activate
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
Запустить проект:
```bash
  python3 manage.py runserver
```
