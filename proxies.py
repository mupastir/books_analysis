import asyncio
import os
from proxybroker import Broker


async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        proxy_type = [k for k in proxy.types.keys()][-1].lower()
        if os.path.isfile('proxies.txt'):
            with open('proxies.txt', 'a') as pl:
                pl.write(f'\n{proxy_type}://{proxy.host}')
        else:
            with open('proxies.txt', 'w') as pl:
                pl.write(f'{proxy_type}://{proxy.host}')
        print('Found proxy: %s' % proxy)


proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(
    broker.find(types=['HTTP', 'HTTPS'], limit=10),
    show(proxies))
loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)
