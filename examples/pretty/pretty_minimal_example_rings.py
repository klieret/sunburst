import matplotlib
import sys
import os.path

matplotlib.use("AGG")

matplotlib.rcParams["font.sans-serif"] = ["Ubuntu"]
matplotlib.rc("font", weight="light")


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import minimal_example_rings
