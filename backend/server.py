# backend/server.py
from app import app

if __name__ == '__main__':
    import os

    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(host=host, port=port, debug=debug)
