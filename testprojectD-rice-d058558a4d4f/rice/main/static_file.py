from flask import send_from_directory
from . import main

@main.route('/')
@main.route('/<path:path>')
def serve_static_file(path='index.html'):
    return send_from_directory('static', path)
