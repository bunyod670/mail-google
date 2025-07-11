import os
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import log_info, log_error, log_debug

def detect_captcha(driver):
    """CAPTCHA mavjudligini aniqlash."""
    try:
        # Turli xil CAPTCHA elementlarini qidirish
        captcha_selectors = [
            "iframe[src*='recaptcha']",
            "iframe[src*='captcha']",
            ".g-recaptcha",
            "#recaptcha",
            "[class*='captcha']",
            "[id*='captcha']"
        ]
        
        for selector in captcha_selectors:
            try:
                captcha_element = driver.find_element(By.CSS_SELECTOR, selector)
                if captcha_element.is_displayed():
                    log_info(f"CAPTCHA topildi: {selector}")
                    return True, captcha_element
            except:
                continue
        
        log_debug("CAPTCHA topilmadi")
        return False, None
    
    except Exception as e:
        log_error(f"CAPTCHA aniqlashda xatolik: {e}")
        return False, None

def take_captcha_screenshot(driver, path):
    """CAPTCHA skrinshotini saqlash."""
    try:
        # Screenshot papkasini yaratish
        screenshot_dir = os.path.dirname(path)
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # CAPTCHA elementini topish
        captcha_found, captcha_element = detect_captcha(driver)
        
        if captcha_found:
            # CAPTCHA elementining skrinshotini olish
            captcha_element.screenshot(path)
            log_info(f"CAPTCHA skrinshot saqlandi: {path}")
            return True
        else:
            # Butun sahifaning skrinshotini olish
            driver.save_screenshot(path)
            log_info(f"Sahifa skrinshot saqlandi: {path}")
            return True
    
    except Exception as e:
        log_error(f"Skrinshot saqlashda xatolik: {e}")
        return False

def solve_captcha(driver, api_key):
    """2Captcha API orqali CAPTCHA ni yechish."""
    try:
        if not api_key or api_key == "YOUR_2CAPTCHA_KEY":
            log_error("2Captcha API kaliti to'g'ri sozlanmagan")
            return False
        
        # CAPTCHA elementini topish
        captcha_found, captcha_element = detect_captcha(driver)
        
        if not captcha_found:
            log_info("CAPTCHA topilmadi, yechish shart emas")
            return True
        
        # CAPTCHA turini aniqlash
        captcha_type = "recaptcha"  # Default
        
        if "recaptcha" in captcha_element.get_attribute("src").lower():
            captcha_type = "recaptcha"
        elif "hcaptcha" in captcha_element.get_attribute("src").lower():
            captcha_type = "hcaptcha"
        
        log_info(f"CAPTCHA turi: {captcha_type}")
        
        # 2Captcha API ga yuborish
        site_key = captcha_element.get_attribute("data-sitekey")
        page_url = driver.current_url
        
        # API so'rovini yuborish
        response = solve_with_2captcha(api_key, site_key, page_url, captcha_type)
        
        if response and "result" in response:
            # Yechilgan kodni input'ga kiritish
            result = response["result"]
            log_info(f"CAPTCHA yechildi: {result}")
            
            # JavaScript orqali CAPTCHA'ni to'ldirish
            driver.execute_script(
                f"document.getElementById('g-recaptcha-response').innerHTML='{result}';"
            )
            
            # Callback funksiyasini chaqirish
            driver.execute_script("___grecaptcha_cfg.clients[0].aa.l.callback('{result}');")
            
            return True
        else:
            log_error("CAPTCHA yechilmadi")
            return False
    
    except Exception as e:
        log_error(f"CAPTCHA yechishda xatolik: {e}")
        return False

def solve_with_2captcha(api_key, site_key, page_url, captcha_type):
    """2Captcha API bilan CAPTCHA yechish."""
    try:
        # 2Captcha API endpoint
        url = "http://2captcha.com/in.php"
        
        data = {
            "key": api_key,
            "method": "userrecaptcha",
            "googlekey": site_key,
            "pageurl": page_url,
            "json": 1
        }
        
        # CAPTCHA yechish so'rovini yuborish
        response = requests.post(url, data=data)
        result = response.json()
        
        if result["status"] == 1:
            captcha_id = result["request"]
            log_info(f"CAPTCHA yechish so'rovi yuborildi, ID: {captcha_id}")
            
            # Natijani kutish
            return wait_for_captcha_result(api_key, captcha_id)
        else:
            log_error(f"2Captcha xatosi: {result.get('error_text', 'Noma\'lum xato')}")
            return None
    
    except Exception as e:
        log_error(f"2Captcha API da xatolik: {e}")
        return None

def wait_for_captcha_result(api_key, captcha_id, timeout=120):
    """CAPTCHA yechish natijasini kutish."""
    try:
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1"
            
            response = requests.get(url)
            result = response.json()
            
            if result["status"] == 1:
                log_info("CAPTCHA muvaffaqiyatli yechildi")
                return result
            elif "CAPCHA_NOT_READY" in result["request"]:
                log_debug("CAPTCHA hali yechilmagan, 5 soniya kutish...")
                time.sleep(5)
            else:
                log_error(f"CAPTCHA yechishda xatolik: {result.get('request', 'Noma\'lum xato')}")
                return None
        
        log_error(f"CAPTCHA yechish timeout: {timeout} soniya")
        return None
    
    except Exception as e:
        log_error(f"CAPTCHA natija kutishda xatolik: {e}")
        return None

def check_captcha_solved(driver):
    """CAPTCHA yechilganligini tekshirish."""
    try:
        # CAPTCHA yechilganligini tekshirish
        solved_selectors = [
            ".recaptcha-checkbox-checked",
            "[data-callback]",
            ".g-recaptcha-response"
        ]
        
        for selector in solved_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    log_info("CAPTCHA yechilganligi tasdiqlandi")
                    return True
            except:
                continue
        
        log_debug("CAPTCHA yechilmagan")
        return False
    
    except Exception as e:
        log_error(f"CAPTCHA tekshirishda xatolik: {e}")
        return False