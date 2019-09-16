"""This package handles uploading images to a server and then returning
the permalink to the image. This supports one very simple structure of
a website, but you will generally need to use your own.
"""

import os
import json
import requests
import io
import typing
from PIL import Image

CONFIG_FILE = 'upload.json'

def _config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(CONFIG_FILE)

    with open(CONFIG_FILE, 'r') as infile:
        res = json.load(infile)

    for key in ('upload_url', 'base_url', 'secret'):
        if key not in res:
            raise ValueError(f'missing key in {CONFIG_FILE}: {key}')
    return res

CONFIG = _config()

def upload(img) -> str:
    """Returns the permalink to an image after uploading it."""
    if not hasattr(img, 'seek'):
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
    else:
        img_bytes = img
    img_bytes.seek(0)

    files = {'file': ('img.png', img_bytes, 'image/png', {'Expires': '0'})}
    res = requests.post(CONFIG['upload_url'],
                        data={'secret': CONFIG['secret']},
                        files=files)

    res_json = res.json()
    if ('success' not in res_json
            or not res_json['success']
            or 'filename' not in res_json):
        raise ValueError(f'seems like failure response: {res_json}')

    return CONFIG['base_url'] + res_json['filename']
