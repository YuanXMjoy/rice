from flask import Blueprint

api = Blueprint('api', __name__)

from . import rice, order, login, change_password, change_phone
