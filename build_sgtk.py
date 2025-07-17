import pathlib
import tomllib
from sun_sgtk import build_sgtk, sgtk_build_tool

def main():
    repo_root = pathlib.Path(__file__).parent
    sgtk_dir = repo_root / "sgtk"
    build_dir = repo_root / "build"
    build_dir.mkdir(exist_ok=True)

    # pyproject_path = repo_root / "pyproject.toml"
    # with open(pyproject_path, "rb") as f:
    #     config = tomllib.load(f)
    # sgtk_config = config["tool"]["sgtk_build"]

    zip_package = sgtk_build_tool.build_sgtk(
        pyproject=pyproject_path,
        sgtk_dir=sgtk_dir,
        build_dir=build_dir,
        python_includes=[],
        ignore_paths=[]
    )

    # zip_package = build_sgtk.main(
    #     repo_root=repo_root,
    #     sgtk_dir=sgtk_dir,
    #     build_dir=build_dir
    # )
    print(f"Built SGTK package: {zip_package}")

    ### UPLOAD TO FLOW


if __name__ == '__main__':
    main()