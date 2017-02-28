from flask import request, jsonify

from .. import db
from ..models import User
from . import api

@api.route('/change_password', methods=["PUT"])
def change_password():
    username = request.form.get('username', type=str)
    old_password = request.form.get('old_password', type=str)
    new_password = request.form.get('new_password', type=str)

    u = User.query.filter_by(username=username).first()
    if u is None:
        return jsonify({
            "ok": False,
            "errmsg": "User not found."
        })

    if u.verify_password(old_password):
        u.password = new_password
        return jsonify({
            "ok": True
        })

    return jsonify({
        "ok": False,
        "errmsg": "Password not match."
    })
