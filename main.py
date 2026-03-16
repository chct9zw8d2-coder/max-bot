from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "MAX BOT ONLINE"

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    print("EVENT:", data)

    try:
        message = data["message"]["text"].lower()
        chat_id = data["message"]["chat_id"]

        if message == "привет":
            return jsonify({
                "chat_id": chat_id,
                "text": "привет"
            })

    except:
        pass

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
