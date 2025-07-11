import json
import os
from utils.logger import log_info, log_error, log_warning

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

def create_sample_config():
    """Namuna config faylini yaratish."""
    sample_config = {
        "imap": {
            "server": "mail.yourdomain.com",
            "port": 993,
            "username": "user@yourdomain.com",
            "password": "yourpassword"
        },
        "chrome": {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "proxy": ""
        },
        "captcha": {
            "api_key": "YOUR_2CAPTCHA_KEY"
        }
    }
    
    try:
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, indent=2, ensure_ascii=False)
        log_info("Namuna config fayli yaratildi: config.json")
        return True
    except Exception as e:
        log_error(f"Config faylini yaratishda xatolik: {e}")
        return False