def parse_accept_header(accept_header_str):
    parts = [part.strip() for part in accept_header_str.split(',')]
    parsed = []
    for part in parts:
        if ';' in part:
            mime, *params = part.split(';')
            q = 1.0
            for param in params:
                if '=' in param:
                    key, value = param.split('=')
                    if key.strip() == 'q':
                        try:
                            q = float(value.strip())
                        except ValueError:
                            q = 0.0
            parsed.append((mime.strip(), q))
        else:
            parsed.append((part, 1.0))
    parsed.sort(key=lambda x: x[1], reverse=True)
    return [mime for mime, q in parsed]

def get_best_format(accept_header):
    best_format = accept_header.best_match(['image/webp', 'image/jpeg'])
    if best_format == 'image/jpeg':
        fmt = 'JPEG'
        ext = 'jpeg'
        mime = 'image/jpeg'
    elif best_format == 'image/png':
        fmt = 'PNG'
        ext = 'png'
        mime = 'image/png'
    elif best_format == 'image/bmp':
        fmt = 'BMP'
        ext = 'bmp'
        mime = 'image/bmp'
    elif best_format == 'image/gif':
        fmt = 'GIF'
        ext = 'gif'
        mime = 'image/gif'
    elif best_format == 'image/tiff':
        fmt = 'TIFF'
        ext = 'tiff'
        mime = 'image/tiff'
    else:
        fmt = 'WEBP'
        ext = 'webp'
        mime = 'image/webp'
    
    return fmt, ext, mime