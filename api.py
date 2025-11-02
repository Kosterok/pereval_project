from flask import Flask, request, jsonify
from db import PerevalDatabase

app = Flask(__name__)


@app.route("/submitData", methods=["POST"])
def submit_data():
    """
    REST-метод добавления данных о перевале.
    Принимает JSON, проверяет поля и записывает в базу.
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
