# std
from pathlib import Path
from typing import List
import subprocess
import os
import pytest

# 3rd
import matplotlib

# ours
from sunburst import base_dir

matplotlib.use("AGG")


def get_all_example_files() -> List[Path]:
    examples_dir = base_dir.parent / "examples"
    return [
        f
        for f in examples_dir.iterdir()
        if f.is_file() and "example" in f.name and not f.name.startswith("_")
    ]


@pytest.mark.parametrize("file", get_all_example_files())
def test_example(file):
    subprocess.run(
        ["python3", file], check=True, env={**os.environ, "NOPLOT": "true"}
    )
