import random
from utils.logger import log_info, log_debug

# Real User Agent'lar ro'yxati
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]

def get_random_user_agent():
    """Tasodifiy User Agent qaytarish."""
    user_agent = random.choice(USER_AGENTS)
    log_debug(f"Tanlangan User Agent: {user_agent}")
    return user_agent

def get_user_agent_by_type(browser_type="chrome"):
    """Brauzer turiga qarab User Agent qaytarish."""
    if browser_type.lower() == "chrome":
        chrome_agents = [ua for ua in USER_AGENTS if "Chrome" in ua and "Edge" not in ua]
        return random.choice(chrome_agents)
    elif browser_type.lower() == "firefox":
        firefox_agents = [ua for ua in USER_AGENTS if "Firefox" in ua]
        return random.choice(firefox_agents)
    elif browser_type.lower() == "edge":
        edge_agents = [ua for ua in USER_AGENTS if "Edge" in ua]
        return random.choice(edge_agents)
    elif browser_type.lower() == "safari":
        safari_agents = [ua for ua in USER_AGENTS if "Safari" in ua and "Chrome" not in ua]
        return random.choice(safari_agents)
    else:
        return get_random_user_agent()

def get_user_agent_by_os(os_type="windows"):
    """Operatsion tizimga qarab User Agent qaytarish."""
    if os_type.lower() == "windows":
        windows_agents = [ua for ua in USER_AGENTS if "Windows" in ua]
        return random.choice(windows_agents)
    elif os_type.lower() == "mac":
        mac_agents = [ua for ua in USER_AGENTS if "Macintosh" in ua]
        return random.choice(mac_agents)
    elif os_type.lower() == "linux":
        linux_agents = [ua for ua in USER_AGENTS if "Linux" in ua]
        return random.choice(linux_agents)
    else:
        return get_random_user_agent()