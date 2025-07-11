import os
import random
from utils.logger import log_info, log_error, log_debug

def load_proxies_from_file(file_path="proxy.txt"):
    """Proxy ro'yxatini fayldan o'qish."""
    try:
        if not os.path.exists(file_path):
            log_error(f"Proxy fayli topilmadi: {file_path}")
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
        
        log_info(f"Proxy ro'yxati yuklandi: {len(proxies)} ta")
        return proxies
    
    except Exception as e:
        log_error(f"Proxy faylini o'qishda xatolik: {e}")
        return []

def get_random_proxy(proxy_list):
    """Tasodifiy proxy qaytarish."""
    if not proxy_list:
        return None
    
    proxy = random.choice(proxy_list)
    log_debug(f"Tanlangan proxy: {proxy}")
    return proxy

def validate_proxy(proxy):
    """Proxy formatini tekshirish."""
    if not proxy:
        return False
    
    # HTTP/HTTPS proxy formatini tekshirish
    if proxy.startswith(('http://', 'https://')):
        return True
    
    # IP:PORT formatini tekshirish
    if ':' in proxy:
        parts = proxy.split(':')
        if len(parts) == 2:
            try:
                port = int(parts[1])
                return 1 <= port <= 65535
            except ValueError:
                return False
    
    return False

def format_proxy(proxy):
    """Proxy formatini to'g'rilash."""
    if not proxy:
        return None
    
    # Agar format yo'q bo'lsa, http:// qo'shish
    if not proxy.startswith(('http://', 'https://')):
        proxy = f"http://{proxy}"
    
    return proxy

def create_proxy_file():
    """Namuna proxy faylini yaratish."""
    sample_proxies = [
        "http://proxy1.example.com:8080",
        "http://proxy2.example.com:8080",
        "https://proxy3.example.com:8443",
        "192.168.1.100:8080",
        "10.0.0.1:3128"
    ]
    
    try:
        with open('proxy.txt', 'w', encoding='utf-8') as f:
            for proxy in sample_proxies:
                f.write(f"{proxy}\n")
        
        log_info("Namuna proxy fayli yaratildi: proxy.txt")
        return True
    except Exception as e:
        log_error(f"Proxy faylini yaratishda xatolik: {e}")
        return False

def get_proxy_list():
    """Proxy ro'yxatini o'qish va tekshirish."""
    proxies = load_proxies_from_file()
    
    if not proxies:
        log_warning("Proxy fayli bo'sh yoki topilmadi")
        return []
    
    # Proxy'larni tekshirish va formatlash
    valid_proxies = []
    for proxy in proxies:
        if validate_proxy(proxy):
            formatted_proxy = format_proxy(proxy)
            valid_proxies.append(formatted_proxy)
        else:
            log_warning(f"Noto'g'ri proxy format: {proxy}")
    
    log_info(f"To'g'ri formatdagi proxy'lar: {len(valid_proxies)}/{len(proxies)}")
    return valid_proxies