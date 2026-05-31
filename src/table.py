from rich.console import Console
from rich.table import Table
from pathlib import Path
import typer

console = Console()


class MakeTable:
    SDDM_THEMES_PATH = Path("/usr/share/sddm/themes")

    def __init__(self):
        try:
            self.themes_folder = []
            for theme_folder in self.SDDM_THEMES_PATH.iterdir():
                if theme_folder.exists() and theme_folder.is_dir():
                    if len(list(theme_folder.rglob("*.conf"))) > 0:
                        self.themes_folder.append(theme_folder)
            self.themes_folder.sort()

        except FileNotFoundError:
            console.print(
                f"\n[red]This folder is not exist on your system[/red]:\n{SDDM_THEMES_PATH}")
            raise typer.Exit(1)

    def package(self) -> dict[str, dict[str, dict[str, str | list]] | Table]:
        table = Table(
            title="What [yellow]Package[/yellow] do you want to [bold green]use[/bold green]?")
        table.add_column("[bold cyan]ID[/bold cyan]")
        table.add_column("[bold cyan]Package[/bold cyan]")
        table.add_column("[bold cyan]Themes Count[/bold cyan]")

        data = {}
        for i, theme_folder in enumerate(self.themes_folder):
            themes = {}
            for theme in theme_folder.rglob("*.conf"):
                theme_parent = theme.parent
                if len(list(theme_parent.rglob("*.conf"))) > 1:
                    themes[theme] = {"name": theme.stem}
                else:
                    themes[theme] = {"name": theme_parent.name}

            theme_counts = str(len(themes))

            data[str(i+1)] = {
                "name": theme_folder.name,
                "path": theme_folder,
                "themes": themes,
                "theme_counts": theme_counts
            }

        for ID, content in data.items():
            package_name = content.get("name")
            theme_counts = content.get("theme_counts")
            table.add_row(
                f"[green]{ID}[/green]",
                f"[blue]{package_name}[/blue]",
                f"[red]{theme_counts}[/red]"
            )

        return {"data": data, "table": table}

    def themes(self, themes: dict, visited_theme: list) -> Table:
        table = Table(
            title=f"Select a [yellow]Theme[/yellow] to [red]preview[/red]")
        table.add_column("[bold cyan]ID[/bold cyan]")
        table.add_column("[bold cyan]Theme Name[/bold cyan]")

        arr_themes = list(themes.items())
        arr_themes.sort(key=lambda x: x[1]["name"])
        for i, theme in enumerate(arr_themes):
            if theme[0] in visited_theme:
                table.add_row(
                    f"[green]{i+1}[/green]",
                    f"{theme[1]["name"]}",
                )
            else:
                table.add_row(
                    f"[green]{i+1}[/green]",
                    f"[bold blue]{theme[1]["name"]}[/bold blue]",
                )

        return table
