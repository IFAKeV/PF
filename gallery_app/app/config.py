import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    GALLERY_PATH = os.path.abspath(os.environ.get('GALLERY_PATH', os.path.join(os.path.dirname(__file__), '..', 'galleries')))
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png']
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'gallery@example.com')
    MAIL_RECIPIENT = os.environ.get('MAIL_RECIPIENT', 'user@example.com')
