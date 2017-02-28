from flask import request, jsonify, current_app
from .. import db
from . import api
from ..models import Rice

@api.route('/rice')
def get_rices():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 5, type=int)
    pagination = Rice.query.paginate(
        page, per_page=page_size)
    rices = pagination.items
    return jsonify({
        'page': page,
        'pages': pagination.pages,
        'items': [r.to_json() for r in rices]
    })

@api.route('/rice', methods=['POST'])
def new_rice():
    json_data = {
        'product_name': request.form.get('product_name', type=str),
        'min_price': request.form.get('min_price', type=int),
        'avaliable_weight': request.form.get('avaliable_weight', type=int),
        'url': request.form.get('url', type=str)
    }
    rice = Rice.from_json(json_data)
    # Prevent duplicate product name
    if Rice.query.filter_by(product_name=rice.product_name).first():
        return jsonify({
            'ok': False,
            'errmsg': 'Duplicate product_name: {}.'.format(rice.product_name),
        }), 400
    db.session.add(rice)
    db.session.commit()
    return jsonify({
        'ok': True,
        'item': rice.to_json()
    }), 201

@api.route('/rice/<int:id>', methods=['PUT'])
def update_rice(id):
    rice = Rice.query.get(id)
    if rice is None:
        return jsonify({
            "ok": False,
            "errmsg": "Product not found."
        })

    json_data = {
        'product_name': request.form.get('product_name', type=str),
        'min_price': request.form.get('min_price', type=int),
        'avaliable_weight': request.form.get('avaliable_weight', type=int),
        'url': request.form.get('url', type=str)
    }
    new_rice = Rice.from_json(json_data)
    rice.product_name = new_rice.product_name
    rice.min_price = new_rice.min_price
    rice.avaliable_weight = new_rice.avaliable_weight
    rice.url = new_rice.url

    db.session.add(rice)
    db.session.commit()
    return jsonify({
        "ok": True,
        "item": rice.to_json()
    })

@api.route('/rice/<int:id>', methods=['DELETE'])
def delete_rice(id):
    rice = Rice.query.get(id)
    if rice is None:
        return jsonify({
            "ok": False,
            "errmsg": "Product not found."
        })
    db.session.delete(rice)
    db.session.commit()
    return jsonify({
        'ok': True,
    })

@api.route('/rice/<int:id>')
def get_rice(id):
    rice = Rice.query.get(id)
    if rice is None:
        return jsonify({
            "ok": False,
            "errmsg": "Product not found."
        })
    return jsonify({
        "ok": True,
        "item": rice.to_json()
    })
