import time
from datetime import datetime
import asyncio
# https://github.com/Kucoin/kucoin-python-sdk
# @TODO: what if don't use this package?
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient

from okx import OKX
from strategry import MarketMaker
import settings

last_time = time.time()
async def handle_data(data):
    global last_time
    ts = data['time'] / 1000
    formated = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')

    # with less than one second, ignore.
    if (time.time() - last_time) < 1:
        return

    # strategy
    #@TODO: now the data processing step is not too time consuming.
    # if it not very time consuming, process it with another process/ at other computer
    bid, ask = mm.calculate(data)

    # @TODO: make these two function to be run asynchronously
    # send order at marker exchange
    print(formated, 'request submited')
    okx.buy('ETH-USDT', bid['price'], bid['size'])
    okx.sell('ETH-USDT', ask['price'], ask['size'])


    # @TODO: check if marker exchange order is filled, send order to taker exchange
    pass
    
    last_time = time.time()

    print(formated, 'request finished')

async def main():
    async def deal_msg(msg):
        if msg['topic'] == '/market/ticker:ETH-USDT':
            data = msg["data"]
            ts = data['time'] / 1000
            formated = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
            print(f'{formated}: got ETH-USDT tick')
            asyncio.ensure_future(handle_data(data), loop=loop)

    client = WsToken()

    ws_client = await KucoinWsClient.create(None, client, deal_msg, private=False)
    # @TODO: what if there are multiple symbol-pairs?
    await ws_client.subscribe('/market/ticker:ETH-USDT')
    while True:
        await asyncio.sleep(60, loop=loop)


if __name__ == "__main__":
    # @TODO: what if there are multiple exchange?
    okx = OKX(settings.apikey, settings.secretkey, settings.passphrase)
    # @TODO: what if there are multiple strategy?
    mm = MarketMaker('ETH-USDT', 0.01)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    
    