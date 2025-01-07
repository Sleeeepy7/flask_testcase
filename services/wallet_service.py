import requests
import base58

API_URL_BASE = "https://api.trongrid.io/"
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT TRC20
METHOD_BALANCE_OF = "balanceOf(address)"


def address_to_parameter(addr: str) -> str:
    return "0" * 24 + base58.b58decode_check(addr)[1:].hex()


def get_usdt_balance(wallet_address: str) -> float:
    url = API_URL_BASE + "wallet/triggerconstantcontract"
    payload = {
        "owner_address": base58.b58decode_check(wallet_address).hex(),
        "contract_address": base58.b58decode_check(USDT_CONTRACT).hex(),
        "function_selector": METHOD_BALANCE_OF,
        "parameter": address_to_parameter(wallet_address),
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        if data["result"].get("result", None):
            value_hex = data["constant_result"][0]
            balance = int(value_hex, 16) / 1_000_000
            return round(balance, 6)
        else:
            return 0.0
    except requests.RequestException as e:
        print(f"Ошибка при получении баланса: {e}")
        return 0.0
