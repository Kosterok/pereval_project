## Функционал

- POST `/submitData`
Добавляет новый перевал с координатами, пользователем, изображениями и уровнем сложности.  
При добавлении новой записи поле `status` автоматически получает значение `new`.
- GET `/submitData/<id>`
Возвращает всю информацию по перевалу с указанным ID, включая `status`.
- PATCH `/submitData/<id>`
Позволяет редактировать данные перевала только если статус `new`.
Редактировать можно все поля, кроме данных пользователя (`email`, `fam`, `name`, `otc`, `phone`).
- GET `/submitData/?user__email=<email>`
Возвращает список всех перевалов, добавленных пользователем с указанным email.

---
## Установка и запуск

1️⃣ **Клонировать репозиторий**
```bash
git clone https://github.com/Kosterok/pereval_project.git
cd pereval_project
```

2️⃣ **Создать и активировать виртуальное окружение**
```bash
python -m venv .venv
.venv\Scripts\activate
```

3️⃣ **Установить зависимости**
```bash
pip install -r requirements.txt
```

4️⃣ **Создать файл `.env`** в корне проекта:
```
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_LOGIN=postgres
FSTR_DB_PASS=password
FSTR_DB_NAME=pereval
```

5️⃣ **Создать базу данных и импортировать структуру**
```sql
CREATE DATABASE pereval;
\c pereval
\i pereval_2022-02-22-2021.sql
```

6️⃣ **Добавить поле `status`, если его нет**
```sql
ALTER TABLE pereval_added
  ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'new',
  ADD CONSTRAINT chk_pereval_added_status CHECK (status IN ('new','pending','accepted','rejected'));
```

7️⃣ **Запустить сервер**
```bash
python api.py
```

---

## Эндпоинты API

## 🌐 Эндпоинты API

| Метод | URL | Описание | Тело запроса / Параметры | Пример ответа |
|--------|-----|-----------|---------------------------|----------------|
| **POST** | `/submitData` | Добавить новый перевал | JSON с данными перевала (см. пример ниже) | `{ "status": 200, "message": "Отправлено успешно", "id": 1 }` |
| **GET** | `/submitData/<id>` | Получить данные перевала по ID | — | JSON с полными данными перевала |
| **PATCH** | `/submitData/<id>` | Обновить данные перевала (если `status = new`) | JSON (аналогичный POST) | `{ "state": 1, "message": "Успешно обновлено" }` |
| **GET** | `/submitData/?user__email=<email>` | Получить все перевалы, добавленные пользователем с данным email | Query-параметр `user__email` | Список JSON-объектов с перевалами |

---

#### Пример запроса к `POST /submitData`
```json
{
  "beauty_title": "пер. ",
  "title": "Тестовый",
  "other_titles": "Тест",
  "connect": "",
  "add_time": "2025-11-01 13:18:13",
  "user": {
    "email": "test@test.ru",
    "fam": "Иванов",
    "name": "Иван",
    "otc": "Иванович",
    "phone": "+79999999999"
  },
  "coords": {
    "latitude": "55.727739",
    "longitude": "37.606945",
    "height": "1000"
  },
  "level": { "summer": "1А" },
  "images": [
    {"data": "<картинка1>", "title": "картинка1"},
    {"data": "<картинка2>", "title": "картинка2"}
  ]
}
```

#### Пример ответа:
```json
{
  "status": 200,
  "message": "Отправлено успешно",
  "id": 4
}
```

#### Возможные коды:
| Код | Значение | Описание |
|-----|-----------|----------|
| 200 | OK | Запись успешно добавлена |
| 400 | Bad Request | Ошибка формата JSON |
| 500 | Internal Server Error | Ошибка подключения или SQL |

---

##  Swagger-документация

 [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

---
