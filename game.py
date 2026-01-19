import cmd
import json
import random
from pathlib import Path
from rich.console import Console # type: ignore
from rich.panel import Panel # type: ignore
from rich.table import Table # type: ignore
from rich import print as rprint # type: ignore
from rich.tree import Tree # type: ignore

from models import Player, World, Battle, Bottyamon

current_world = ""

def checkFile(file):
    dataFile = Path(file)

    if not dataFile.exists():
        rprint(f"[red]{file} doesn't exist![/red]")
        ans = input("Want to create the file? (y/n)\n")

        if ans == 'y':
            data = {"settings":{"skip_intro":False, "debug": False, "language": "en"}, "saves": {}}
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=3)

            rprint(f"[green]File is created![/green]")
            return True
        else:
            rprint("[yellow]Ok, try find it then :)[/yellow]")
            return True
def isDebug(file):
    checkFile(file)

    with open('data.json', 'r') as file:
        data = json.load(file)
    
    if data["settings"]["debug"] == True:
        return True
    else:
        return False

class BottyamonCmd(cmd.Cmd):

    intro = print(r"""    _____                                                                 _____ 
   ( ___ )                                                               ( ___ )
    |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
    |   |  ___           _    _                                           |   | 
    |   | (  _`\        ( )_ ( )_                                         |   | 
    |   | | (_) )   _   | ,_)| ,_) _   _    _ _   ___ ___     _     ___   |   | 
    |   | |  _ <' /'_`\ | |  | |  ( ) ( ) /'_` )/' _ ` _ `\ /'_`\ /' _ `\ |   | 
    |   | | (_) )( (_) )| |_ | |_ | (_) |( (_| || ( ) ( ) |( (_) )| ( ) | |   | 
    |   | (____/'`\___/'`\__)`\__)`\__, |`\__,_)(_) (_) (_)`\___/'(_) (_) |   | 
    |   |                         ( )_| |                                 |   | 
    |   |                         `\___/'                                 |   | 
    |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
   (_____)                                                               (_____)
                                     V1.0 
                              A small story game
    
    Load save: load save (save name)
    Start new game: load new (save name)
    Settings: settings list|(setting) true|false|(else)
    Exit game: quit
                                              """)
    prompt = "> "

    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        self.console = Console()

    def do_load(self, args):
        """load [save]/[new] (save name)
        Loads a save or creates one"""

        if checkFile("data.json"):
            return

        args = args.lower().split()

        if len(args) < 2:
            self.console.print("[red]Bad usage. Try: load save|new (name)[/red]")
            return

        if not args:
            self.console.print("[red]You must give a save name or start a new save with [white]load new (name)[/white][/red]") 
            return
        if args[0] == "new":
            name = args[1]
            
            newWorld = World(name)
            seed = newWorld.genSeed()
            if isDebug("data.json"):
                rprint("[gray]Debug: [/gray]", "[yellow]Seed [/yellow]", seed)
            newWorld.seed = seed
            newWorld.buildWorld(newWorld.seed, 30)

            self.console.print("[green]New game started:[/green]", args[1])
        elif args[0] == "save":
            self.console.print ("[green]Loading save:[/green]", args[1])
        else:
            self.console.print("[red]Bad usage. Try: load save|new (name)[/red]")
    def do_quit(self, args):
        """quit
        Command to quit the game"""

        self.console.print("[yellow]Bye! :)[/yellow]")

        return True
    def do_settings(self, args):

        """settings list|setting (true/false/other)
        A command to list and change settings"""

        if checkFile("data.json"):
            return

        args = args.lower().split()

        if len(args) < 1 or not args:
            self.console.print("[red]Bad usage. Try: settings list|(setting) true|false|(else)[/red]")
            return

        if args[0] != "list" and len(args) < 2:
            self.console.print("[red]Bad usage. Try: settings list|(setting) true|false|(else)[/red]")
            return
        if args[0] == "list":

            table = Table(title="Settings")

            table.add_column("Option", justify="right", style="blue")
            table.add_column("Status", justify="left", style="green")

            with open("data.json", "r") as file:
                data = json.load(file)
            
            for key, item in data["settings"].items():
                table.add_row(str(key), str(item))

            self.console.print(table)
            
        if args[0] != "list":

           with open("data.json", "r") as file: 
            data = json.load(file)

            updated = False
            for key, value in data["settings"].items():
                if args[0] == key:
                    if isinstance(value, bool):
                        bool_map = {"true": True, "false": False}
                        try:
                            new_value = bool_map[args[1].lower()]
                        except KeyError:
                            self.console.print("[red]Only 'true' or 'false'[/red]")
                            return
                        
                        data["settings"][key] = new_value
                        self.console.print(f"[green]{key} -> {new_value}[/green]")
                    else:
                        data["settings"][key] = args[1]
                        self.console.print(f"[green]{key} -> {args[1]}[/green]")
                    updated = True
                    break

            if updated:
                
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=3)
            else:
                self.console.print("[red]Setting not found[/red]")
    def do_debug(self, args):
        """debug (any)
        Command to help debug things"""

        if not isDebug("data.json"):
            self.console.print("[red]You are not in debug mode![/red]")
            return
        
        if len(args) < 1:
            self.console.print("[red]Must give debug option![/red]")
            return
        
        args = args.split()

        if args[0] == "check_seed":
            
            if len(args) < 3:
                self.console.print("[red]Must give seed and length![/red]")
                return
            
            length = int(args[2])
            seed = int(args[1])

            random.seed(seed)
            events = []

            for _ in range(length):
                events.append(random.randint(1, 15))

            self.console.print(events)


if __name__ == '__main__':
    
    BottyamonCmd().cmdloop()