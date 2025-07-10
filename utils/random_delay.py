import random
import time

def wait_random(min_sec=2, max_sec=5):
    """Tasodifiy kutish (antibot uchun)."""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)