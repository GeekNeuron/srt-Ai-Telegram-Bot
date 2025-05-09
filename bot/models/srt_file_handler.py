# این فایل شامل تعریف کلاس SrtFileHandler است

import logging
from typing import Optional

class SrtFileHandler:
    """
    کلاس مدیریت فایل SRT.
    """
    def __init__(self, file_path: str):
        """
        سازنده کلاس.
        """
        self.file_path = file_path

    def read_file_content(self) -> Optional[str]:
        """
        خواندن محتوای فایل SRT.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"فایل SRT یافت نشد: {self.file_path}")
            return None
        except Exception as e:
            logging.exception(f"خطا در خواندن فایل SRT: {e}")
            return None
