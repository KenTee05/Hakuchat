"""Flask-palvelin hakuchatille. Kuuntelee vain paikallista konetta."""
from flask import Flask, jsonify, request, send_from_directory

from chat_core import chat

app = Flask(__name__, static_folder="static")


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.post("/api/chat")
def api_chat():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Pyyntö ei sisältänyt kelvollista JSON-dataa."}), 400
    messages = payload.get("messages")
    if not isinstance(messages, list):
        return jsonify({"error": "messages-kentän pitää olla lista."}), 400
    try:
        result = chat(messages)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    except Exception:
        app.logger.exception("Chat-pyynnön käsittely epäonnistui")
        return jsonify({"error": "Palvelimella tapahtui virhe. Tarkista terminaalin loki."}), 500


if __name__ == "__main__":
    # Älä vaihda host-arvoa 0.0.0.0:ksi: API-avain on käytössä paikallisesti.
    app.run(host="127.0.0.1", port=5000, debug=False)
