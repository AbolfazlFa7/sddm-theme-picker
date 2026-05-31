from rich.console import Console
from rich.prompt import Prompt

console = Console()

class Ask:
    @staticmethod
    def ask_id(max_range, back=True) -> str:
        BACK = ['back','b', 'before']

        while True:
            if back:
                value = Prompt.ask(
                    "Enter a [bold green]ID[/bold green] or '[red]b[/red]' for [red]back[/red]",
                )

                if value in BACK:
                    return None

            else:
                value = Prompt.ask(
                    "Enter a [bold green]ID[/bold green]",
                )

            try:
                if 1 <= int(value) <= max_range:
                    return value

                else:
                    console.print(f"[red]You can choose from [white]1[/white] to [white]{max_range}[/white][/red]")
                    continue
                        
            except ValueError:
                console.print("[red]You must enter [bold red]Digit[/bold red][red]!")
                continue
    
    @staticmethod
    def ask_yes_no(set_theme = False) -> bool | str:
        yes = ['y','yep','ye','yeh','yes']
        no = ['n','no','not']

        while True:
            if set_theme:
                value = Prompt.ask(
                    "Do you want to [bold green]Set[/bold green] this theme? [[bold green]y[/bold green]][yellow]-[/yellow][[bold red]n[/bold red]]"
                )
            else:
                value = Prompt.ask(
                    "Do you want to proceed? [[bold green]y[/bold green]][yellow]-[/yellow][[bold red]n[/bold red]]"
                )

            if value in yes:
                return True
            elif value in no:
                return False
            else:
                console.print("[bold red]Not Valid Option[/bold red]")
                continue
            
