def is_valid_user(user_id: int) -> bool:
    from config import Settings
    settings = Settings()
    return str(user_id) == str(settings.manager_id)
