# این فایل شامل توابع مربوط به رمزنگاری و امنیت است

import logging
from cryptography.fernet import Fernet
import string
from ..config import ALLOWED_CHARACTERS_FILENAME

def generate_encryption_key() -> bytes:
    """
    تولید یک کلید رمزنگاری Fernet.
    """
    return Fernet.generate_key()

def encrypt_api_key(api_key: str, encryption_key: bytes) -> str:
    """
    رمزنگاری API Key با استفاده از Fernet.
    """
    f = Fernet(encryption_key)
    api_key_bytes = api_key.encode('utf-8')
    encrypted_api_key_bytes = f.encrypt(api_key_bytes)
    return encrypted_api_key_bytes.decode('utf-8')

def decrypt_api_key(encrypted_api_key: str, encryption_key: bytes) -> str:
    """
    رمزگشایی API Key رمزنگاری شده با Fernet.
    """
    try:
        f = Fernet(encryption_key)
        encrypted_api_key_bytes = encrypted_api_key.encode('utf-8')
        api_key_bytes = f.decrypt(encrypted_api_key_bytes)
        return api_key_bytes.decode('utf-8')
    except Exception as e:
        logging.error(f"خطا در رمزگشایی API Key: {e}")
        return ""

def is_filename_safe(filename: str) -> bool:
    """
    بررسی می‌کند که آیا نام فایل امن است یا خیر.
    """
    for char in filename:
        if char not in ALLOWED_CHARACTERS_FILENAME:
            return False
    return True

def validate_file_name(file_name: str) -> str:
    """
    اعتبارسنجی نام فایل و حذف کاراکترهای غیرمجاز.
    """
    cleaned_filename = ''.join(c for c in file_name if c in ALLOWED_CHARACTERS_FILENAME)
    if cleaned_filename != file_name:
        logging.warning("نام فایل شامل کاراکترهای غیرمجاز بود و اصلاح شد.")
    return cleaned_filename
