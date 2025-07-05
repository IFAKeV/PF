import os
import yaml
from flask import Blueprint, render_template, current_app, send_from_directory
from ..config import Config
from ..utils import read_iptc

gallery_bp = Blueprint('gallery', __name__)


def load_folders():
    base_path = Config.GALLERY_PATH
    folders = []
    for name in sorted(os.listdir(base_path)):
        folder_path = os.path.join(base_path, name)
        meta_path = os.path.join(folder_path, 'folder_meta.yaml')
        images_dir = os.path.join(folder_path, 'bilder')
        if os.path.isdir(folder_path) and os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = yaml.safe_load(f)
            images = []
            if os.path.isdir(images_dir):
                for img_name in os.listdir(images_dir):
                    if os.path.splitext(img_name)[1].lower() in Config.UPLOAD_EXTENSIONS:
                        images.append({'filename': img_name})
            folders.append({'name': name, 'meta': meta, 'images': images})
    return folders


@gallery_bp.route('/')
def index():
    folders = load_folders()
    return render_template('gallery.html', folders=folders)


@gallery_bp.route('/image/<folder>/<filename>')
def image(folder, filename):
    path = os.path.join(Config.GALLERY_PATH, folder, 'bilder')
    return send_from_directory(path, filename)
