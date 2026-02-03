from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from chatbot_enhanced import EnhancedChatbot

app = Flask(__name__)
CORS(app)

# Initialize chatbot
chatbot = EnhancedChatbot()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please type a message."})

        # ✅ CORRECT METHOD
        bot_reply = chatbot.chat(user_message)

        return jsonify({
            "response": bot_reply
        })

    except Exception as e:
        print("CHAT ERROR:", e)  # <-- IMPORTANT for debugging
        return jsonify({
            "response": "Sorry, something went wrong on the server."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
