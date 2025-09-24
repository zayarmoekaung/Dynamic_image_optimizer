class Config:
    SECRET_KEY = ''
    CACHE_DIR = './cache'
    OPTIMIZATION_RULES = {
    'desktop': {'max_width' : 1920,'max_height' : 1080,'quality': 85},
    'tablet': {'max_width' : 1024,'max_height' : 768,'quality': 75},
    'mobile': {'max_width' : 640,'max_height' : 480,'quality': 65}
    }
    STRIP_RULES = {
    'quality': 90,  
    'max_height_cap': 8000  
    }
