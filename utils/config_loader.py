import json
import os
from utils.logger import log_info, log_error

def load_config(path):
    """config.json faylidan sozlamalarni yuklash."""
    try:
        if not os.path.exists(path):
            log_error(f"Config fayli topilmadi: {path}")
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        log_info("Config fayli muvaffaqiyatli yuklandi")
        return config
    
    except json.JSONDecodeError as e:
        log_error(f"Config faylida JSON xatosi: {e}")
        return None
    except Exception as e:
        log_error(f"Config yuklashda xatolik: {e}")
        return None

def validate_config(config):
    """Config faylini tekshirish."""
    required_fields = ['imap', 'chrome', 'captcha']
    
    for field in required_fields:
        if field not in config:
            log_error(f"Configda kerakli maydon yo'q: {field}")
            return False
    
    # IMAP sozlamalarini tekshirish
    imap_fields = ['server', 'port', 'username', 'password']
    for field in imap_fields:
        if field not in config['imap']:
            log_error(f"IMAP sozlamalarida kerakli maydon yo'q: {field}")
            return False
    
    log_info("Config fayli to'g'ri formatda")
    return True