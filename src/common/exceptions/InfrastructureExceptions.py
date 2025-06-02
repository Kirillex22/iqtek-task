class ConfigurationException(Exception):
    code = "VALIDATION_ERROR"

    def __init__(self):
        super().__init__(f"Ошибка конфигурации.")
