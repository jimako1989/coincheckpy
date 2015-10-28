coincheckpy
======
Python wrapper for Coincheck API.

Dependencies
======
python-requests is required.

Usage
======

Include the coincheckpy module and create an coincheckpy instance with your account credentials. For trading, a key and a secret key must be provided.

	import coincheckpy

	coincheck = coincheckpy.API(environment="live", key="AaBbCc012...", secret_key="123a456...")

**Method names are referred by the part of HTML label name after #, which you can see [Coincheck API web page](https://coincheck.jp/documents/exchange/api).**

**In the label name, you don't forget to replace all '-'s with '_'.**


Examples
======

### Get latest BTC price
	coincheck.ticker()

### Get an order book
    coincheck.order_book()

### Make sure my balance
    coincheck.account_balance()

### Publish a new order to exchange
For example if you'd like buy 0.001 BTC as 28000 JPY/BTC, you need to specify following parameters.

	coincheck.order_new(pair="btc_jpy",order_type="buy",rate=28000,amount=0.001)

BTC Price Streaming
======
Create a custom streamer class to setup how you want to handle the data.
Each tick is sent through the `on_success` and `on_error` functions.
You can override these functions to handle the streaming data.

Initialize an instance of your custom streamer, and start connecting to the stream.

    stream = coincheckpy.Streamer(environment=DOMAIN, heartbeat=1.0)
    stream.start()



Copyright (c) 2015 jimako1989
