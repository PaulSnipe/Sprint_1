# FSTR Pass Submission API

**FSTR Pass Submission API** — это REST API для приёма, хранения и обработки информации о горных перевалах, отправленных туристами.  
Проект выполнен на базе **FastAPI** и **PostgreSQL** с использованием **SQLAlchemy ORM**.  
API предназначен для взаимодействия с внешним мобильным приложением, отправляющим данные о перевалах.

## Функциональность

- Приём данных о перевалах через POST-запрос `/submitData`
- Получение перевала по ID `/submitData/{id}`
- Редактирование перевала, если статус = `new` `/submitData/{id}` (PATCH)
- Получение всех перевалов пользователя по email `/submitData/?user__email=<email>`
- Автоматическое сохранение пользователя, координат, уровня сложности и изображений
- Проверка корректности данных
- Автоматическая генерация Swagger-документации
- Хранение данных в PostgreSQL

---

##  Стек технологий

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Pydantic**
- **Uvicorn**

## Установка и запуск 

1. Клонируй репозиторий:
   ```bash
   git clone git@github.com:PaulSnipe/Sprint_1.git
   cd Sprint_1/PycharmProjects/fstr_project
Создай виртуальное окружение и установи зависимости:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
Настрой .env с переменными окружения для PostgreSQL:

FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_LOGIN=postgres
FSTR_DB_PASS=password
FSTR_DB_NAME=fstr_db
Запусти сервер:

uvicorn app.main:app --reload
Swagger-документация доступна по адресу:
http://127.0.0.1:8000/docs
Структура проекта

fstr_project/
├── app/
│   ├── __init__.py
│   ├── main.py          # Точка входа FastAPI
│   ├── models.py        # ORM-модели базы данных
│   ├── database.py      # Подключение к PostgreSQL
│   ├── crud.py          # Класс/функции для работы с БД
│   └── routes/
│       ├── __init__.py
│       └── submit.py    # Эндпоинты POST/GET/PATCH
├── venv/                # Виртуальное окружение 
├── .env                 # Переменные окружения 
├── .gitignore
├── README.md
└── requirements.txt

1. Добавление нового перевала (POST /submitData)
Тело запроса (JSON):

{
  "beauty_title": "пер.",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22 13:18:13",
  "user": {
    "email": "qwerty@mail.ru",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
  },
  "coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {"data":"<картинка1>", "title":"Седловина"},
    {"data":"<картинка2>", "title":"Подъём"}
  ]
}
Пример успешного ответа:

{
  "status": 200,
  "message": null,
  "id": 42
}
2. Получение перевала по ID (GET /submitData/{id})
Пример запроса:

GET http://127.0.0.1:8000/submitData/42
Пример ответа:

{
  "id": 42,
  "status": "new",
  "beauty_title": "пер.",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22 13:18:13",
  "user": {
    "email": "qwerty@mail.ru",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
  },
  "coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {"title":"Седловина","data":"<картинка1>"},
    {"title":"Подъём","data":"<картинка2>"}
  ]
}
3. Редактирование перевала (PATCH /submitData/{id})
Пример запроса:

PATCH http://127.0.0.1:8000/submitData/42
Content-Type: application/json

{
  "beauty_title": "пер. Пхия",
  "coords": {
    "height": "1250"
  },
  "level": {
    "summer": "1Б"
  }
}
Пример ответа:

{
  "state": 1,
  "message": "Запись успешно обновлена"
}
Ошибка при запрещённом редактировании:

{
  "state": 0,
  "message": "Редактирование запрещено: статус не 'new'"
}
4. Получение всех перевалов пользователя по email (GET /submitData/?user__email=<email>)
Пример запроса:
GET http://127.0.0.1:8000/submitData/?user__email=qwerty@mail.ru
Пример ответа:
[
  {"id": 42, "title": "Пхия", "status": "new", "add_time": "2021-09-22 13:18:13"},
  {"id": 43, "title": "Альпийский перевал", "status": "accepted", "add_time": "2021-10-01 09:45:00"}
]
Автор проекта
Павел Бекасов
Москва, 2025
📧 Контакты: pbekasov@mail.ru