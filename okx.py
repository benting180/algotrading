import time
import json
from datetime import datetime

import base64
import hmac
import hashlib

import requests

import settings


class OKX:
    def __init__(self, api_key, secret_key, passphrase):
        self.endpoint = "https://www.okx.com"
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
    
    def _send(self, method, body, uri):
        # generate header, signature, execute request sending

        body = json.dumps(body)
        timestamp = (
            str(time.time()).split(".")[0]
            + "."
            + str(time.time()).split(".")[1][:3]
        )
        prehash = timestamp + method.upper() + uri + str(body)
        mac = hmac.new(
            key=bytes(self.secret_key, "utf-8"),
            msg=bytes(prehash, "utf-8"),
            digestmod="sha256"
        )
        d = mac.digest()
        sign = base64.b64encode(d)

        headers = {
            "Content-Type": "application/json",
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": sign,
            "OK-ACCESS-TIMESTAMP": str(timestamp),
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "x-simulated-trading": "1",
        }
        url = self.endpoint + uri
        request = requests.request(method=method.upper(), url=url, data=body, headers=headers)
        # @TODO: exception handling
        return request.json()


    def buy(self, symbol, price, quantity):
        uri = "/api/v5/trade/order"
        # body = {
        #     "instId": "BTC-USDT",
        #     "ordType": "limit",
        #     "px": 1000,
        #     "side": "buy",
        #     "sz": 1,
        #     "tdMode": "cash"
        # }
        body = {"side": "buy", "tdMode": "cash", "ordType": "limit",}
        body['instId'] = symbol
        body['px'] = price
        body['sz'] = quantity
        print("sending buy order")
        return self._send('post', body=body, uri=uri)
    
    def sell(self, symbol, price, quantity):
        uri = "/api/v5/trade/order"
        body = {"side": "sell", "tdMode": "cash", "ordType": "limit",}
        body['instId'] = symbol
        body['px'] = price
        body['sz'] = quantity
        print("sending sell order")
        return self._send('post', body=body, uri=uri)


if __name__ == '__main__':
    apikey = settings.apikey
    secretkey = settings.secretkey
    passphrase = settings.passphrase
    okx = OKX(api_key=apikey, secret_key=secretkey, passphrase=passphrase)
    okx.buy("BTC-USDT", 1000, 1)
    okx.sell("BTC-USDT", 1000, 1)
    # @TODO: handle the order information. e.g. save it into somewhere
