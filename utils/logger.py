import logging
import os
from datetime import datetime

# Log papkasini yaratish
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

LOG_FILE = os.path.join(log_dir, 'signup_activity.log')

# Logging konfiguratsiyasi
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_info(message):
    """Ma'lumot logini yozish."""
    logging.info(message)
    print(f"[INFO] {message}")

def log_error(message):
    """Xatolik logini yozish."""
    logging.error(message)
    print(f"[ERROR] {message}")

def log_warning(message):
    """Ogohlantirish logini yozish."""
    logging.warning(message)
    print(f"[WARNING] {message}")

def log_debug(message):
    """Debug logini yozish."""
    logging.debug(message)
    print(f"[DEBUG] {message}")