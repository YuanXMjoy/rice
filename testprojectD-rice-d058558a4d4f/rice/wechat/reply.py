import os

from flask import request
from wechat_sdk.messages import EventMessage
from wechat_sdk.exceptions import ParseError

from . import wechat, sdk

welcome_message = "欢迎关注来米，米线专用米、质优价低\n还能做大宗预定哦～"
business_line_message = "大客户专线电话: XXXXXXXXXXX"
service_line_message = "来米客服电话：XXXXXXXXXXX"


@wechat.route('/')
def validate_server():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    if sdk.check_signature(signature, timestamp, nonce):
        return echostr
    else:
        return "Not match.\ntoken: {}, appid: {}, appsecret: {}" \
            .format(
                os.getenv('WECHAT_TOKEN'),
                os.getenv('WECHAT_APPID'),
                os.getenv('WECHAT_APPSECRET')
            )


@wechat.route('/', methods=['POST'])
def handle_wechat_message():
    data = request.data.decode('utf-8')
    try:
        sdk.parse_data(data)
    except ParseError as e:
        return "Invalid body text"

    if isinstance(sdk.message, EventMessage):
        return handle_event_message(sdk.message)

    return sdk.response_none()

def handle_event_message(message):
    if message.type == 'subscribe':
        return sdk.response_text(welcome_message)
    if message.type == 'click':
        return handle_click(message)

    return sdk.response_none()


def handle_click(message):
    if message.key == 'business_line_number':
        return sdk.response_text(business_line_message)
    if message.key == 'laimi_service_number':
        return sdk.response_text(service_line_message)

    return sdk.response_none()
