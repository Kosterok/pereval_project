## Функционал

- Приём данных о перевале (`/submitData`)
- Сохранение JSON в PostgreSQL
- Автоматическое присвоение статуса `"new"`
- Подключение к БД через `.env` файл
- Просмотр Swagger-документации

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

### **POST /submitData**

Добавляет новый перевал в БД.

#### Пример запроса:
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

Здесь можно протестировать метод **POST /submitData** прямо из браузера.

---
