from flask import Flask, request, jsonify
from db import PerevalDatabase
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

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


if __name__ == "__main__":
    app.run(debug=True)
