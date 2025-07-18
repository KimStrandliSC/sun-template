import pathlib
import tomllib
from sun_sgtk import sgtk_build_tool, sg_utils


def main():
    repo_root = pathlib.Path(__file__).parent
    sgtk_dir = repo_root / "sgtk"
    build_dir = repo_root / "build"
    # build_dir = pathlib.Path(r"W:\temp\pyprojectBuild")
    build_dir.mkdir(exist_ok=True)


    pyproject_path = repo_root / "pyproject.toml"
    if not pyproject_path.is_file():
        raise ValueError(f"pyproject.toml file not found at {pyproject_path}. Cannot build SGTK.")

    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    sgtk_config = config.get("tool", {}).get("sgtk_build")
    if not sgtk_config:
        raise ValueError("No 'sgtk_build' configuration found in pyproject.toml. Cannot build SGTK.")



    zip_package = sgtk_build_tool.build_sgtk(
        repo_root=repo_root,
        build_dir=build_dir,
        sgtk_dir=sgtk_dir,
        keep_build_dir=False,
        use_venv_packages=False,
    )
    print(f"Built SGTK package: {zip_package}")



    # ### UPLOAD TO FLOW
    # sgtk_name = sgtk_config.get("sgtk_name")
    # print(f'Uploading SGTK bundle {zip_package.name} to Flow')
    # result = sg_utils.upload_toolkit_bundle(bundle_name=sgtk_name, zip_file_path=zip_package)
    # print(result)



if __name__ == '__main__':
    main()