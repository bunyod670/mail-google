import os
import sys
from utils.logger import log_info, log_error, log_warning
from utils.config_loader import load_config, validate_config
from utils.proxy_manager import create_proxy_file, get_proxy_list
from utils.email_manager import create_email_file, get_email_list
from utils.user_agent_manager import get_random_user_agent, get_user_agent_by_type

def show_main_menu():
    """Asosiy menyuni ko'rsatish."""
    print("\n" + "="*50)
    print("🔧 GOOGLE ACCOUNT CREATOR")
    print("="*50)
    print("1. 📧 Google hisob yaratish")
    print("2. ⚙️  Sozlamalarni ko'rish")
    print("3. 🔧 Fayllarni boshqarish")
    print("4. 📊 Statistika")
    print("5. 🧪 Test qilish")
    print("6. ❓ Yordam")
    print("0. 🚪 Chiqish")
    print("="*50)

def show_settings_menu():
    """Sozlamalar menyusini ko'rsatish."""
    print("\n" + "="*50)
    print("⚙️  SOZLAMALAR")
    print("="*50)
    print("1. 📋 Config faylini ko'rish")
    print("2. 🔧 Config faylini tahrirlash")
    print("3. 📊 Proxy ro'yxatini ko'rish")
    print("4. 📧 Email ro'yxatini ko'rish")
    print("5. 🔄 User Agent'lar")
    print("0. ⬅️  Orqaga")
    print("="*50)

def show_file_management_menu():
    """Fayl boshqarish menyusini ko'rsatish."""
    print("\n" + "="*50)
    print("🔧 FAYL BOSHQARISH")
    print("="*50)
    print("1. 📝 Namuna config yaratish")
    print("2. 🌐 Namuna proxy fayli yaratish")
    print("3. 📧 Namuna email fayli yaratish")
    print("4. 📁 Fayllarni ko'rish")
    print("5. 🗑️  Log fayllarini tozalash")
    print("0. ⬅️  Orqaga")
    print("="*50)

def show_statistics():
    """Statistikani ko'rsatish."""
    print("\n" + "="*50)
    print("📊 STATISTIKA")
    print("="*50)
    
    # Config ma'lumotlari
    config = load_config('config.json')
    if config:
        print("✅ Config fayli mavjud")
        if 'imap' in config:
            print(f"📧 IMAP server: {config['imap']['server']}")
    else:
        print("❌ Config fayli topilmadi")
    
    # Proxy ma'lumotlari
    proxies = get_proxy_list()
    print(f"🌐 Proxy'lar: {len(proxies)} ta")
    
    # Email ma'lumotlari
    emails = get_email_list()
    print(f"📧 Email'lar: {len(emails)} ta")
    
    # Log fayli
    if os.path.exists('logs/signup_activity.log'):
        log_size = os.path.getsize('logs/signup_activity.log')
        print(f"📝 Log fayli: {log_size} bayt")
    else:
        print("📝 Log fayli: mavjud emas")
    
    # Cookie fayllari
    if os.path.exists('cookies'):
        cookie_count = len([f for f in os.listdir('cookies') if f.endswith('.json')])
        print(f"🍪 Cookie fayllari: {cookie_count} ta")
    else:
        print("🍪 Cookie fayllari: mavjud emas")
    
    print("="*50)

def show_test_menu():
    """Test menyusini ko'rsatish."""
    print("\n" + "="*50)
    print("🧪 TEST QILISH")
    print("="*50)
    print("1. 🔧 Config test")
    print("2. 🌐 Proxy test")
    print("3. 📧 Email test")
    print("4. 🌐 User Agent test")
    print("5. 🔗 Internet ulanish test")
    print("0. ⬅️  Orqaga")
    print("="*50)

def show_help():
    """Yordam ma'lumotlarini ko'rsatish."""
    print("\n" + "="*50)
    print("❓ YORDAM")
    print("="*50)
    print("Bu dastur Google hisoblarini avtomatik yaratish uchun mo'ljallangan.")
    print("\n📋 Kerakli fayllar:")
    print("- config.json - Asosiy sozlamalar")
    print("- proxy.txt - Proxy ro'yxati")
    print("- emails.txt - Email ro'yxati")
    print("\n🚀 Foydalanish:")
    print("1. Sozlamalarni to'g'rilang")
    print("2. Proxy va email fayllarini tayyorlang")
    print("3. Dasturni ishga tushiring")
    print("\n⚠️  Eslatma:")
    print("- Faqat o'quv maqsadlarida ishlatish kerak")
    print("- Google xizmat shartlariga rioya qiling")
    print("="*50)

def handle_main_menu():
    """Asosiy menyuni boshqarish."""
    while True:
        show_main_menu()
        choice = input("\nTanlang (0-6): ").strip()
        
        if choice == "1":
            return "create_account"
        elif choice == "2":
            handle_settings_menu()
        elif choice == "3":
            handle_file_management_menu()
        elif choice == "4":
            show_statistics()
        elif choice == "5":
            handle_test_menu()
        elif choice == "6":
            show_help()
        elif choice == "0":
            print("\n👋 Xayr!")
            sys.exit(0)
        else:
            print("❌ Noto'g'ri tanlov!")

def handle_settings_menu():
    """Sozlamalar menyusini boshqarish."""
    while True:
        show_settings_menu()
        choice = input("\nTanlang (0-5): ").strip()
        
        if choice == "1":
            show_config_info()
        elif choice == "2":
            edit_config()
        elif choice == "3":
            show_proxy_list()
        elif choice == "4":
            show_email_list()
        elif choice == "5":
            show_user_agent_info()
        elif choice == "0":
            break
        else:
            print("❌ Noto'g'ri tanlov!")

