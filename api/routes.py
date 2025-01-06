from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flasgger import swag_from

from core.database import SessionLocal
from services.transaction_service import create_transaction, cancel_transaction, get_transaction_by_id

from api.docs import create_transaction_doc, cancel_transaction_doc, check_transaction_doc

api_bp = Blueprint("api", __name__)


@api_bp.route("/create_transaction", methods=["POST"])
@swag_from(create_transaction_doc)
def create_transaction_route():
    """
    Создать транзакцию.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    if not user_id or not amount:
        return jsonify({"error": "user_id и amount обязательны."}), 400

    with SessionLocal() as db:
        try:
            transaction = create_transaction(db, user_id, amount)
            return jsonify(
                {
                    "id": transaction.id,
                    "user_id": transaction.user_id,
                    "amount": transaction.amount,
                    "commission": transaction.commission,
                    "status": transaction.status.value,
                    "created_at": transaction.created_at,
                }
            ), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404  # только dev разумется выдает str(e)
        except SQLAlchemyError as e:
            return jsonify({"error": "Не удалось создать транзакцию."}), 500


@api_bp.route("/cancel_transaction", methods=["POST"])
@swag_from(cancel_transaction_doc)
def cancel_transaction_route():
    """
    Отменить транзакцию.
    """
    data = request.get_json()
    transaction_id = data.get("transaction_id")

    if not transaction_id:
        return jsonify({"error": "transaction_id обязателен."}), 400

    with SessionLocal() as db:
        try:
            transaction = cancel_transaction(db, transaction_id)
            return jsonify(
                {
                    "id": transaction.id,
                    "user_id": transaction.user_id,
                    "status": transaction.status.value,
                }
            ), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404  # только dev разумется выдает str(e)
        except SQLAlchemyError as e:
            return jsonify({"error": "Не удалось отменить транзакцию."}), 500


@api_bp.route("/check_transaction", methods=["GET"])
@swag_from(check_transaction_doc)
def check_transaction_route():
    """
    Получить информацию о транзакции.
    """
    transaction_id = request.args.get("transaction_id", type=int)

    if not transaction_id:
        return jsonify({"error": "transaction_id обязателен."}), 400

    with SessionLocal() as db:
        try:
            transaction = get_transaction_by_id(db, transaction_id)
            return jsonify(
                {
                    "id": transaction.id,
                    "user_id": transaction.user_id,
                    "amount": transaction.amount,
                    "commission": transaction.commission,
                    "status": transaction.status.value,
                    "created_at": transaction.created_at,
                }
            ), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404  # только dev разумется выдает str(e)
        except SQLAlchemyError as e:
            return jsonify({"error": "Не удалось получить информацию о транзакции"}), 500
