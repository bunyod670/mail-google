import json
import os
from utils.logger import log_info, log_error

def save_cookies(driver, path):
    """Cookie'larni JSON formatida saqlash."""
    try:
        # Cookie papkasini yaratish
        cookie_dir = os.path.dirname(path)
        os.makedirs(cookie_dir, exist_ok=True)
        
        cookies = driver.get_cookies()
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
        
        log_info(f"Cookie'lar saqlandi: {path}")
        return True
    
    except Exception as e:
        log_error(f"Cookie saqlashda xatolik: {e}")
        return False

def load_cookies(driver, path):
    """Cookie'larni yuklash."""
    try:
        if not os.path.exists(path):
            log_error(f"Cookie fayli topilmadi: {path}")
            return False
        
        with open(path, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                log_error(f"Cookie qo'shishda xatolik: {e}")
                continue
        
        log_info(f"Cookie'lar yuklandi: {path}")
        return True
    
    except Exception as e:
        log_error(f"Cookie yuklashda xatolik: {e}")
        return False

def clear_cookies(driver):
    """Barcha cookie'larni tozalash."""
    try:
        driver.delete_all_cookies()
        log_info("Barcha cookie'lar tozalandi")
        return True
    except Exception as e:
        log_error(f"Cookie tozalashda xatolik: {e}")
        return False

def get_cookies_info(driver):
    """Cookie'lar haqida ma'lumot olish."""
    try:
        cookies = driver.get_cookies()
        log_info(f"Jami cookie'lar soni: {len(cookies)}")
        return cookies
    except Exception as e:
        log_error(f"Cookie ma'lumotini olishda xatolik: {e}")
        return []