def handle_file_management_menu():
    """Fayl boshqarish menyusini boshqarish."""
    while True:
        show_file_management_menu()
        choice = input("\nTanlang (0-5): ").strip()
        
        if choice == "1":
            from utils.config_loader import create_sample_config
            create_sample_config()
        elif choice == "2":
            create_proxy_file()
        elif choice == "3":
            create_email_file()
        elif choice == "4":
            show_files_info()
        elif choice == "5":
            clear_logs()
        elif choice == "0":
            break
        else:
            print("❌ Noto'g'ri tanlov!")

def handle_test_menu():
    """Test menyusini boshqarish."""
    while True:
        show_test_menu()
        choice = input("\nTanlang (0-5): ").strip()
        
        if choice == "1":
            test_config()
        elif choice == "2":
            test_proxies()
        elif choice == "3":
            test_emails()
        elif choice == "4":
            test_user_agents()
        elif choice == "5":
            test_internet()
        elif choice == "0":
            break
        else:
            print("❌ Noto'g'ri tanlov!")

def show_config_info():
    """Config ma'lumotlarini ko'rsatish."""
    config = load_config('config.json')
    if config:
        print("\n📋 CONFIG MA'LUMOTLARI:")
        print(f"IMAP Server: {config.get('imap', {}).get('server', 'N/A')}")
        print(f"IMAP Port: {config.get('imap', {}).get('port', 'N/A')}")
        print(f"IMAP Username: {config.get('imap', {}).get('username', 'N/A')}")
        print(f"CAPTCHA API: {'Mavjud' if config.get('captcha', {}).get('api_key') else 'Yo\'q'}")
    else:
        print("❌ Config fayli topilmadi")

def edit_config():
    """Config faylini tahrirlash."""
    print("⚠️  Config faylini qo'lda tahrirlash kerak")
    print("📁 config.json faylini ochib, ma'lumotlarni kiriting")

def show_proxy_list():
    """Proxy ro'yxatini ko'rsatish."""
    proxies = get_proxy_list()
    if proxies:
        print(f"\n🌐 PROXY RO'YXATI ({len(proxies)} ta):")
        for i, proxy in enumerate(proxies[:10], 1):
            print(f"{i}. {proxy}")
        if len(proxies) > 10:
            print(f"... va {len(proxies) - 10} ta yana")
    else:
        print("❌ Proxy'lar topilmadi")

def show_email_list():
    """Email ro'yxatini ko'rsatish."""
    emails = get_email_list()
    if emails:
        print(f"\n📧 EMAIL RO'YXATI ({len(emails)} ta):")
        for i, email in enumerate(emails[:10], 1):
            print(f"{i}. {email}")
        if len(emails) > 10:
            print(f"... va {len(emails) - 10} ta yana")
    else:
        print("❌ Email'lar topilmadi")

def show_user_agent_info():
    """User Agent ma'lumotlarini ko'rsatish."""
    print("\n🌐 USER AGENT MA'LUMOTLARI:")
    print(f"Tasodifiy: {get_random_user_agent()}")
    print(f"Chrome: {get_user_agent_by_type('chrome')}")
    print(f"Firefox: {get_user_agent_by_type('firefox')}")

def show_files_info():
    """Fayllar haqida ma'lumot ko'rsatish."""
    print("\n📁 FAYLLAR MA'LUMOTI:")
    
    files = [
        ('config.json', 'Sozlamalar'),
        ('proxy.txt', 'Proxy ro\'yxati'),
        ('emails.txt', 'Email ro\'yxati'),
        ('logs/signup_activity.log', 'Log fayli')
    ]
    
    for file_path, description in files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {description}: {size} bayt")
        else:
            print(f"❌ {description}: mavjud emas")

def clear_logs():
    """Log fayllarini tozalash."""
    try:
        if os.path.exists('logs/signup_activity.log'):
            os.remove('logs/signup_activity.log')
            print("✅ Log fayllari tozalandi")
        else:
            print("📝 Log fayllari mavjud emas")
    except Exception as e:
        print(f"❌ Log tozalashda xatolik: {e}")

def test_config():
    """Config test qilish."""
    config = load_config('config.json')
    if config and validate_config(config):
        print("✅ Config test muvaffaqiyatli")
    else:
        print("❌ Config testda xatolik")

def test_proxies():
    """Proxy test qilish."""
    proxies = get_proxy_list()
    if proxies:
        print(f"✅ Proxy test muvaffaqiyatli: {len(proxies)} ta")
    else:
        print("❌ Proxy testda xatolik")

def test_emails():
    """Email test qilish."""
    emails = get_email_list()
    if emails:
        print(f"✅ Email test muvaffaqiyatli: {len(emails)} ta")
    else:
        print("❌ Email testda xatolik")

def test_user_agents():
    """User Agent test qilish."""
    try:
        ua = get_random_user_agent()
        print(f"✅ User Agent test muvaffaqiyatli: {ua}")
    except Exception as e:
        print(f"❌ User Agent testda xatolik: {e}")

def test_internet():
    """Internet ulanish test qilish."""
    try:
        import requests
        response = requests.get('https://www.google.com', timeout=5)
        print("✅ Internet ulanish mavjud")
    except Exception as e:
        print(f"❌ Internet ulanish yo'q: {e}")