import logging

class LoggingFormatter(logging.Formatter):
    def format(self, record):
        format = "{asctime} | {levelname:<6} | {name} | {message}"
        formatter = logging.Formatter(
            format,
            "%Y-%m-%d %H:%M:%S",
            style="{"
        )
        return formatter.format(record)


