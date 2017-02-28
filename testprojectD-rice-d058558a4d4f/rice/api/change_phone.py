from flask import request, jsonify

from .. import db
from ..models import User
from . import api

@api.route('/change_phone', methods=['PUT'])
def change_phone():
    username = request.form.get('username', type=str)
    password = request.form.get('password', type=str)
    new_phone_number = request.form.get('phone_number', type=str)

    u = User.query.filter_by(username=username).first()
    if u is None:
        return jsonify({
            "ok": False,
            "errmsg": "User not found."
        })
    if u.verify_password(password):
        u.phone_number = new_phone_number
        db.session.add(u)
        db.session.commit()
        return jsonify({
            "ok": True,
        })

    return jsonify({
        "ok": False,
        "errmsg": "Password not match."
    })
