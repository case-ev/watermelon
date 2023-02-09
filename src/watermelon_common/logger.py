"""
watermelon_common.logger
------------------------
Creation and setup for the logger used by watermelon and its related
packages.
"""

import logging
import os
from datetime import datetime

from watermelon_utils.console import AsciiColors


LOGGER = logging.Logger("watermelon")

# Formatter for the files
log_fmt = logging.Formatter(
    fmt="[%(asctime)s](%(filename)s:%(lineno)d) %(levelname)s :: %(message)s",
    datefmt="%Y-%m-%d|%H:%M:%S",
)


# Formatter for the console
class CustomFormatter(logging.Formatter):
    """Custom formatter for the watermelon logger"""

    FMT = f"{AsciiColors.BG_MAGENTA}[%(asctime)s](%(filename)s:%(lineno)d){AsciiColors.BG_RESET} \
{{}}%(levelname)s{AsciiColors.RESET} :: %(message)s"
    DATE_FMT = "%Y-%m-%d|%H:%M:%S"
    COLORS = {
        logging.DEBUG: AsciiColors.CYAN,
        logging.INFO: AsciiColors.GREEN,
        logging.WARNING: AsciiColors.YELLOW,
        logging.ERROR: AsciiColors.RED,
        logging.CRITICAL: AsciiColors.BOLD_RED,
    }

    def format(self, record):
        fmt = self.FMT.format(self.COLORS.get(record.levelno))
        formatter = logging.Formatter(
            fmt=fmt,
            datefmt=self.DATE_FMT,
        )
        return formatter.format(record)


def setup_logger(quiet=False, debug=False, verbose=False, log_dir=False):
    """Setup the logger.

    This must be run at the beginning of every program that uses
    watermelon or its related packages.

    Parameters
    ----------
    quiet : bool, optional
        Whether to silence all logs, by default False
    debug : bool, optional
        Run in debug mode, which shows all log levels and adds extra
        functionality that might be useful when debugging a watermelon
        program, by default False
    verbose : bool, optional
        Run in verbose mode, which shows all logs at INFO level, by
        default False
    log_dir : bool, optional
        Directory to save all logs, by default False. If it it False,
        the program doesn't store the logs; if it is a string
        corresponding to a directory, it generates a file within it
        with the current time and date as name, and if it corresponds
        to a file then it outputs to the given file, overwriting if
        necessary
    """

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

    # File logger
    if log_dir:
        if "." in log_dir:
            # Assume log_dir is a file
            file_path = log_dir
        else:
            # Assume log_dir is a directory
            now = datetime.now()
            file_name = f"{now.year}{now.month:02}{now.day:02}_{now.hour:02}\
{now.minute:02}{now.second:02}"
            file_path = os.path.join(log_dir, f"{file_name}.txt")
        file_hdl = logging.FileHandler(file_path, encoding="utf-8")
        file_hdl.setFormatter(log_fmt)
        file_hdl.setLevel(logging.DEBUG)
        LOGGER.addHandler(file_hdl)
        LOGGER.debug("Log file: %s", os.path.abspath(file_path))
