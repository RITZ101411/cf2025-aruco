import secrets
import string

def generate_api_key(length=32):
    chars = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(chars) for _ in range(length))
    return api_key

api_key = generate_api_key()
print("Generated API Key:", api_key)