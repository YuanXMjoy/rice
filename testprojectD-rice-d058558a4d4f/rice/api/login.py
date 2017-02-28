from flask import request, jsonify
import json
from . import api
from ..models import User

@api.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', type=str)
    password = request.form.get('password', type=str)

    u = User.query.filter_by(username=username).first()
    if u is None:
        return jsonify({
            "ok": False,
            "errmsg": "User not found."
        })
    if u.verify_password(password):
        return jsonify({
            "ok": True,
            "phone_number": u.phone_number
        })

    return jsonify({
        "ok": False,
        "errmsg": "Password not match."
    })
