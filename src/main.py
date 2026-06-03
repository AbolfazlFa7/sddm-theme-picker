from rich.console import Console
from pathlib import Path
from configparser import ConfigParser
import typer
import os
import subprocess
from table import MakeTable
from ask import Ask

app = typer.Typer()
console = Console()

DATA = {
    "sddm_themes_path": Path("/usr/share/sddm/themes"),
    "sddm_config_path": Path("/etc/sddm.conf"),
    "write_file_path": Path(__file__).parent / "write.py",
    "visited_theme": []
}


def make_sddm_conf():
    config = ConfigParser()

    sddm_config_path = Path("/etc/sddm.conf")
    config.read(sddm_config_path)
    if config.get("Theme", "Current") != ".":
        console.print(
            f"\nThis file `{sddm_config_path}` must get this changes to continue:")
        console.print(
            f"[on red][Theme]\nCurrent={config.get("Theme", "Current")}[/on red]")
        console.print("[cyan]↓[cyan]")
        console.print(f"[on green][Theme]\nCurrent=.[/on green]")

        value = Ask.ask_yes_no()
        if value:
            script_path = DATA['write_file_path']
            command = f"sudo python3 {script_path} config"
            code = subprocess.run(command.split())
            if code.returncode != 0:
                raise Exception
        else:
            console.print(
                "[on red]This Operation can not get complete without this![/on red]")
            raise typer.Exit(1)

        return 201
    return 200


def change_metadata():
    metadata_path = DATA["sddm_themes_path"] / "metadata.desktop"
    console.print(
        f"\nThis file `{metadata_path}` must get updated to apply theme to system")

    value = Ask.ask_yes_no()
    if value:
        script_path = DATA['write_file_path']
        theme = DATA["step_2"]["theme"]

        command = f"sudo python3 {script_path} metadata {theme}"
        code = subprocess.run(command.split())

        if code.returncode != 0:
            raise Exception

        return 201
    else:
        return "BACK"


def show_preview():
    command = f"sddm-greeter-qt6  --test-mode --theme {DATA["sddm_themes_path"]} > /dev/null 2>&1"

    result = make_sddm_conf()
    if result == 201:
        console.print(
            "[green]old `sddm.conf` has been renamed too `_sddm.conf`[/green]")
        console.print("[bold green]SDDM Config get updated![/bold green]")
    elif result == 200:
        console.print(
            "[green]SDDM Exists and [bold green]Ok[/bold green][/green]")

    result = change_metadata()
    if result == 201:
        console.print("[bold green]metadata.desktop get updated![/bold green]")
        subprocess.run(command.split(), stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        theme = DATA["step_2"]["theme"]

        DATA["visited_theme"].append(theme)
    elif result == "BACK":
        return "BACK"


@app.command()
def main():
    make_table = MakeTable()
    while True:
        if not DATA.get("step_1"):
            if DATA.get("package"):
                package_table = DATA["package"]["table"]
            else:
                package = make_table.package()
                DATA["package"] = package
                package_table = package["table"]

            console.print()
            console.print(package_table)
            chosen_pkg = Ask.ask_id(len(DATA["package"]["data"]), back=False)
            DATA["step_1"] = {
                "id": chosen_pkg,
                "folder": DATA["package"]["data"][chosen_pkg]
            }

        if not DATA.get("step_2"):
            package = DATA["step_1"]["folder"]
            themes = package.get("themes")

            themes_table = make_table.themes(themes, DATA["visited_theme"])
            console.print()
            console.print(themes_table)
            chosen_theme = Ask.ask_id(
                int(DATA["step_1"]["folder"]["theme_counts"])
            )
            if chosen_theme == None:
                DATA["step_1"] = None
                continue
            else:
                arr_themes = list(themes.items())
                arr_themes.sort(key=lambda x: x[1]["name"])
                DATA["step_2"] = {
                    "id": chosen_theme,
                    "theme": arr_themes[int(chosen_theme) - 1][0]
                }

        if not DATA.get("step_3"):
            result = show_preview()
            if result == "BACK":
                DATA["step_2"] = None
                continue

            value = Ask.ask_yes_no(set_theme=True)
            if value:
                console.print(
                    "[bold green]Theme has set on your System[/bold green]")
            else:
                DATA["step_2"] = None
                continue

        break


if __name__ == "__main__":
    app()
