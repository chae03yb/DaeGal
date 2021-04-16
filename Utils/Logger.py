import datetime
from io import TextIOWrapper

def write(logtype: str, message: str, logfile: TextIOWrapper) -> None:
    """
    `logtype`: INFO | ERROR | WARNING
    `message`: log message
    `logfile`: log file
    """
    print(f"[{logtype}][{datetime.datetime.now().isoformat()}]: {message}", file=logfile)