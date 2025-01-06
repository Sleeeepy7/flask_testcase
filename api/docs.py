create_transaction_doc = {
    "tags": ["Transactions"],
    "summary": "Создание транзакции",
    "description": "Создаёт новую транзакцию с автоматическим расчётом комиссии.",
    "consumes": ["application/json"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "ID пользователя"},
                    "amount": {"type": "number", "description": "Сумма транзакции"},
                },
                "required": ["user_id", "amount"],
            },
        }
    ],
    "responses": {
        "201": {
            "description": "Транзакция успешно создана",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "user_id": {"type": "integer"},
                    "amount": {"type": "number"},
                    "commission": {"type": "number"},
                    "status": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                },
            },
        },
        "400": {"description": "Некорректные данные."},
        "500": {"description": "Ошибка сервера."},
    },
}

cancel_transaction_doc = {
    "tags": ["Transactions"],
    "summary": "Отмена транзакции",
    "description": "Отменяет транзакцию с указанным ID.",
    "consumes": ["application/json"],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "transaction_id": {"type": "integer"},
                },
                "required": ["transaction_id"],
            },
        }
    ],
    "responses": {
        "200": {
            "description": "Транзакция успешно отменена",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "user_id": {"type": "integer"},
                            "status": {"type": "string"},
                        },
                    }
                }
            },
        },
        "400": {"description": "Некорректные данные."},
        "404": {"description": "Транзакция не найдена."},
    },
}

check_transaction_doc = {
    "tags": ["Transactions"],
    "summary": "Проверка транзакции",
    "description": "Получить информацию о транзакции по её ID.",
    "parameters": [
        {
            "in": "query",
            "name": "transaction_id",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID транзакции",
        }
    ],
    "responses": {
        "200": {
            "description": "Информация о транзакции",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "user_id": {"type": "integer"},
                            "amount": {"type": "number"},
                            "commission": {"type": "number"},
                            "status": {"type": "string"},
                            "created_at": {"type": "string", "format": "date-time"},
                        },
                    }
                }
            },
        },
        "400": {"description": "Некорректные данные."},
        "404": {"description": "Транзакция не найдена."},
    },
}
