from helpers.config import get_settings ,settings


class BaseController :
    def __init__(self):
        self.app_settings = get_settings()