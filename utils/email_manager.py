import os
import random
from utils.logger import log_info, log_error, log_debug

def load_emails_from_file(file_path="emails.txt"):
    """Email ro'yxatini fayldan o'qish."""
    try:
        if not os.path.exists(file_path):
            log_error(f"Email fayli topilmadi: {file_path}")
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            emails = [line.strip() for line in f if line.strip()]
        
        log_info(f"Email ro'yxati yuklandi: {len(emails)} ta")
        return emails
    
    except Exception as e:
        log_error(f"Email faylini o'qishda xatolik: {e}")
        return []

def get_random_email(email_list):
    """Tasodifiy email qaytarish."""
    if not email_list:
        return None
    
    email = random.choice(email_list)
    log_debug(f"Tanlangan email: {email}")
    return email

def validate_email(email):
    """Email formatini tekshirish."""
    if not email:
        return False
    
    # Oddiy email formatini tekshirish
    if '@' in email and '.' in email.split('@')[1]:
        return True
    
    return False

def create_email_file():
    """Namuna email faylini yaratish."""
    sample_emails = [
        "user1@yourdomain.com",
        "user2@yourdomain.com",
        "user3@yourdomain.com",
        "test1@yourdomain.com",
        "test2@yourdomain.com"
    ]
    
    try:
        with open('emails.txt', 'w', encoding='utf-8') as f:
            for email in sample_emails:
                f.write(f"{email}\n")
        
        log_info("Namuna email fayli yaratildi: emails.txt")
        return True
    except Exception as e:
        log_error(f"Email faylini yaratishda xatolik: {e}")
        return False

def get_email_list():
    """Email ro'yxatini o'qish va tekshirish."""
    emails = load_emails_from_file()
    
    if not emails:
        log_warning("Email fayli bo'sh yoki topilmadi")
        return []
    
    # Email'larni tekshirish
    valid_emails = []
    for email in emails:
        if validate_email(email):
            valid_emails.append(email)
        else:
            log_warning(f"Noto'g'ri email format: {email}")
    
    log_info(f"To'g'ri formatdagi email'lar: {len(valid_emails)}/{len(emails)}")
    return valid_emails

def generate_user_data_from_email(email):
    """Email'dan foydalanuvchi ma'lumotlarini yaratish."""
    try:
        username = email.split('@')[0]
        
        # Ism va familiya yaratish
        first_names = ["John", "Jane", "Mike", "Sarah", "David", "Lisa", "Alex", "Emma"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        # Parol yaratish
        password = f"StrongPass{random.randint(100, 999)}!"
        
        # Tug'ilgan sana
        birth_day = str(random.randint(1, 28))
        birth_month = random.choice(["January", "February", "March", "April", "May", "June", 
                                   "July", "August", "September", "October", "November", "December"])
        birth_year = str(random.randint(1980, 2000))
        
        # Jinsi
        gender = random.choice(["male", "female"])
        
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'birth_day': birth_day,
            'birth_month': birth_month,
            'birth_year': birth_year,
            'gender': gender
        }
        
        log_debug(f"Foydalanuvchi ma'lumotlari yaratildi: {email}")
        return user_data
        
    except Exception as e:
        log_error(f"Foydalanuvchi ma'lumotlarini yaratishda xatolik: {e}")
        return None