coincheckpy
======
Python wrapper for Coincheck API.

Dependencies
======
Requests and Pandas libraries are required.

Usage
======

Include the coincheckpy module and create an coincheckpy instance with your account credentials. For trading, a key and a secret key must be provided.

	import coincheckpy

	coincheck = coincheckpy.API(environment="live", key="AaBbCc012...", secret_key="123a456...")

**Method names are referred by the part of HTML label name after #, which you can see [Coincheck API web page](https://coincheck.jp/documents/exchange/api).**

**In the label name, you don't forget to replace all '-'s with '_'.** (e.g. order-opens -> order_opens)


Examples
======

### Get the latest BTC price
	coincheck.ticker()

### Get an order book
    coincheck.order_book()

### Make sure your balance
    coincheck.account_balance()

### Publish a new order to exchange
For example, if you'd like to buy 0.001 BTC as 28000 JPY/BTC, you need to specify following parameters.

	coincheck.order_new(pair="btc_jpy",order_type="buy",rate=28000,amount=0.001)

### Get the historical prices of JPY/BTC
If you'd like to get the historical prices, you can set a parameter chosen of three, '10_minutes', '1_hour' and '1_day'.
It returns an useful pandas series object.

	coincheck.get_prices('10_minutes')


BTC Price Streaming
======
Create a custom streamer class to setup how you want to handle the data.
Each tick is sent through the `on_success` and `on_error` functions.
You can override these functions to handle the streaming data.

Initialize an instance of your custom streamer, and start connecting to the stream.

    stream = coincheckpy.Streamer(environment=DOMAIN, heartbeat=1.0)
    stream.start()



Copyright (c) 2015 jimako1989
