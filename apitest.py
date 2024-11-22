from binance_api import setup_exchange

exchange = setup_exchange("dein_api_key", "dein_api_secret")
print(exchange.fetch_status())
