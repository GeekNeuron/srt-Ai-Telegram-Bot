# این فایل شامل تعریف کلاس TranslationRequest است

class TranslationRequest:
    """
    کلاس درخواست ترجمه.
    """
    def __init__(self, chat_id: str, file_info: telebot.types.File,
                 source_language: str, target_language: str, translation_style: str,
                 gemini_api_key: str):
        """
        سازنده کلاس.
        """
        self.chat_id = chat_id
        self.file_info = file_info
        self.source_language = source_language
        self.target_language = target_language
        self.translation_style = translation_style
        self.gemini_api_key = gemini_api_key
