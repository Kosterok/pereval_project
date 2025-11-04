from flask import Flask, request, jsonify
from db import PerevalDatabase
from flasgger import Swagger
import json

app = Flask(__name__)
swagger = Swagger(app)
db = PerevalDatabase()

@app.route('/submitData', methods=['POST'])
def submit_data():
    """
    Добавить данные о перевале
    ---
    tags:
      - Pereval
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            beauty_title:
              type: string
              example: "пер. "
            title:
              type: string
              example: "Тестовый"
            other_titles:
              type: string
              example: "Тест"
            connect:
              type: string
              example: ""
            add_time:
              type: string
              example: "2025-11-01 13:18:13"
            user:
              type: object
              properties:
                email:
                  type: string
                  example: "test@test.ru"
                fam:
                  type: string
                  example: "Иванов"
                name:
                  type: string
                  example: "Иван"
                otc:
                  type: string
                  example: "Иванович"
                phone:
                  type: string
                  example: "+79999999999"
            coords:
              type: object
              properties:
                latitude:
                  type: string
                  example: "55.727739"
                longitude:
                  type: string
                  example: "37.606945"
                height:
                  type: string
                  example: "1000"
            level:
              type: object
              properties:
                summer:
                  type: string
                  example: "1А"
            images:
              type: array
              items:
                type: object
                properties:
                  data:
                    type: string
                    example: "<картинка1>"
                  title:
                    type: string
                    example: "Седловина"
    responses:
      200:
        description: Успешное добавление перевала
        schema:
          type: object
          properties:
            status:
              type: integer
              example: 200
            message:
              type: string
              example: "Отправлено успешно"
            id:
              type: integer
              example: 4
      400:
        description: Некорректный запрос
      500:
        description: Ошибка сервера
    """
    pereval_data = request.get_json()

    required_fields = ["beauty_title", "title", "user", "coords", "images"]
    if not pereval_data or not all(field in pereval_data for field in required_fields):
        return jsonify({
            "status": 400,
            "message": "Некоторые обязательные поля отсутствуют",
            "id": None
        }), 400

    db = PerevalDatabase()
    new_id, error = db.add_pereval(pereval_data)

    if error:
        return jsonify({
            "status": 500,
            "message": f"Ошибка: {error}",
            "id": None
        }), 500

    return jsonify({
        "status": 200,
        "message": "Отправлено успешно",
        "id": new_id
    }), 200

