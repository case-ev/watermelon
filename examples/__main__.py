import sys
import pathlib
import os
import importlib

# Change the import path
src_path = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent, "src")
os.environ["PYTHONPATH"] = str(src_path)
sys.path.append(str(src_path))

from watermelon_common.logger import setup_logger, LOGGER
import argparse


# Set up argument parsing
desc_str = """run the examples"""

PARSER = argparse.ArgumentParser(prog="examples", description=desc_str)
PARSER.add_argument(
    "args",
    nargs="+",
    help="program and its arguments",
)
PARSER.add_argument(
    "-d",
    "--debug",
    action="store_true",
    help="run in debug mode",
)
PARSER.add_argument(
    "--log",
    action="store",
    default=os.path.join(src_path.parent, "logs"),
    help="generate log files for the current run in the given directory",
)
PARSER.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    help="disable logging",
)
PARSER.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="run in verbose mode",
)

cmd_args = PARSER.parse_args()
try:
    setup_logger(cmd_args.quiet, cmd_args.debug, cmd_args.verbose, cmd_args.log)
except FileNotFoundError:
    os.mkdir(cmd_args.log)
    setup_logger(cmd_args.quiet, cmd_args.debug, cmd_args.verbose, cmd_args.log)

# Get the attributes
name = cmd_args.args[0]
ex_args = []
ex_kwargs = {}
LOGGER.info("Parsing args and kwargs")
for arg in map(lambda x: x.split("="), cmd_args.args[1:]):
    if len(arg) == 2:
        key, val = arg
        ex_kwargs[key] = val
    else:
        ex_args.extend(arg)

# Run the example
print(
    f"\nExecuting example '\x1b[32;20m{name}\x1b[0m' with args {ex_args} and kwargs {ex_kwargs}\n"
)
LOGGER.info(f"Importing example {name}")
mod = importlib.import_module(f"examples.{name}")
LOGGER.info(f"Running main function")
mod.main(*ex_args, **ex_kwargs)
