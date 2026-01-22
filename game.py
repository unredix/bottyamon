import cmd
import json
import random
import time
from pathlib import Path
from rich.console import Console # type: ignore
from rich.panel import Panel # type: ignore
from rich.table import Table # type: ignore
from rich import print as rprint # type: ignore
from rich.tree import Tree # type: ignore

from models import Player, World, Battle, Bottyamon

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

def createWorld(name, length):
    world = World(name)
    seed = world.genSeed()
    
    if isDebug("data.json"):
        rprint("[gray]Debug: [/gray]", "[yellow]Seed [/yellow]", seed)
    
    world.seed = seed
    world.buildWorld(world.seed, length)

    return world

def checkNewSave(saveName):
    with open("data.json", "r") as file:
        data = json.load(file)

    for save in data["saves"]:
        if saveName == save:
            return False
        
    return True

def loadSave(saveName):
    rprint(saveName)

def typeText(text, style, delay):
    for i in text:
        rprint(f"[{style}]{i}[/{style}]", end="", flush=True)
        time.sleep(delay)
    rprint()

def storyTeller(text):
    typeText(f"[Story] {text}", "white", 0.05)

def taskTeller(text):
    typeText(f"[Task] {text}", "yellow", 0)

def playerMon(text):
    typeText(f'[Player] "{text}"', "blue", 0.05)

def npcMon(text, npcName):
    typeText(f'[{npcName}] "{text}"', "cyan", 0.05)

def badUsage(text):
    rprint(f"[black on red]{text}[/black on red]")

def clearScreen():
    print("\033c", end="")

