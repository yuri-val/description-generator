import os
import openai
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ініціалізація API-ключа OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY", "<demo>")

# Prompt для системного повідомлення
SYSTEM_PROMPT = """
Ти – помічник інтернет-магазину, який генерує привабливі описи товарів українською мовою.
Отримуючи характеристики товару у форматі "Свойство: Значение", ти повинен згенерувати опис, який привертає увагу покупців.
"""

# Завантаження попередньо згенерованих повідомлень з файлу data.json
with open("data.json", "r", encoding="utf-8") as f:
    messages = json.load(f)


@app.route("/generate-description", methods=["POST"])
def generate_description():
    """
    Ендпойнт для генерації опису товару.
    Очікує JSON із полем `parameters`, яке містить характеристики товару у форматі "Свойство: Значение".
    """
    try:
        # Отримуємо дані з запиту
        data = request.get_json(force=True)
        parameters = data.get("parameters", "").strip()

        if not parameters:
            return jsonify({"error": "Поле 'parameters' не може бути порожнім"}), 400

        # Формуємо запит до моделі

        messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

        messages.append(
            {
                "role": "user",
                "content": f"Я маю характеристики та параметри товару. потрібно згенерувати опис для мого інтернет магазину:\n{parameters}",
            }
        )

        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Можна замінити на GPT-4 або іншу модель
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
        )

        # Отримуємо відповідь
        description = response.choices[0].message.content
        print(description)
        return jsonify({"description": description}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5566, debug=True)
