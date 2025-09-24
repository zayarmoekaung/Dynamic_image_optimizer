def is_strip(img):
    width, height = img.size
    aspect_ratio = height / width
    return aspect_ratio > 3

def get_img_ext(img):
        if hasattr(img, 'format') and img.format:
            return img.format.lower()
        return None
def get_mime_type(ext):
    mime_types = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'webp': 'image/webp',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'tiff': 'image/tiff',
        'svg': 'image/svg+xml'
    }
    return mime_types.get(ext.lower(), 'application/octet-stream')

def get_fmt(ext):
    fmt_types = {
        'jpeg': 'JPEG',
        'jpg': 'JPEG',
        'png': 'PNG',
        'webp': 'WEBP',
        'gif': 'GIF',
        'bmp': 'BMP',
        'tiff': 'TIFF',
        'svg': 'SVG'
    }
    return fmt_types.get(ext.lower(), None)