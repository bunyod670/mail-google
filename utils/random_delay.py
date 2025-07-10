import random
import time
from utils.logger import log_debug

def wait_random(min_sec=2, max_sec=5):
    """Tasodifiy kutish (antibot uchun)."""
    delay = random.uniform(min_sec, max_sec)
    log_debug(f"Kutish: {delay:.2f} soniya")
    time.sleep(delay)

def wait_fixed(seconds):
    """Belgilangan vaqt kutish."""
    log_debug(f"Belgilangan kutish: {seconds} soniya")
    time.sleep(seconds)

def wait_human_like():
    """Inson o'xshash kutish (1-3 soniya)."""
    delay = random.uniform(1, 3)
    log_debug(f"Inson o'xshash kutish: {delay:.2f} soniya")
    time.sleep(delay)

def wait_long():
    """Uzoq kutish (5-10 soniya)."""
    delay = random.uniform(5, 10)
    log_debug(f"Uzoq kutish: {delay:.2f} soniya")
    time.sleep(delay)

def wait_short():
    """Qisqa kutish (0.5-1.5 soniya)."""
    delay = random.uniform(0.5, 1.5)
    log_debug(f"Qisqa kutish: {delay:.2f} soniya")
    time.sleep(delay)