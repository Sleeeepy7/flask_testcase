import requests
import base58


ADDRESS = "TTEnyr3zYcVXixuG8cuzoW2kAjd6DKUFXa"

CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT trc20

API_URL_BASE = "https://api.trongrid.io/"

METHOD_BALANCE_OF = "balanceOf(address)"


def address_to_parameter(addr):
    return "0" * 24 + base58.b58decode_check(addr)[1:].hex()


def amount_to_parameter(amount):
    return "%064x" % amount


def get_balance(address=ADDRESS):
    url = API_URL_BASE + "wallet/triggerconstantcontract"
    payload = {
        "owner_address": base58.b58decode_check(address).hex(),
        "contract_address": base58.b58decode_check(CONTRACT).hex(),
        "function_selector": METHOD_BALANCE_OF,
        "parameter": address_to_parameter(address),
    }
    resp = requests.post(url, json=payload)
    data = resp.json()

    if data["result"].get("result", None):
        print(data)
        val = data["constant_result"][0]
        balance = int(val, 16) / 1_000_000
        print(f"USDT TRC20 balance: {balance:.6f}")
        return balance
    else:
        print("Error:", bytes.fromhex(data["result"]["message"]).decode())
        return 0


get_balance()


import tronpy
from tronpy import Tron
from tronpy.providers import HTTPProvider

tron_apikey = "ваш токен"  # получить свой можно через https://www.trongrid.io/register
provider = HTTPProvider(timeout=30, api_key=tron_apikey)
provider.sess.trust_env = False
client = Tron(provider)


token_usdt = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
contract_usdt = client.get_contract(token_usdt)
search_address = "TTEnyr3zYcVXixuG8cuzoW2kAjd6DKUFXa"
amount = round(contract_usdt.functions.balanceOf(search_address) / tronpy.TRX, 4)
print(amount)
