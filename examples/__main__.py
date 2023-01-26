import sys
import os
import pathlib


src_path = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent, "src")

args = sys.argv[1:]
args[0] = os.path.join("examples", f"{sys.argv[1]}.py")

os.environ["PYTHONPATH"] = str(src_path)
os.system(f"python {' '.join(args)}")
