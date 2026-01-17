import cmd
import json
import os
import random
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from rich.tree import Tree

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
    Settings: settings list|setting (on/off/else)
    Exit game: quit
                                              """)
    prompt = "> "

    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        self.console = Console()


    
    def do_load(self, args):
        """load [save]/[new] (save name)
        Loads a save or creates one"""

        dataFile = Path("./data.json")

        if not dataFile.exists():
            self.console.print("[red]data.json doesn't exist![/red]")
            ans = input("Want to create the file? (y/n)\n")

            if ans == 'y':
                data = {"settings":{"skip_intro":False, "debug": False, "language": "en"}}
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=3)

                self.console.print("[green]data.json file is created![/green]")
            else:
                self.console.print("Ok, try find it then :)")
            return

        args = args.lower().split()

        if len(args) < 2:
            self.console.print("[red]Bad usage. Try: load save|new (name)[/red]")
            return

        if not args:
            self.console.print("[red]You must give a save name or start a new save with [white]load new (name)[/white][/red]") 
            return
        if args[0] == "new":   
            self.console.print("[green]New game started:[/green]", args[1])
        elif args[0] == "save":
            self.console.print ("[green]Loading save:[/green]", args[1])
        else:
            self.console.print("[red]Bad usage. Try: load save|new (name)[/red]")

class Bottyamon:
    def __init__(self, breed, name):
        self.breed = breed
        self.name = name
        self.baseAtk = 0
        self.defense = 0
        self.rarity = "unknown"
        self.isEvo = False
        self.lvl = 0

    def train(rebirths):
        
        rebirthMultiplier = 1
        if rebirths > 0:
            rebirthMultiplier = 1.25

        Bottyamon.baseAtk = round(random.randint(5, 15) * rebirthMultiplier)
        Bottyamon.defense = round(random.randint(10, 20) * rebirthMultiplier)

        # rating < 20 --> C
        # 20 <= rating < 30 --> B
        # rating > 30 --> A  
        # rating >= 35 --> S

        rating = (Bottyamon.baseAtk + Bottyamon.defense)
        rarity = "C"

        if rating >= 20 and rating < 30:
            rarity = "B"
        elif rating >= 30 and rating < 35:
            rarity = "A"
        elif rating >= 35:
            rarity = "S"
        return [Bottyamon.baseAtk, Bottyamon.defense, rarity]

if __name__ == '__main__':
    
    BottyamonCmd().cmdloop()


