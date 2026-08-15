class FormatEngineError(Exception):
    pass


class UnsupportedFormatError(FormatEngineError):
    pass


class InvalidFileError(FormatEngineError):
    pass


class ParseError(FormatEngineError):
    pass


class WriteError(FormatEngineError):
    pass
