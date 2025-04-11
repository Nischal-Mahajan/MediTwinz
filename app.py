from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Set your API key directly or via environment variable
openai.api_key = "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"  # <-- Replace this or use env var

@app.route("/")
def index():
    return render_template("home.html")  # Make sure index.html is in templates/

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]

    # Generate response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    bot_reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
