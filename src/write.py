from configparser import ConfigParser
from pathlib import Path
import sys


def fix_sddm_conf(backup=True):
    config_path = Path("toch.py")
    backup_config_path = config_path.with_name(f"_{config_path.name}")

    config = ConfigParser()
    config.optionxform = str  # preserve original case

    if config_path.exists():
        config.read(config_path)
    else:
        config_path.touch()
        config.add_section("Theme")

    config.set("Theme", "Current", ".")

    if not backup_config_path.exists():
        config_path.move(backup_config_path)
    with open(config_path, 'w') as f:
        config.write(f)


def change_metadata(theme: str):
    theme = Path(theme)
    sddm_themes_path = Path("/usr/share/sddm/themes")
    theme_base_folder = sddm_themes_path / str(theme.absolute()).split("/")[5]
    metadata_path = sddm_themes_path / "metadata.desktop"

    for qml in theme_base_folder.rglob("*ain.qml"):
        if qml.parent == theme.parent or qml.parent == theme_base_folder:
            mainscript = "/".join(str(qml.absolute()).split("/")[5:])

    theme_r = "/".join(str(theme.absolute()).split("/")[5:])
    config = ConfigParser()
    config.optionxform = str
    config["SddmGreeterTheme"] = {
        "Type": "sddm-theme",
        "Name": "sddm_preview",
        "Description": "A SDDM theme management",
        "QtVersion": "6",
        "MainScript": mainscript,
        "ConfigFile": theme_r,
    }

    with open(metadata_path, "w") as f:
        config.write(f)


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == "config":
            fix_sddm_conf()
        elif args[1] == "metadata":
            change_metadata(args[2])
