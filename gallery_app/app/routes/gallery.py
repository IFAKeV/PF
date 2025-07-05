import os
import yaml
from flask import Blueprint, render_template, request, send_from_directory
from ..config import Config

gallery_bp = Blueprint('gallery', __name__)


def load_folders(filter_tag=None):
    base_path = Config.GALLERY_PATH
    folders = []
    for name in os.listdir(base_path):
        folder_path = os.path.join(base_path, name)
        meta_path = os.path.join(folder_path, 'folder_meta.yaml')
        images_dir = os.path.join(folder_path, 'bilder')
        if os.path.isdir(folder_path) and os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = yaml.safe_load(f)
            if filter_tag and filter_tag not in meta.get('tags', []):
                continue
            images = []
            if os.path.isdir(images_dir):
                for img_name in os.listdir(images_dir):
                    if os.path.splitext(img_name)[1].lower() in Config.UPLOAD_EXTENSIONS:
                        images.append({'filename': img_name})
            folders.append({'name': name, 'meta': meta, 'images': images})
    folders.sort(key=lambda f: f['meta'].get('date', ''), reverse=True)
    return folders


@gallery_bp.route('/')
def index():
    selected_tag = request.args.get('tag')
    folders = load_folders(selected_tag)
    # collect all tags for filter dropdown
    all_tags = set()
    for f in load_folders():
        all_tags.update(f['meta'].get('tags', []))
    tags = sorted(all_tags)
    return render_template('gallery.html', folders=folders, tags=tags, selected_tag=selected_tag)


@gallery_bp.route('/image/<folder>/<filename>')
def image(folder, filename):
    path = os.path.join(Config.GALLERY_PATH, folder, 'bilder')
    return send_from_directory(path, filename)
