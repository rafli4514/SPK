from .ahp_bp import ahp_bp
from .saw_bp import saw_bp

def register_blueprints(app):
    app.register_blueprint(ahp_bp, url_prefix='/api/ahp')
    app.register_blueprint(saw_bp, url_prefix='/api/saw')