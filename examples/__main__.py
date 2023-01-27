import sys
import pathlib
import os

# Change the import path
src_path = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent, "src")
os.environ["PYTHONPATH"] = str(src_path)
sys.path.append(str(src_path))
try:
    os.mkdir(os.path.join(src_path.parent, "logs"))
except Exception:
    pass

from watermelon_common.logger import setup_logger
import argparse
import examples


# Set up argument parsing
desc_str = """run the examples in watermelon"""

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
setup_logger(cmd_args.quiet, cmd_args.debug, cmd_args.verbose, cmd_args.log)

# Run the examples
for arg in cmd_args.args:
    print(f"\nExecuting example '\x1b[32;20m{arg}\x1b[0m'\n")
    with open(os.path.join("examples", f"{arg}.py"), "r") as f:
        exec(f.read())
