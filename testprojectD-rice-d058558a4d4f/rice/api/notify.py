import os
import json

import requests
from .. import db
from ..models import User

api_uri = 'http://sms-api.luosimao.com/v1/send_batch.json'
api_key = os.getenv('SMS_API_KEY')

def notify_all_admin(msg):
    all_users = User.query.all()
    mobile_list = ",".join([u.phone_number for u in all_users])
    send_batch(mobile_list, msg)

def send_batch(mobile_list, message):
    resp = requests.post(api_uri, auth=('api', 'key-' + api_key), data=dict(
        mobile_list=mobile_list,
        message=message
    ))
    json_resp = json.loads(resp.content.decode('utf-8'))
    if json_resp['error'] != 0:
        print("msg:", json_resp['msg'])
