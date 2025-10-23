# FSTR Pass Submission API

**FSTR Pass Submission API** — это REST API для приёма, хранения и обработки информации о горных перевалах, отправленных туристами.  
Проект выполнен на базе **FastAPI** и **PostgreSQL** с использованием **SQLAlchemy ORM**.  
API предназначен для взаимодействия с внешним мобильным приложением, отправляющим данные о перевалах.

---

## Функциональность

- Приём данных о перевалах через POST-запрос `/submitData`
- Автоматическое сохранение пользователя, координат, уровня сложности и изображений
- Проверка корректности данных
- Автоматическая генерация Swagger-документации
- Хранение данных в PostgreSQL

---

## 🧩 Стек технологий

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Pydantic**
- **Uvicorn**

---

## Установка и запуск 

1. Клонируй репозиторий:
   ```bash
   git clone git@github.com:PaulSnipe/Sprint_1.git
   cd Sprint_1

##  Структура проекта
fstr_project/
├── app/
│ ├── init.py
│ ├── main.py # Точка входа FastAPI
│ ├── models.py # ORM-модели базы данных
│ ├── database.py # Подключение к PostgreSQL
│ ├── crud.py # Класс/функции для работы с БД
│ └── routes/
│ ├── init.py
│ └── submit.py # POST /submitData
├── venv/ # Виртуальное окружение 
├── .env # Переменные окружения 
├── .gitignore
├── README.md
└── requirements.txt


## Примеры вызова REST API
### 1. Добавление нового перевала

**Тело запроса (JSON):**
```json
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

Пример ответа при успешной вставке:

{
  "status": 200,
  "message": null,
  "id": 42
}


Пример ошибки при нехватке полей:

{
  "status": 400,
  "message": "Отсутствуют обязательные поля: user",
  "id": null
}


Пример ошибки сервера:

{
  "status": 500,
  "message": "Ошибка на сервере: ошибка подключения к базе данных",
  "id": null
}

Автор проекта
Павел Бекасов
Москва, 2025
📧 Контакты: pbekasov@mail.ru