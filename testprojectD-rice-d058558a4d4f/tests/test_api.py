import unittest
import json
from flask import current_app, url_for
from rice import create_app, db
from rice.models import Rice, User, Order

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_rices(self):
        # Add a rice product
        rices = [
            Rice(product_name="泰国黑米", min_price=100, avaliable_weight=100, url="http://www.example.com/"),
            Rice(product_name="黑米", min_price=100, avaliable_weight=100, url="http://www.example.com/"),
            Rice(product_name="东北黑米", min_price=100, avaliable_weight=100, url="http://www.example.com/"),
            Rice(product_name="东北大米", min_price=100, avaliable_weight=100, url="http://www.example.com/"),
            Rice(product_name="大米", min_price=100, avaliable_weight=100, url="http://www.example.com/"),
            Rice(product_name="日本黑米", min_price=100, avaliable_weight=100, url="http://www.example.com/"),
            Rice(product_name="泰国紫米", min_price=100, avaliable_weight=100, url="http://www.example.com/"),
            Rice(product_name="法国黑米", min_price=100, avaliable_weight=100, url="http://www.example.com/"),
            Rice(product_name="兰州黑米", min_price=100, avaliable_weight=100, url="http://www.example.com/"),
            Rice(product_name="西班牙黑米", min_price=100, avaliable_weight=100, url="http://www.example.com/")
        ]
        db.session.add_all(rices)
        db.session.commit()

        # Get rices
        page = 2
        page_size = 5
        resp = self.client.get(
            url_for('api.get_rices', page=page, page_size=page_size))
        self.assertTrue(resp.status_code == 200)
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['page'], page)
        self.assertEqual(json_resp['pages'], len(rices) // page_size)
        items = rices[(page - 1) * page_size:]
        for i, r in enumerate(items):
            get_rice = Rice.from_json(json_resp['items'][i])
            self.assertEqual(get_rice.product_name, r.product_name)
            self.assertEqual(get_rice.min_price, r.min_price)
            self.assertEqual(get_rice.avaliable_weight, r.avaliable_weight)
            self.assertEqual(get_rice.url, r.url)

    def test_new_rice(self):
        json_rice = {
            'product_name': '泰国黑米',
            'min_price': 100,
            'avaliable_weight': 100,
            'url': 'http://www.example.com/'
        }
        resp = self.client.post(
            url_for('api.new_rice'),
            data=json_rice)
        self.assertEqual(resp.status_code, 201)
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['ok'], True)
        resp_item = json_resp['item']
        for k, v in resp_item.items():
            if k == 'id':
                continue
            self.assertEqual(v, json_rice[k])

        rice_database = Rice.query.filter_by(product_name=json_rice['product_name']).first()
        for k, v in json_rice.items():
            self.assertEqual(v, getattr(rice_database, k))

        # Add duplicate in product_name
        rice_dup = {
            'product_name': '泰国黑米',
            'min_price': 300,
            'avaliable_weight': 200,
            'url': 'http://www.example.cn/'
        }
        resp = self.client.post(
            url_for('api.new_rice'),
            data=json_rice)
        self.assertEqual(resp.status_code, 400)
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['ok'], False)
        self.assertEqual(json_resp['errmsg'], 'Duplicate product_name: {}.'.format(rice_dup['product_name']))

    def test_get_orders(self):
        orders = [
            Order(product_name="泰国黑米", will_price=100, amount=100, customer="王大米", phone_number="13900000000"),
            Order(product_name="黑米", will_price=100, amount=100, customer="王大米", phone_number="13900000000"),
            Order(product_name="东北黑米", will_price=100, amount=100, customer="王大米", phone_number="13900000000"),
            Order(product_name="东北大米", will_price=100, amount=100, customer="王大米", phone_number="13900000000"),
            Order(product_name="大米", will_price=100, amount=100, customer="王大米", phone_number="13900000000"),
            Order(product_name="日本黑米", will_price=100, amount=100, customer="王大米", phone_number="13900000000"),
            Order(product_name="泰国紫米", will_price=100, amount=100, customer="王大米", phone_number="13900000000"),
            Order(product_name="法国黑米", will_price=100, amount=100, customer="王大米", phone_number="13900000000"),
            Order(product_name="兰州黑米", will_price=100, amount=100, customer="王大米", phone_number="13900000000"),
            Order(product_name="西班牙黑米", will_price=100, amount=100, customer="王大米", phone_number="13900000000")
        ]
        db.session.add_all(orders)
        db.session.commit()

        # Get orders
        page = 2
        page_size = 5
        resp = self.client.get(
            url_for('api.get_orders', page=page, page_size=page_size))
        self.assertEqual(resp.status_code, 200)
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['page'], page)
        self.assertEqual(json_resp['pages'], len(orders) // page_size)
        items = orders[5:]
        for i, order in enumerate(items):
            get_order = Order.from_json(json_resp['items'][i])
            self.assertEqual(get_order.product_name, order.product_name)
            self.assertEqual(get_order.will_price, order.will_price)
            self.assertEqual(get_order.amount, order.amount)
            self.assertEqual(get_order.customer, order.customer)
            self.assertEqual(get_order.phone_number, order.phone_number)

    def test_new_order(self):
        json_order = {
            'product_name': '东北大米',
            'will_price': 100,
            'amount': 100,
            'customer': "陈阿祥",
            'phone_number': "13900000000"
        }
        resp = self.client.post(
            url_for('api.new_order'),
            data=json_order)
        self.assertEqual(resp.status_code, 201)
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['ok'], True)
        resp_item = json_resp['item']
        for k, v in resp_item.items():
            if k == 'id':
                continue
            self.assertEqual(v, json_order[k])

        order_database = Order.query.filter_by(product_name=json_order['product_name']).first()
        for k, v in resp_item.items():
            self.assertEqual(v, getattr(order_database, k))

    def test_update_rice(self):
        rice = Rice(product_name="泰国黑米", min_price=100, avaliable_weight=100, url="http://www.example.com/")
        db.session.add(rice)
        db.session.commit()

        new_rice = Rice(product_name="泰国黑米", min_price=200, avaliable_weight=200, url="http://www.github.com/")
        resp = self.client.put(
            url_for('api.update_rice', id=rice.id),
            data=new_rice.to_json()
        )

        db_rice = Rice.query.get(rice.id)
        for k, v in new_rice.to_json().items():
            if k == 'id':
                continue
            self.assertEqual(getattr(db_rice, k), v)

        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['ok'], True)
        resp_item = json_resp['item']
        for k, v in db_rice.to_json().items():
            self.assertEqual(v, resp_item[k])

    def test_login(self):
        username="admin_rice"
        password="rice"
        phone_number="13971270000"
        admin = User(username=username, password=password, phone_number=phone_number)
        db.session.add(admin)
        db.session.commit()

        resp = self.client.post(
            url_for('api.login'),
            data=dict(
                username=username,
                password=password
            )
        )

        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['ok'], True)
        self.assertEqual(json_resp['phone_number'], phone_number)

    def test_change_password(self):
        username="admin_rice"
        old_password="rice"
        phone_number="13971270000"
        admin = User(username=username, password=old_password, phone_number=phone_number)
        db.session.add(admin)
        db.session.commit()

        new_password = "new_rice"
        resp = self.client.put(
            url_for('api.change_password'),
            data=dict(
                username=username,
                old_password=old_password,
                new_password=new_password
            )
        )

        self.assertEqual(resp.status_code, 200)
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['ok'], True)

        db_user = User.query.filter_by(username=username).first()
        self.assertIsNotNone(db_user)
        self.assertTrue(db_user.verify_password(new_password))

    def test_change_phone_number(self):
        username="admin_rice"
        password="rice"
        old_phone_number="13971270000"
        admin = User(username=username, password=password, phone_number=old_phone_number)
        db.session.add(admin)
        db.session.commit()

        new_phone_number = "13971279099"
        resp = self.client.put(
            url_for('api.change_phone'),
            data=dict(
                username=username,
                password=password,
                phone_number=new_phone_number
            )
        )
        self.assertEqual(resp.status_code, 200)
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['ok'], True)

        db_user = User.query.filter_by(username=username).first()
        self.assertIsNotNone(db_user)
        self.assertNotEqual(db_user.phone_number, old_phone_number)
        self.assertEqual(db_user.phone_number, new_phone_number)
