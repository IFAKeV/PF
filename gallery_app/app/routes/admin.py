import os
import yaml
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename

from ..config import Config
from ..utils import read_iptc, write_iptc
from .. import mail
from flask_mail import Message

admin_bp = Blueprint('admin', __name__)


def get_folder_path(folder_name):
    return os.path.join(Config.GALLERY_PATH, folder_name)


def list_folders():
    folders = []
    for name in sorted(os.listdir(Config.GALLERY_PATH)):
        folder_path = get_folder_path(name)
        meta_path = os.path.join(folder_path, 'folder_meta.yaml')
        if os.path.isdir(folder_path) and os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = yaml.safe_load(f)
            folders.append({'name': name, 'meta': meta})
    return folders


@admin_bp.route('/')
def index():
    folders = list_folders()
    return render_template('admin/index.html', folders=folders)


@admin_bp.route('/folder/<folder_name>')
def edit_folder(folder_name):
    folder_path = get_folder_path(folder_name)
    images_dir = os.path.join(folder_path, 'bilder')
    images = []
    for img_name in os.listdir(images_dir):
        if os.path.splitext(img_name)[1].lower() in Config.UPLOAD_EXTENSIONS:
            path = os.path.join(images_dir, img_name)
            title, caption = read_iptc(path)
            if not caption:
                caption = 'unbenannt'
            images.append({'filename': img_name, 'title': title, 'caption': caption})
    return render_template('admin/edit_folder.html', folder=folder_name, images=images)


@admin_bp.route('/folder/<folder_name>/edit/<filename>', methods=['GET', 'POST'])
def edit_image(folder_name, filename):
    folder_path = get_folder_path(folder_name)
    images_dir = os.path.join(folder_path, 'bilder')
    path = os.path.join(images_dir, filename)
    if request.method == 'POST':
        title = request.form.get('title', '')
        caption = request.form.get('caption', '')
        write_iptc(path, title, caption)
        flash('Metadaten gespeichert', 'success')
        return redirect(url_for('admin.edit_folder', folder_name=folder_name))
    else:
        title, caption = read_iptc(path)
        return render_template('admin/edit_image.html', folder=folder_name, filename=filename, title=title, caption=caption)


@admin_bp.route('/upload/<folder_name>', methods=['POST'])
def upload(folder_name):
    folder_path = get_folder_path(folder_name)
    images_dir = os.path.join(folder_path, 'bilder')
    file = request.files.get('file')
    if file and os.path.splitext(file.filename)[1].lower() in Config.UPLOAD_EXTENSIONS:
        filename = secure_filename(file.filename)
        dest = os.path.join(images_dir, filename)
        file.save(dest)
        title, caption = read_iptc(dest)
        if not caption:
            caption = 'unbenannt'
            write_iptc(dest, title, caption)
        # optional email
        send_edit_link(dest, folder_name)
        flash('Bild hochgeladen', 'success')
    else:
        flash('Ungültige Datei', 'error')
    return redirect(url_for('admin.edit_folder', folder_name=folder_name))


def send_edit_link(path, folder_name):
    try:
        url = url_for('admin.edit_folder', folder_name=folder_name, _external=True)
        msg = Message('Neuer Upload', recipients=[Config.MAIL_RECIPIENT])
        msg.body = f'Ein neues Bild wurde hochgeladen. Bearbeiten: {url}'
        mail.send(msg)
    except Exception:
        pass
