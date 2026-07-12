from app.config import Settings, get_settings

def get_settings_dep() -> Settings:
    """
    Dependency to retrieve application settings.
    """
    return get_settings()
