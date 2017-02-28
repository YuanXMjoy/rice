from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Rice(db.Model):
    __tablename__ = 'rices'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.Unicode(20), unique=True, index=True)
    min_price = db.Column(db.Integer)
    avaliable_weight = db.Column(db.Integer)
    url = db.Column(db.String(128),  nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'min_price': self.min_price,
            'avaliable_weight': self.avaliable_weight,
            'url': self.url
        }

    @staticmethod
    def from_json(json_rice):
        return Rice(**json_rice)

    def __repr__(self):
        return '<Role product_name: {}, min_price: {}\
            avaliable_weight: {}, url: {}>'.format(
            self.product_name, self.min_price,
            self.avaliable_weight, self.url
            )


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.Unicode(20))
    will_price = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    customer = db.Column(db.Unicode(10))
    phone_number = db.Column(db.String(11))
    time = db.Column(db.DateTime)

    def to_json(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'will_price': self.will_price,
            'amount': self.amount,
            'customer': self.customer,
            'phone_number': self.phone_number,
            'time': self.time.strftime("%Y年%m月%d日 %H:%M") if self.time is not None else self.time
        }

    @staticmethod
    def from_json(json_order):
        return Order(**json_order)

    def __repr__(self):
        return '<Order product_name: {}, will_price: {}\
            amount: {}, customer: {}, phone_number: {}>'.format(
            self.product_name, self.will_price,
            self.amount, self.customer, self.phone_number, self.time
            )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(11))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def from_json(json_user):
        return User(**json_user)

    def __repr__(self):
        return '<User username: {}, password: {}, phone_number: {}>'.format(
            self.username, self.password_hash, self.phone_number
            )
