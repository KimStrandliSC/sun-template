import tomllib
import subprocess
import sys
from pathlib import Path


def main():
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    sgtk_build = config["tool"]["sgtk_build"]
    build_deps = sgtk_build.get("build_dependencies", [])

    # Install build dependencies
    if build_deps:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + build_deps)


if __name__ == '__main__':
    main()