def playIntro():
    time.sleep(1.5)
    typeText("...", "green", 1)
    clearScreen()
    storyTeller("You open your eyes and find an unfamiliar ceiling. You don't remember anything or anyone. As you sit up, you try desperately to remember anything that might give you a clue who you might be.")
    time.sleep(1)
    playerMon("It's no use...")
    time.sleep(1)
    storyTeller("After some time you decide to go out from your room to look around.")
    time.sleep(1)
    playerMon("...")
    storyTeller("The sight of a small tavern's inside welcomed you. As you walk down on the stairs towards the exit the receptionist call after you.")
    npcMon("Hey! I got something for you!", "Receptionist")
    storyTeller("As you walk up to the counter the receptionist hands you a map.")
    time.sleep(1)
    npcMon("Here, take a look. Something tells me that you might need this.", "Receptionist")
    playerMon("Thank you...")
    time.sleep(1)
    storyTeller("As you look at the map the receptionist gave you, from the side of your eye you catch something. A name you think you're familiar with but don't actually know...")
    playerMon("!!!")
    time.sleep(1)
    storyTeller("This is your only chance. You think to yourself.")
    playerMon("How can I get there?")
    time.sleep(1)
    npcMon("The thing is... it's really difficult even for seasoned hunters to get there...","Receptionist")
    npcMon("I think I can help.", "???")
    time.sleep(1)
    storyTeller("An old man sitting at one of the many tables in the reception, spoke up.")
    npcMon("I just wanted to sell my untrained Bottyamon to someone... I'll give it to you if you promise you tell me your tales when we next meet.", "Old man")
    time.sleep(1)
    playerMon("I gladly accept!")
    time.sleep(5)


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
        self.current_world = None
        self.bottyamon = None
        self.battle = None
        self.player = None

    def do_load(self, args):
        """load save|new (save name)
        Loads a save or creates one"""

        if checkFile("data.json"):
            return

        args = args.lower().split()

        if len(args) < 2:
            badUsage("Bad usage. Try: load save|new (name)")
            return

        if not args:
            badUsage("You must give a save name or start a new save with load new (name)")
            return
        if args[0] == "new":
            name = args[1]
            
            isDebugVar = isDebug("data.json")

            if not checkNewSave(name):
                badUsage("You already have a save named this.")
                print("\nWould you like to load it? (y/n)")
                choice = input().lower()

                if choice == "y":
                    loadSave(name)

                    return
                elif choice == "n":
                    self.console.print("[yellow]Choose a different name then[/yellow]")
                    return
                else:
                    badUsage('Different choice was made! Defaulting to "n"...')
                    return
            self.current_world = createWorld(name, 30)
            
            with open("data.json", "r") as file:
                data = json.load(file)
            
            self.console.print("[green]New game started:[/green]", args[1])
            if data["settings"]["skip_intro"] == True:
                typeText("...", "green", 1)
                if not isDebugVar:
                    clearScreen()
                self.console.print("\n[black on green]\nIntro Skipped\n[/black on green]\n")
            else:
                playIntro()
            
            npcMon("I haven't gave them a name, please give them one...", "Old man")
            bottyamonName = ""
            while True:
                taskTeller("Give your Bottyamon a name: ")
                bottyamonName = input()
                if bottyamonName == "" or bottyamonName == " ":
                    badUsage("You need to give a name to your Bottyamon!")
                    pass
                else:
                    break
            time.sleep(1.5)
            playerMon(f"I should call you... {bottyamonName}!")
            time.sleep(1.5)
            npcMon("Great name choice! It's better than I've ever given!", "Old man")
            time.sleep(1.5)
            storyTeller("You start thinking about what names the old man could even give to his pets if the name you gave is considered really good...")
            time.sleep(1.5)
            npcMon("Now. This Bottyamon has an affinity to three types. Choose one now and train it good!", "Old man")
            time.sleep(1.5)
            taskTeller("Choose from one of these options:")
            
            types = ["Lightning", "Earth", "Water", "Gas", "Darkness", "Shadow", "Stone", "Fire"]
            got = []
            random.seed(self.current_world.seed)
            if isDebugVar:
                self.console.print(f"Debug: [yellow]Seed used for types[/yellow] {self.current_world.seed}")
            while len(got) < 3:
                a = random.choice(types)
                if a in got:
                    pass
                else:
                    got.append(a)
            
            styles = {
                "Lightning": ":zap: Lightning",
                "Earth": ":earth_africa: Earth",
                "Water": ":ocean: Water",
                "Gas": ":warning:  Gas",
                "Darkness": ":new_moon: Darkness",
                "Shadow": " :black_medium_square: Shadow",
                "Stone": ":mountain:  Stone",
                "Fire": ":fire: Fire"
            }
            counter = 1
            for elem in got:
                style = styles.get(elem, "[gray]???[/gray]")
                self.console.print(f"\n{style} [{counter}]\n")
                counter+=1
            counter = 0
            choice = None
            while True:
                try:
                    choice = int(input())
                except ValueError:
                    badUsage("Only numbers allowed!")
                    pass
                if choice > 3 or choice < 1:
                    badUsage("Only numbers 1-3!")
                    pass
                else:
                    break
            
            bottyamonType = got[choice - 1]

            time.sleep(1.5)
            playerMon(f"I'll try to train {bottyamonName} the best I can as a {bottyamonType} type!")

            self.bottyamon = Bottyamon(bottyamonName, bottyamonType)
            self.player = Player()
            self.console.print("[green]A week later[/green]")

            trainedStats = self.bottyamon.train(self.player.rebirths)

            #TODO: Make it use seed 

            playerMon(f"I finally managed to train you, {bottyamonName}")
            self.console.print(f"The stats your Bottyamon got:\n\n[red]ATK[/red] :crossed_swords: : {trainedStats[0]}\n[blue]DEF[/blue] :shield: : {trainedStats[1]}\n\n:star: The rarity you got: [yellow]{trainedStats[2]}[/yellow]")


        elif args[0] == "save":
            self.console.print ("[green]Loading save:[/green]", args[1])
        else:
            badUsage("Bad usage. Try: load save|new (name)")
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
            badUsage("Bad usage. Try: settings list|(setting) true|false|(else)")
            return

        if args[0] != "list" and len(args) < 2:
            badUsage("Bad usage. Try: settings list|(setting) true|false|(else)")
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
                            badUsage("Only 'true' or 'false'")
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
                badUsage("Setting not found")
    def do_debug(self, args):
        """debug (any)
        Command to help debug things"""

        if not isDebug("data.json"):
            badUsage("You are not in debug mode!")
            return
        
        if len(args) < 1:
            badUsage("Must give debug option!")
            return
        
        args = args.split()

        if args[0] == "check_seed":
            
            if len(args) < 3:
                badUsage("Must give seed and length!")
                return
            
            length = int(args[2])
            seed = int(args[1])

            random.seed(seed)
            events = []
            
            shopPity = 0
            safePointPity = 0

            for _ in range(length):
                eventNum = random.randint(1,15)
                
                if shopPity >= 5:
                    events.append(1)
                    shopPity = 0
                    pass
                
                if safePointPity >= 10:
                    events.append(15)
                    safePointPity = 0
                    pass

                if eventNum != 1: shopPity += 1 
                else:
                    if shopPity == 0:
                        eventNum = random.randint(2, 14)
                    shopPity = 0 
                if eventNum != 15: safePointPity += 1
                else: 
                    if safePointPity == 0:
                        eventNum = random.randint(2, 14)
                    safePointPity = 0
                
                events.append(eventNum)
            
            types = ["Lightning", "Earth", "Water", "Gas", "Darkness", "Shadow", "Stone", "Fire"]
            got = []
            random.seed(seed)
            while len(got) < 3:
                a = random.choice(types)
                if a in got:
                    pass
                else:
                    got.append(a)


            self.console.print(f"Events: {events}")
            self.console.print(f"Types: {got}")

        if args[0] == "play_intro":
            playIntro()

if __name__ == '__main__':
    BottyamonCmd().cmdloop()