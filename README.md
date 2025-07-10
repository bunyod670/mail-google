# Google Account Creator

Bu loyiha Google hisoblarini avtomatik yaratish uchun mo'ljallangan. IMAP orqali verification kodini oladi va CAPTCHA'ni avtomatik yechadi.

## 🚀 Xususiyatlar

- ✅ Chrome WebDriver bilan avtomatik signup
- ✅ IMAP orqali verification kodini olish
- ✅ 2Captcha API bilan CAPTCHA yechish
- ✅ Cookie va sessiyalarni saqlash
- ✅ Batafsil log yozish
- ✅ Skrinshot saqlash
- ✅ Antibot texnikalari

## 📁 Loyiha tuzilmasi

```
project_root/
├── modules/
│   └── google_signup_with_verification.py   # Asosiy modul
├── utils/
│   ├── logger.py
│   ├── imap_verifier.py
│   ├── captcha_solver.py
│   ├── session_manager.py
│   ├── config_loader.py
│   └── random_delay.py
├── logs/
│   └── signup_activity.log
├── cookies/
│   └── *.json
├── screenshots/
│   └── *.png
├── config.json
├── main.py
├── requirements.txt
└── README.md
```

## 🛠️ O'rnatish

1. **Kutubxonalarni o'rnatish:**
```bash
pip install -r requirements.txt
```

2. **Chrome WebDriver o'rnatish:**
```bash
# Linux uchun
sudo apt-get install chromium-browser

# Windows uchun
# Chrome brauzerini o'rnatish kerak
```

3. **Config faylini sozlash:**
```bash
python main.py --create-config
```

## ⚙️ Sozlash

`config.json` faylini o'zgartiring:

```json
{
  "imap": {
    "server": "mail.yourdomain.com",
    "port": 993,
    "username": "user@yourdomain.com",
    "password": "yourpassword"
  },
  "chrome": {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "proxy": "http://ip:port"
  },
  "captcha": {
    "api_key": "YOUR_2CAPTCHA_KEY"
  }
}
```

## 🚀 Foydalanish

### Asosiy foydalanish:
```bash
python main.py
```

### Config test qilish:
```bash
python main.py --test-config
```

### Namuna config yaratish:
```bash
python main.py --create-config
```

### Yordam:
```bash
python main.py --help
```

## 📋 Kerakli ma'lumotlar

- **IMAP server** - Email server ma'lumotlari
- **2Captcha API key** - CAPTCHA yechish uchun
- **Proxy** (ixtiyoriy) - IP yashirish uchun

## 🔧 Modullar

### modules/google_signup_with_verification.py
- Chrome sessiyani yaratish
- Google signup sahifasini ochish
- Formani to'ldirish
- Verification kodini kutish
- CAPTCHA yechish
- Cookie'larni saqlash

### utils/logger.py
- Log yozish funksiyalari
- Xatolik boshqarish

### utils/imap_verifier.py
- IMAP serverga ulanish
- Email o'qish
- Verification kod ajratish

### utils/captcha_solver.py
- CAPTCHA aniqlash
- 2Captcha API bilan yechish
- Skrinshot saqlash

### utils/session_manager.py
- Cookie'larni saqlash/yuklash
- Sessiya boshqarish

### utils/config_loader.py
- Config faylini yuklash
- Sozlamalarni tekshirish

### utils/random_delay.py
- Antibot kutish funksiyalari

## 📊 Natija

Dastur muvaffaqiyatli yakunlanganda quyidagi natija qaytaradi:

```json
{
  "email": "user123@yourdomain.com",
  "status": "created",
  "cookies": "cookies/user123_yourdomain_com.json",
  "screenshot": "screenshots/final_user123_yourdomain_com.png",
  "timestamp": "2025-07-10T19:00:00"
}
```

## ⚠️ Eslatmalar

- Bu dastur faqat o'quv maqsadlarida ishlatilishi kerak
- Google xizmat shartlariga rioya qiling
- Proxy va CAPTCHA xizmatlarini to'g'ri sozlang
- Test muhitida sinab ko'ring

## 🐛 Xatoliklar

Agar muammo yuzaga kelsa:

1. Log faylini tekshiring: `logs/signup_activity.log`
2. Config faylini to'g'ri sozlang
3. Chrome WebDriver o'rnatilganligini tekshiring
4. Internet ulanishini tekshiring

## 📞 Yordam

Muammo yoki savol bo'lsa, loyiha muallifiga murojaat qiling.