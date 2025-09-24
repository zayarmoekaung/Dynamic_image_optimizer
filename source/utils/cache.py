import hashlib

def get_cache_key(url, device_type):
    key_string = f"{url}_{device_type}"
    return hashlib.md5(key_string.encode()).hexdigest()+'.webp'

def is_avaiable():
    return True