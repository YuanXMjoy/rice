from datetime import datetime

from flask import request, jsonify, current_app

from .. import db
from . import api
from ..models import Order
from .notify import notify_all_admin

@api.route('/order')
def get_orders():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 5, type=int)
    pagination = Order.query.paginate(
        page, per_page=page_size)
    orders = pagination.items
    return jsonify({
        'page': page,
        'pages': pagination.pages,
        'items': [order.to_json() for order in orders]
    })

@api.route('/order', methods=['POST'])
def new_order():
    json_data = {
        'product_name': request.form.get('product_name', type=str),
        'will_price': request.form.get('will_price', type=int),
        'amount': request.form.get('amount', type=int),
        'customer': request.form.get('customer', type=str),
        'phone_number': request.form.get('phone_number', type=str),
        'time': datetime.now()
    }
    order = Order.from_json(json_data)
    db.session.add(order)
    db.session.commit()
    msg = "收到一份新大宗订单：{product_name} {amount}吨，心理价位{will_price}元/斤，{customer}，{phone_number}【来米】".format(
        product_name=json_data['product_name'],
        will_price=json_data['will_price'] / 100.0,
        amount=json_data['amount'],
        customer=json_data['customer'],
        phone_number=json_data['phone_number']
    )
    notify_all_admin(msg)
    return jsonify({
        'ok': True,
        'item': order.to_json()
    }), 201
