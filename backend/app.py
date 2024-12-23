# backend/app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
import os
import sys
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from blueprints import register_blueprints

app = Flask(__name__)
CORS(app) 

register_blueprints(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Server is running."}), 200

if __name__ == '__main__':
    import os

    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(host=host, port=port, debug=debug)
