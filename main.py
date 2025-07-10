from modules.google_signup_with_verification import create_google_account_with_verification
from utils.config_loader import load_config
from utils.logger import log_info, log_error
import sys

if __name__ == "__main__":
    try:
        config = load_config('config.json')
        # user_data ni config yoki inputdan oling
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'user123@yourdomain.com',
            'password': 'StrongPassword123!',
            'birth_day': '10',
            'birth_month': 'July',
            'birth_year': '1990',
            'gender': 'male'
        }
        result = create_google_account_with_verification(user_data, config)
        print(result)
    except Exception as e:
        log_error(str(e))
        sys.exit(1)