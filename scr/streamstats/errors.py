class StreamStatsError(Exception):
    pass


class UnsupportedFormatError(StreamStatsError):
    def __init__(self, format: str) -> None:
        super().__init__(f"Формат {format} не поддерживается")


class InvalidEventError(StreamStatsError):
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
    pass


class CLIConfigError(StreamStatsError):
    def __init__(self, message: str) -> None:
        super().__init__(message)