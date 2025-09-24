import os
import requests
from flask import abort,send_file
from io import BytesIO
from PIL import Image
from PIL.Image import Resampling
from werkzeug.utils import secure_filename
from utils.cache import get_cache_key
from utils.img_meta import is_strip
from utils.accept_header import get_best_format
from config import Config
class Optimizer:
    def __init__(self, url='', device_type='',client_width=0,client_height=0,dpr=1.0,accept_header=''):
        self.url = url
        self.device_type = device_type
        self.client_width = client_width
        self.client_height = client_height
        self.dpr = dpr
        self.accept_header = accept_header

    def optimize(self):
        if not self.url:
            abort(400, description="Missing 'url' query parameter")
        OPTIMIZATION_RULES = Config.OPTIMIZATION_RULES or {
            'desktop': {'max_width': 1920, 'max_height': 1080, 'quality': 85},
            'tablet': {'max_width': 1024, 'max_height': 768, 'quality': 75},
            'mobile': {'max_width': 640, 'max_height': 480, 'quality': 65}
        }
        STRIP_RULES = Config.STRIP_RULES or {
            'quality': 90,  
            'max_height_cap': 3000
        }
        fmt, ext, mime = get_best_format(self.accept_header)
        CACHE_DIR = Config.CACHE_DIR or './cache'
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        cache_key = get_cache_key(self.url, self.device_type)
        cache_path = os.path.join(CACHE_DIR, secure_filename(cache_key))
        #if os.path.exists(cache_path):
        #    return send_file(cache_path, mimetype=mime)
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            img_data = BytesIO(response.content)
        except requests.RequestException:
            abort(400, description="Failed to fetch image from URL")
        try:
            img = Image.open(img_data)
        except IOError:
            abort(400, description="Invalid image data")
        try:
            rules = OPTIMIZATION_RULES.get(self.device_type, OPTIMIZATION_RULES['desktop'])
            if self.client_width > 0 and self.client_height > 0:
                max_width = int(self.client_width * self.dpr)
                max_height = int(self.client_height * self.dpr)
                quality = rules['quality']
            else:
                max_width = rules['max_width']
                max_height = rules['max_height']
                quality = rules['quality']

            if is_strip(img):
                target_width = int(max_width * self.dpr)
                width, height = img.size
                scale_factor = target_width / width
                target_height = int(height * scale_factor)
                if target_height > STRIP_RULES['max_height_cap']:
                    target_height = STRIP_RULES['max_height_cap']
                scale_factor = target_height / height
                target_width = int(width * scale_factor)
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                quality = STRIP_RULES['quality']  
            else:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            output = BytesIO()
            save_kwargs = {'quality': quality}
            if fmt == 'JPEG':
                save_kwargs['progressive'] = True  
            img.save(output, format=fmt, **save_kwargs)
            output.seek(0)
            #with open(cache_path, 'wb') as f:
            #    f.write(output.getbuffer())
            return send_file(output, mimetype=mime)
        except Exception as e:
            abort(500, description=f"Image optimization failed: {str(e)}")

    
    def set_url(self, url):
        self.url = url  
    def set_device_type(self, device_type):
        self.device_type = device_type
    def set_client_dimensions(self, width, height):
        self.client_width = width
        self.client_height = height
    def set_dpr(self, dpr):
        self.dpr = dpr
    def set_accept_header(self, accept_header):
        self.accept_header = accept_header