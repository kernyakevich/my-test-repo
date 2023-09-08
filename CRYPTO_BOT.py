import requests
import json
import time

class Account:
    def __init__(self, balance):
        self.balance = balance

    def buy(self, price):
        quantity = self.balance / price
        self.balance = 0
        return quantity

    def sell(self, price, quantity):
        self.balance += price * quantity

    def get_balance(self):
        return self.balance

    def get_profit_loss(self, initial_balance):
        return self.balance - initial_balance

def get_pair_data(api_key, secret_key, symbol):
    url = f'https://api.bybit.com/v2/public/tickers'

    try:
        response = requests.get(url, params={'symbol': symbol})
        data = json.loads(response.text)

        if 'result' in data and data['result']:
            price = data['result'][0]['last_price']
            return float(price)
        else:
            print(f"Pair {symbol} not found.")
            return None

    except requests.exceptions.RequestException as e:
        print('Error occurred during API request.')
        return None

def execute_trades(api_key, secret_key, symbol):
    balance = Account(1000)
    holding = False
    quantity = 0
    previous_price = get_pair_data(api_key, secret_key, symbol)

    while True:
        price = get_pair_data(api_key, secret_key, symbol)

        if price is not None:
            if not holding and price < previous_price:
                quantity = balance.buy(price)
                price_buy = price
                print(f"Buy {symbol} at {price}. Quantity: {quantity:.8f}. Balance: {balance.get_balance()}")
                holding = True

            elif holding and price > previous_price and price > price_buy:
                balance.sell(price, quantity)
                print(f"Sell {symbol} at {price}. Balance: {balance.get_balance()}")
                holding = False

            previous_price = price

        time.sleep(1)

pair = input("Enter pair: ")

execute_trades(api_key='YOUR_API_KEY', secret_key='YOUR_SECRET_KEY', symbol=pair)

