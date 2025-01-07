from flask import Blueprint, request, jsonify

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/test-webhook", methods=["POST"])
def test_webhook():
    data = request.json
    print("Получен вебхук:", data)
    return jsonify({"received": True}), 200
