import imaplib
import email
import re
import time
from email.header import decode_header
from utils.logger import log_info, log_error, log_debug

def connect_imap(email_addr, password, server, port=993):
    """IMAP serverga ulanish."""
    try:
        # IMAP serverga ulanish
        imap = imaplib.IMAP4_SSL(server, port)
        imap.login(email_addr, password)
        
        log_info(f"IMAP serverga muvaffaqiyatli ulandi: {server}")
        return imap
    
    except imaplib.IMAP4.error as e:
        log_error(f"IMAP autentifikatsiya xatosi: {e}")
        return None
    except Exception as e:
        log_error(f"IMAP ulanishda xatolik: {e}")
        return None

def fetch_latest_email(imap, subject_filter, timeout=120):
    """Inboxdan kerakli emailni topish."""
    try:
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Inbox papkasini tanlash
            imap.select('INBOX')
            
            # Barcha email'larni olish
            _, message_numbers = imap.search(None, 'ALL')
            email_list = message_numbers[0].split()
            
            if not email_list:
                log_debug("Inbox bo'sh")
                time.sleep(5)
                continue
            
            # Eng so'nggi email'dan boshlab tekshirish
            for num in reversed(email_list):
                _, msg_data = imap.fetch(num, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # Subject'ni olish
                subject = decode_header(email_message["subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                
                log_debug(f"Email subject: {subject}")
                
                # Subject filter'ni tekshirish
                if subject_filter.lower() in subject.lower():
                    log_info(f"Kerakli email topildi: {subject}")
                    return email_message
            
            log_debug("Kerakli email topilmadi, 5 soniya kutish...")
            time.sleep(5)
        
        log_error(f"Timeout: {timeout} soniya ichida email topilmadi")
        return None
    
    except Exception as e:
        log_error(f"Email olishda xatolik: {e}")
        return None

def extract_verification_code(email_body):
    """Email'dan verification kodni regex bilan ajratib olish."""
    try:
        # Email body'ni olish
        if email_body.is_multipart():
            for part in email_body.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_body.get_payload(decode=True).decode()
        
        log_debug(f"Email body: {body[:200]}...")
        
        # Turli xil verification kod formatlarini qidirish
        patterns = [
            r'\b\d{6}\b',  # 6 xonali kod
            r'\b\d{4}\b',  # 4 xonali kod
            r'verification code[:\s]*(\d+)',
            r'code[:\s]*(\d+)',
            r'(\d{4,6})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, body, re.IGNORECASE)
            if matches:
                code = matches[0] if isinstance(matches[0], str) else str(matches[0])
                log_info(f"Verification kod topildi: {code}")
                return code
        
        log_error("Verification kod topilmadi")
        return None
    
    except Exception as e:
        log_error(f"Verification kod ajratishda xatolik: {e}")
        return None

def disconnect_imap(imap):
    """IMAP ulanishni uzish."""
    try:
        imap.logout()
        log_info("IMAP ulanish uzildi")
    except Exception as e:
        log_error(f"IMAP uzishda xatolik: {e}")

def get_email_count(imap):
    """Inbox'dagi email'lar sonini olish."""
    try:
        imap.select('INBOX')
        _, message_numbers = imap.search(None, 'ALL')
        count = len(message_numbers[0].split())
        log_debug(f"Inbox'dagi email'lar soni: {count}")
        return count
    except Exception as e:
        log_error(f"Email sonini olishda xatolik: {e}")
        return 0