import os

from flask import Blueprint
from wechat_sdk import WechatConf, WechatBasic

conf = WechatConf(
    token=os.getenv('WECHAT_TOKEN'),
    appid=os.getenv('WECHAT_APPID'),
    appsecret=os.getenv('WECHAT_APPSECRET'),
    encrypt_mode="normal"
)

sdk = WechatBasic(conf=conf)

wechat = Blueprint('wechat', __name__)

from . import reply
