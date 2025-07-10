import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import log_info, log_error, log_debug
from utils.imap_verifier import connect_imap, fetch_latest_email, extract_verification_code, disconnect_imap
from utils.captcha_solver import detect_captcha, take_captcha_screenshot, solve_captcha, check_captcha_solved
from utils.session_manager import save_cookies, load_cookies
from utils.config_loader import load_config, validate_config
from utils.random_delay import wait_random, wait_human_like

def create_google_account_with_verification(user_data, config):
    """Google hisobini yaratish va barcha jarayonlarni boshqarish."""
    driver = None
    imap = None
    
    try:
        # Config'ni tekshirish
        if not validate_config(config):
            return {"status": "error", "message": "Config fayli noto'g'ri"}
        
        log_info(f"Google hisob yaratish boshlanmoqda: {user_data['email']}")
        
        # 1. Chrome sessiyani yaratish
        driver = create_chrome_session(config)
        if not driver:
            return {"status": "error", "message": "Chrome sessiyasi yaratilmadi"}
        
        # 2. Google Signup sahifasini ochish
        if not open_google_signup(driver):
            return {"status": "error", "message": "Google signup sahifasi ochilmadi"}
        
        # 3. Formani to'ldirish
        if not fill_signup_form(driver, user_data):
            return {"status": "error", "message": "Forma to'ldirilmadi"}
        
        # 4. IMAP ulanish
        imap = connect_imap(
            config['imap']['username'],
            config['imap']['password'],
            config['imap']['server'],
            config['imap']['port']
        )
        if not imap:
            return {"status": "error", "message": "IMAP ulanish amalga oshmadi"}
        
        # 5. Verification kodini kutish
        verification_code = wait_for_verification_email(imap, "Google")
        if not verification_code:
            return {"status": "error", "message": "Verification kodi olinmadi"}
        
        # 6. Kodni kiritish
        if not enter_verification_code(driver, verification_code):
            return {"status": "error", "message": "Verification kodi kiritilmadi"}
        
        # 7. Profil ma'lumotlarini to'ldirish
        if not fill_profile_info(driver, user_data):
            return {"status": "error", "message": "Profil ma'lumotlari to'ldirilmadi"}
        
        # 8. CAPTCHA monitoring
        if not handle_captcha_if_present(driver, config):
            return {"status": "error", "message": "CAPTCHA yechilmadi"}
        
        # 9. Cookie'larni saqlash
        cookie_path = f"cookies/{user_data['email'].replace('@', '_')}.json"
        if not save_cookies(driver, cookie_path):
            log_warning("Cookie'lar saqlanmadi")
        
        # 10. Yakuniy natija
        result = finalize_signup(driver, user_data)
        log_info("Google hisob muvaffaqiyatli yaratildi")
        
        return result
        
    except Exception as e:
        log_error(f"Google hisob yaratishda xatolik: {e}")
        return {"status": "error", "message": str(e)}
    
    finally:
        # Resurslarni tozalash
        if driver:
            driver.quit()
        if imap:
            disconnect_imap(imap)

def create_chrome_session(config):
    """Chrome sessiyani yaratish."""
    try:
        chrome_options = Options()
        
        # Chrome sozlamalari
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent
        if 'user_agent' in config['chrome']:
            chrome_options.add_argument(f"--user-agent={config['chrome']['user_agent']}")
        
        # Proxy
        if 'proxy' in config['chrome'] and config['chrome']['proxy']:
            chrome_options.add_argument(f"--proxy-server={config['chrome']['proxy']}")
        
        # Qo'shimcha sozlamalar
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # JavaScript orqali automation belgilarini yashirish
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        log_info("Chrome sessiyasi muvaffaqiyatli yaratildi")
        return driver
        
    except Exception as e:
        log_error(f"Chrome sessiyasi yaratishda xatolik: {e}")
        return None

def open_google_signup(driver):
    """Google Signup sahifasini ochish."""
    try:
        signup_url = "https://accounts.google.com/signup"
        driver.get(signup_url)
        
        # Sahifa yuklanishini kutish
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )
        
        log_info("Google signup sahifasi ochildi")
        return True
        
    except TimeoutException:
        log_error("Google signup sahifasi ochilmadi")
        return False
    except Exception as e:
        log_error(f"Google signup sahifasini ochishda xatolik: {e}")
        return False

def fill_signup_form(driver, user_data):
    """Signup formani to'ldirish."""
    try:
        wait = WebDriverWait(driver, 10)
        
        # Ism
        first_name_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "firstName"))
        )
        first_name_input.clear()
        first_name_input.send_keys(user_data['first_name'])
        wait_human_like()
        
        # Familiya
        last_name_input = driver.find_element(By.NAME, "lastName")
        last_name_input.clear()
        last_name_input.send_keys(user_data['last_name'])
        wait_human_like()
        
        # Email
        email_input = driver.find_element(By.NAME, "Username")
        email_input.clear()
        email_input.send_keys(user_data['email'].split('@')[0])
        wait_human_like()
        
        # Parol
        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.clear()
        password_input.send_keys(user_data['password'])
        wait_human_like()
        
        # Parol tasdiqlash
        confirm_password_input = driver.find_element(By.NAME, "ConfirmPasswd")
        confirm_password_input.clear()
        confirm_password_input.send_keys(user_data['password'])
        wait_human_like()
        
        # Next tugmasini bosish
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        next_button.click()
        
        log_info("Signup formasi to'ldirildi")
        return True
        
    except Exception as e:
        log_error(f"Signup formani to'ldirishda xatolik: {e}")
        return False

