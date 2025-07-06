from iptcinfo3 import IPTCInfo


def read_iptc(path):
    try:
        info = IPTCInfo(path, force=True)
        title = info['object name'] or ''
        caption = info['caption/abstract'] or ''
        return title, caption
    except Exception:
        return '', ''


def write_iptc(path, title, caption):
    info = IPTCInfo(path, force=True)
    info['object name'] = title
    info['caption/abstract'] = caption
    info.save()
