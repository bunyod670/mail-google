import sys
import json
from modules.google_signup_with_verification import create_google_account_with_verification
from utils.config_loader import load_config, validate_config
from utils.logger import log_info, log_error, log_warning
from utils.menu_system import handle_main_menu, show_statistics

def main():
    """Asosiy dastur."""
    try:
        # Config faylini yuklash
        config = load_config('config.json')
        if not config:
            log_error("Config fayli yuklanmadi")
            return False
        
        # Config'ni tekshirish
        if not validate_config(config):
            log_error("Config fayli noto'g'ri formatda")
            return False
        
        log_info("Google hisob yaratish boshlanmoqda...")
        
        # Google hisob yaratish
        result = create_google_account_with_verification(config=config)
        
        if result['status'] == 'created':
            log_info("Google hisob muvaffaqiyatli yaratildi!")
            print("\n=== NATIJA ===")
            print(f"Email: {result['email']}")
            print(f"Status: {result['status']}")
            print(f"Cookies: {result['cookies']}")
            print(f"Screenshot: {result['screenshot']}")
            print(f"Timestamp: {result['timestamp']}")
            return True
        else:
            log_error(f"Google hisob yaratilmadi: {result['message']}")
            return False
            
    except KeyboardInterrupt:
        log_info("Dastur foydalanuvchi tomonidan to'xtatildi")
        return False
    except Exception as e:
        log_error(f"Kutilmagan xatolik: {e}")
        return False

def run_with_menu():
    """Menyu bilan ishga tushirish."""
    try:
        while True:
            choice = handle_main_menu()
            
            if choice == "create_account":
                print("\n🚀 Google hisob yaratish boshlanmoqda...")
                result = create_google_account_with_verification()
                
                if result['status'] == 'created':
                    print("\n✅ MUVAFFAQIYATLI!")
                    print("="*50)
                    print(f"📧 Email: {result['email']}")
                    print(f"📊 Status: {result['status']}")
                    print(f"🍪 Cookies: {result['cookies']}")
                    print(f"📸 Screenshot: {result['screenshot']}")
                    print(f"⏰ Vaqt: {result['timestamp']}")
                    print("="*50)
                else:
                    print(f"\n❌ XATOLIK: {result['message']}")
                
                input("\nDavom etish uchun Enter tugmasini bosing...")
            
    except KeyboardInterrupt:
        print("\n👋 Xayr!")
        sys.exit(0)
    except Exception as e:
        log_error(f"Menyu ishlashda xatolik: {e}")
        return False

def test_config():
    """Config faylini test qilish."""
    try:
        config = load_config('config.json')
        if config and validate_config(config):
            log_info("Config fayli to'g'ri sozlangan")
            return True
        else:
            log_error("Config faylida muammo bor")
            return False
    except Exception as e:
        log_error(f"Config testida xatolik: {e}")
        return False

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

if __name__ == "__main__":
    # Argumentlarni tekshirish
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test-config":
            success = test_config()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--create-config":
            success = create_sample_config()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--help":
            print("Google Account Creator")
            print("Foydalanish:")
            print("  python main.py                    - Asosiy dastur (mendu bilan)")
            print("  python main.py --direct           - To'g'ridan-to'g'ri ishga tushirish")
            print("  python main.py --test-config      - Config faylini test qilish")
            print("  python main.py --create-config    - Namuna config yaratish")
            print("  python main.py --help             - Yordam")
            sys.exit(0)
        elif sys.argv[1] == "--direct":
            # To'g'ridan-to'g'ri ishga tushirish
            success = main()
            sys.exit(0 if success else 1)
    
    # Asosiy dastur (mendu bilan)
    run_with_menu()