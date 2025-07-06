from flask import Flask
from flask_mail import Mail
from .config import Config

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)

    from .routes.gallery import gallery_bp
    from .routes.admin import admin_bp

    app.register_blueprint(gallery_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
