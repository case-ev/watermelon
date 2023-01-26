import logging
import os
from datetime import datetime


LOGGER = logging.Logger("watermelon")

# Formatter for the files
log_fmt = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s :: %(message)s",
    datefmt="%Y-%m-%d|%H:%M:%S",
)


# Formatter for the console
class CustomFormatter(logging.Formatter):
    GREY     = "\x1b[38;20m"
    YELLOW   = "\x1b[33;20m"
    RED      = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET    = "\x1b[0m"

    FMT = "[%(asctime)s] {}%(levelname)s\x1b[0m :: %(message)s"
    DATE_FMT = "%Y-%m-%d|%H:%M:%S"

    COLORS = {
        logging.DEBUG: GREY,
        logging.INFO: GREY,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: BOLD_RED,
    }

    def format(self, record):
        log_fmt = self.FMT.format(self.COLORS.get(record.levelno))
        formatter = logging.Formatter(
            fmt=log_fmt,
            datefmt=self.DATE_FMT,
        )
        return formatter.format(record)


def setup_logger(quiet=False, debug=False, verbose=False, log_dir=False):
    global LOGGER

    if not quiet:
        # Stream logger
        str_hdl = logging.StreamHandler()
        str_hdl.setFormatter(CustomFormatter())
        if debug:
            str_hdl.setLevel(logging.DEBUG)
        elif verbose:
            str_hdl.setLevel(logging.INFO)
        else:
            str_hdl.setLevel(logging.WARNING)
        LOGGER.addHandler(str_hdl)

    if log_dir:
        # File logger
        now = datetime.now()
        file_name = f"{now.year}{now.month:02}{now.day:02}_{now.hour:02}{now.minute:02}{now.second:02}"
        file_path = os.path.join(log_dir, f"{file_name}.txt")
        file_hdl = logging.FileHandler(file_path, encoding="utf-8")
        file_hdl.setFormatter(log_fmt)
        file_hdl.setLevel(logging.DEBUG)
        LOGGER.addHandler(file_hdl)
        LOGGER.debug(f"Log file: {os.path.abspath(file_path)}")