def wait_for_verification_email(imap, subject_filter, timeout=120):
    """IMAP orqali verification kodini kutish."""
    try:
        log_info("Verification email kutish boshlanmoqda...")
        
        email_message = fetch_latest_email(imap, subject_filter, timeout)
        if not email_message:
            return None
        
        verification_code = extract_verification_code(email_message)
        if verification_code:
            log_info(f"Verification kodi olingan: {verification_code}")
            return verification_code
        else:
            log_error("Verification kodi ajratilmadi")
            return None
            
    except Exception as e:
        log_error(f"Verification email kutishda xatolik: {e}")
        return None

def enter_verification_code(driver, code):
    """Verification kodini inputga kiritish."""
    try:
        wait = WebDriverWait(driver, 10)
        
        # Verification kod input'ini topish
        code_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "code"))
        )
        code_input.clear()
        code_input.send_keys(code)
        wait_human_like()
        
        # Verify tugmasini bosish
        verify_button = driver.find_element(By.XPATH, "//span[text()='Verify']")
        verify_button.click()
        
        # Verification natijasini kutish
        wait.until(
            EC.presence_of_element_located((By.NAME, "day"))
        )
        
        log_info("Verification kodi muvaffaqiyatli kiritildi")
        return True
        
    except Exception as e:
        log_error(f"Verification kodini kiritishda xatolik: {e}")
        return False

def fill_profile_info(driver, user_data):
    """Profil ma'lumotlarini to'ldirish."""
    try:
        wait = WebDriverWait(driver, 10)
        
        # Tug'ilgan kun
        day_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "day"))
        )
        day_input.clear()
        day_input.send_keys(user_data['birth_day'])
        wait_human_like()
        
        # Tug'ilgan oy
        month_select = driver.find_element(By.NAME, "month")
        month_select.click()
        month_option = driver.find_element(By.XPATH, f"//option[text()='{user_data['birth_month']}']")
        month_option.click()
        wait_human_like()
        
        # Tug'ilgan yil
        year_input = driver.find_element(By.NAME, "year")
        year_input.clear()
        year_input.send_keys(user_data['birth_year'])
        wait_human_like()
        
        # Jinsi
        gender_select = driver.find_element(By.NAME, "gender")
        gender_select.click()
        gender_option = driver.find_element(By.XPATH, f"//option[text()='{user_data['gender']}']")
        gender_option.click()
        wait_human_like()
        
        # Next tugmasini bosish
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        next_button.click()
        
        log_info("Profil ma'lumotlari to'ldirildi")
        return True
        
    except Exception as e:
        log_error(f"Profil ma'lumotlarini to'ldirishda xatolik: {e}")
        return False

def handle_captcha_if_present(driver, config):
    """CAPTCHA monitoring va yechish."""
    try:
        # CAPTCHA mavjudligini tekshirish
        captcha_found, captcha_element = detect_captcha(driver)
        
        if captcha_found:
            log_info("CAPTCHA topildi, yechish boshlanmoqda...")
            
            # Skrinshot saqlash
            screenshot_path = f"screenshots/captcha_{int(time.time())}.png"
            take_captcha_screenshot(driver, screenshot_path)
            
            # CAPTCHA yechish
            api_key = config['captcha']['api_key']
            if solve_captcha(driver, api_key):
                log_info("CAPTCHA muvaffaqiyatli yechildi")
                return True
            else:
                log_error("CAPTCHA yechilmadi")
                return False
        else:
            log_info("CAPTCHA topilmadi")
            return True
            
    except Exception as e:
        log_error(f"CAPTCHA boshqarishda xatolik: {e}")
        return False

def finalize_signup(driver, user_data):
    """Signup yakuniy natijasini tayyorlash."""
    try:
        # Yakuniy skrinshot
        screenshot_path = f"screenshots/final_{user_data['email'].replace('@', '_')}.png"
        driver.save_screenshot(screenshot_path)
        
        # Natija
        result = {
            "email": user_data['email'],
            "status": "created",
            "cookies": f"cookies/{user_data['email'].replace('@', '_')}.json",
            "screenshot": screenshot_path,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        
        log_info(f"Google hisob yaratish yakunlandi: {user_data['email']}")
        return result
        
    except Exception as e:
        log_error(f"Yakuniy natija tayyorlashda xatolik: {e}")
        return {"status": "error", "message": str(e)}