@app.route('/submitData/<int:pereval_id>', methods=['GET'])
def get_pereval(pereval_id):
    """
        Получить запись о перевале по ID
        ---
        tags:
          - Pereval
        parameters:
          - name: pereval_id
            in: path
            type: integer
            required: true
            description: ID перевала
        responses:
          200:
            description: Успешный ответ с данными перевала
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 4
                date_added:
                  type: string
                  example: "2025-11-01 13:18:13"
                data:
                  type: object
                  example: { "title": "Тестовый", "user": {"email": "test@test.ru"} }
                moderation_status:
                  type: string
                  example: "new"
          404:
            description: Перевал не найден
          500:
            description: Ошибка подключения к БД
        """

    conn = db.connection
    if not conn:
        return jsonify({"status": 500, "message": "Нет подключения к БД"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, date_added, raw_data, status FROM pereval_added WHERE id = %s", (pereval_id,))
            row = cur.fetchone()
            if not row:
                return jsonify({"status": 404, "message": f"Перевал с id={pereval_id} не найден"}), 404

            return jsonify({
                "status": 200,
                "id": row["id"],
                "date_added": row["date_added"],
                "data": row["raw_data"],
                "moderation_status": row["status"]
            })
    except Exception as e:
        return jsonify({"status": 500, "message": f"Ошибка: {e}"}), 500


@app.route('/submitData/<int:pereval_id>', methods=['PATCH'])
def update_pereval(pereval_id):
    """
        Редактировать запись о перевале (если статус = 'new')
        ---
        tags:
          - Pereval
        consumes:
          - application/json
        parameters:
          - name: pereval_id
            in: path
            type: integer
            required: true
            description: ID перевала для обновления
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                beauty_title:
                  type: string
                  example: "пер. "
                title:
                  type: string
                  example: "Обновлённый перевал"
                other_titles:
                  type: string
                  example: "Новый вариант"
                coords:
                  type: object
                  properties:
                    latitude:
                      type: string
                      example: "55.727739"
                    longitude:
                      type: string
                      example: "37.606945"
                    height:
                      type: string
                      example: "1200"
                images:
                  type: array
                  items:
                    type: object
                    properties:
                      data:
                        type: string
                        example: "<новая картинка>"
                      title:
                        type: string
                        example: "Обновлённый вид"
        responses:
          200:
            description: Успешное обновление записи
            schema:
              type: object
              properties:
                state:
                  type: integer
                  example: 1
                message:
                  type: string
                  example: "Запись успешно обновлена"
          400:
            description: Ошибка запроса или изменение запрещённых полей
          404:
            description: Запись не найдена
          500:
            description: Ошибка подключения или SQL
        """
    conn = db.connection
    if not conn:
        return jsonify({"state": 0, "message": "Нет подключения к базе данных"}), 500

    data = request.get_json()
    if not data:
        return jsonify({"state": 0, "message": "Пустое тело запроса"}), 400

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT status, raw_data FROM pereval_added WHERE id = %s", (pereval_id,))
            row = cur.fetchone()
            if not row:
                return jsonify({"state": 0, "message": f"Перевал с id={pereval_id} не найден"}), 404

            if row["status"] != "new":
                return jsonify({"state": 0, "message": "Редактировать можно только перевалы со статусом 'new'"}), 400

            old_user = row["raw_data"].get("user", {})
            new_user = data.get("user", {})

            if (old_user.get("email") != new_user.get("email") or
                old_user.get("fam") != new_user.get("fam") or
                old_user.get("name") != new_user.get("name") or
                old_user.get("phone") != new_user.get("phone")):
                return jsonify({"state": 0, "message": "Изменение ФИО, почты и телефона запрещено"}), 400

            cur.execute(
                """
                UPDATE pereval_added
                SET raw_data = %s::jsonb,
                    images = %s::jsonb
                WHERE id = %s
                """,
                (
                    json.dumps(data, ensure_ascii=False),
                    json.dumps(data.get("images", []), ensure_ascii=False),
                    pereval_id
                )
            )
            conn.commit()
            return jsonify({"state": 1, "message": "Запись успешно обновлена"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"state": 0, "message": f"Ошибка: {e}"}), 500

@app.route('/submitData', methods=['GET'])
def get_perevals_by_email():
    """
        Получить все перевалы пользователя по email
        ---
        tags:
          - Pereval
        parameters:
          - name: user__email
            in: query
            type: string
            required: true
            description: Почта пользователя, чьи перевалы нужно получить
            example: test@test.ru
        responses:
          200:
            description: Список перевалов пользователя
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 2
                  date_added:
                    type: string
                    example: "2025-11-02 12:33:00"
                  data:
                    type: object
                    example: { "title": "Пхия", "coords": {"latitude": "45.38"} }
                  status:
                    type: string
                    example: "new"
          400:
            description: Не передан параметр user__email
          500:
            description: Ошибка подключения к БД
        """
    email = request.args.get('user__email')
    if not email:
        return jsonify({"status": 400, "message": "Не указан параметр user__email"}), 400

    conn = db.connection
    if not conn:
        return jsonify({"status": 500, "message": "Нет подключения к БД"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, date_added, raw_data, status FROM pereval_added")
            rows = cur.fetchall()
            result = []
            for row in rows:
                user = row["raw_data"].get("user", {})
                if user.get("email") == email:
                    result.append({
                        "id": row["id"],
                        "date_added": row["date_added"],
                        "data": row["raw_data"],
                        "status": row["status"]
                    })
            return jsonify(result)
    except Exception as e:
        return jsonify({"status": 500, "message": f"Ошибка: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
