class StreamStatsError(Exception):
    """
    Базовая ошибка программы
    """


class UnsupportedFormatError(StreamStatsError):
    """
    Ошибка: формат файла не поддерживается
    """
    def __init__(self, format: str) -> None:
        super().__init__(f"Формат {format} не поддерживается")


class InvalidEventError(StreamStatsError):
    """
    Ошибка: в строке файла неверное событие
    """
    def __init__(self, message: str, path=None, line=None, field=None) -> None:
        self.path = path
        self.line = line
        self.field = field

        text = message
        if field is not None:
            text = f"Поле {field}: {text}"
        if path is not None:
            text = f"{path}, строка {line}: {text}"
        super().__init__(text)


class InvalidTimestampError(InvalidEventError):
    """
    Ошибка: неверная дата или уровень в событии
    """


class CLIConfigError(StreamStatsError):
    """
    Ошибка: неверные параметры командной строки
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)