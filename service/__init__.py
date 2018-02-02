import base64
import asyncio
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
from service.spider import all_search

loop = asyncio.get_event_loop()

def create_app():
    app = web.Application()
    # 产生加密所需的密钥
    fernet_key = fernet.Fernet.generate_key()
    # 产生base64编码, secret_key一定要是32 url-safe base64-encoded bytes
    secret_key = base64.urlsafe_b64decode(fernet_key)
    # 把session数据存在cookie里面,经过编码
    setup(app, EncryptedCookieStorage(secret_key))

    return app

app = create_app()

from .api import api
app.add_subapp('/api/', api)