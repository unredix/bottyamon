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

from models import Player, World, Battle, Shop, SafePoint, Bottyamon 

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
    with open("data.json", "r") as file:
        data = json.load(file)
    
    if saveName in data["saves"]:
        return data["saves"][saveName]
    else:
        return False
def save(Bottyamon, Player, World):
    with open("data.json", "r") as file:
        data = json.load(file)

    data["saves"][World.name] = {
        "Bottyamon":{
            "name": Bottyamon.name,
            "breed": Bottyamon.breed,
            "baseAtk": Bottyamon.baseAtk,
            "defense": Bottyamon.defense,
            "hp": Bottyamon.hp,
            "rarity": Bottyamon.rarity,
            "isEvo": Bottyamon.isEvo
        },
        "World":{
            "events": World.events,
            "name": World.name,
            "seed": World.seed,
            "progress": World.progress,
            "length": World.length
        },
        "Player": {
            "lvl": Player.lvl,
            "xp": Player.xp,
            "rebirths": Player.rebirths,
            "deaths": Player.deaths,
            "inventory": Player.inventory,
            "money": Player.money,
            "upgrades": Player.upgrades
        }
    }

    with open("data.json", "w") as file:
        json.dump(data, file, indent=3)

    return True

def typeText(text, style, delay, isEnter=True):
    for i in text:
        rprint(f"[{style}]{i}[/{style}]", end="", flush=True)
        time.sleep(delay)
    
    if isEnter:
        input()
    else:
        rprint()

def storyTeller(text, isEnter=True):
    typeText(f"[Story] {text}", "white", 0.05, isEnter)

def taskTeller(text, isEnter=True):
    typeText(f"[Task] {text}", "yellow", 0, isEnter)

def playerMon(text, isEnter=True):
    typeText(f'[Player] "{text}"', "blue", 0.05, isEnter)

def npcMon(text, npcName, isEnter=True):
    typeText(f'[{npcName}] "{text}"', "cyan", 0.05, isEnter)

def badUsage(text):
    rprint(f"[black on red]{text}[/black on red]")

def clearScreen():
    print("\033c", end="")

def shopShow(shop, playerMoney):
    table = Table(title="Shop", show_lines=True)
    table.add_column("Id", justify="right", style="cyan", no_wrap=True)
    table.add_column("Item", style="magenta")
    table.add_column("Stock", justify="right", style="yellow")
    table.add_column("Price", justify="right", style="green")

    for name, data in shop.items():
        table.add_row(
            str(data["iid"]),
            name,
            str(data["amount"]),
            str(data["price"]),
        )
    rprint(table,f"\n[yellow]Your balance :money_with_wings:: {playerMoney}[/]\n\n[yellow]Help:[/]\nYou can buy items using: [blue bold]buy (id) (amount)[/]\nYou can checkout with [blue bold]buy checkout[/]\nOr you can cancel with: [blue bold]buy cancel[/]")

def playIntro():
    time.sleep(1.5)
    typeText("...", "green", 1, False)
    clearScreen()
    storyTeller("You open your eyes and find an unfamiliar ceiling. You don't remember anything or anyone. As you sit up, you try desperately to remember anything that might give you a clue who you might be.")
    playerMon("It's no use...")
    storyTeller("After some time you decide to go out from your room to look around.")
    playerMon("...")
    storyTeller("The sight of a small tavern's inside welcomed you. As you walk down on the stairs towards the exit the receptionist call after you.")
    npcMon("Hey! I got something for you!", "Receptionist")
    storyTeller("As you walk up to the counter the receptionist hands you a map.")
    npcMon("Here, take a look. Something tells me that you might need this.", "Receptionist")
    playerMon("Thank you...")
    storyTeller("As you look at the map the receptionist gave you, from the side of your eye you catch something. A name you think you're familiar with but don't actually know...")
    playerMon("!!!")
    storyTeller("This is your only chance. You think to yourself.")
    playerMon("How can I get to *there*?")
    npcMon("The thing is... it's really difficult even for seasoned hunters to get to *there*...","Receptionist")
    npcMon("I think I can help.", "???")
    storyTeller("An old man sitting at one of the many tables in the reception, spoke up.")
    npcMon("I just wanted to sell my untrained Bottyamon to someone... I'll give it to you if you promise you tell me your tales when we next meet.", "Old man")
    playerMon("I gladly accept!")

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
        self.isLoaded = False
        self.current_shop = None
        self.current_savePoint = None

    def nextEvent(self, progress):

        currentEvent = self.current_world.events[progress]

        rprint(f"\n[white on green]{progress + 1}. Day[/]\n")

        if currentEvent == 1:
            self.current_shop = Shop()
            self.current_shop.generateShop()
            generatedItems = self.current_shop.shopItems

            storyTeller("As you walk out from a big forest's dark inside, your eyes catch something.")
            playerMon("It's a Shop!")
            storyTeller("You go and get closer to the Shop to see its offerings")

            shopShow(generatedItems, self.player.money)
            return True
        
        if currentEvent == 15:
            self.current_savePoint = SafePoint()
            self.current_savePoint.generateTrader()
            data = self.current_savePoint.traderItem
    
            storyTeller("You notice a busy looking road next to your trail you were following. You decide to check it out.")
            npcMon("Welcome!", "???")
            storyTeller("On the side of the road a guard stood proudly.")
            npcMon("Can I see some identification?", "Guard")
            storyTeller("You hand your id to him.")
            npcMon("It's alright, you might get thru.", "Guard")
            storyTeller("As you walk to the big front gate of the Safe Point a trader approaches you...")
            npcMon("Would you mind trading with me?", "Trader")
            self.console.print("Would you like to see the traders offer? (y/n)")
            choice = input()
            while choice != "y" and choice != "n": 
                badUsage("Only options: y/n")
                choice = input().lower()
            if choice == "y":
                self.console.print(f"[blue][Trader] My offer is:[/] (You give) {data["name"]} --> (You get) {data["price"]} money")

                self.console.print("[yellow]Do you accept this offer? (y/n)[/]")
                choice = input()
                while choice != "y" and choice != "n": 
                    badUsage("Only options: y/n")
                    choice = input().lower()

                if choice == "y":
                    success = self.player.removeItem(data["name"], 1)

                    if success:
                        npcMon("It was pleasure doing business with you!", "Trader")
                        self.console.print(f"[red]-1 {data["name"]}[/]\n+{data['price']} money")
                    else:
                        badUsage("You don't have the necessary item!")
                        npcMon("Too bad.", "Trader")

                elif choice == "n":
                    npcMon("Alright, lets meet again sometime!", "Trader")
                
            elif choice == "n":
                npcMon("Lets meet again sometime.", "Trader")
            
            storyTeller("After you left the trader you go to the Safe Zones big gate.")
            npcMon("Have a nice stay!", "Guard2")
            typeText("...", "green bold", "1", isEnter=False)
            self.bottyamon.hp = 100
            self.console.print(f"[green]{self.bottyamon.name}'s health maxed![/]")

        return False
        
    def mainGame(self):
        while self.current_world.progress < self.current_world.length:
            should_wait = self.nextEvent(self.current_world.progress)
            if not should_wait:
                self.current_world.progress += 1
            else:
                return

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
                    data = loadSave(name)

                    self.bottyamon = Bottyamon(data["Bottyamon"]["breed"], data["Bottyamon"]["name"], data["Bottyamon"]["hp"])
                    self.bottyamon.baseAtk = data["Bottyamon"]["baseAtk"]
                    self.bottyamon.defense = data["Bottyamon"]["defense"]
                    self.bottyamon.isEvo = data["Bottyamon"]["isEvo"]
                    self.bottyamon.rarity = data["Bottyamon"]["rarity"]

                    self.player = Player()
                    self.player.lvl = data["Player"]["lvl"]
                    self.player.xp = data["Player"]["xp"]
                    self.player.rebirths = data["Player"]["rebirths"]
                    self.player.deaths = data["Player"]["deaths"]
                    self.player.inventory = data["Player"]["inventory"]
                    self.player.money = data["Player"]["money"]
                    self.player.upgrades = data["Player"]["upgrades"]

                    self.current_world = World(data["World"]["name"])
                    self.current_world.events = data["World"]["events"]
                    self.current_world.seed = data["World"]["seed"]
                    self.current_world.length = data["World"]["length"]
                    self.current_world.progress = data["World"]["progress"]

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
            self.isLoaded = True
            if data["settings"]["skip_intro"] == True:
                typeText("...", "green", 1, isEnter=False)
                if not isDebugVar:
                    clearScreen()
                self.console.print("\n[black on green]\nIntro Skipped\n[/black on green]\n")
            else:
                playIntro()
            
            npcMon("I haven't gave them a name, please give them one...", "Old man", isEnter=False)
            bottyamonName = ""
            while True:
                taskTeller("Give your Bottyamon a name: ", isEnter=False)
                bottyamonName = input()
                if bottyamonName == "" or bottyamonName == " ":
                    badUsage("You need to give a name to your Bottyamon!")
                    continue
                else:
                    break
            time.sleep(1)
            playerMon(f"I should call you... {bottyamonName}!")
            npcMon("Great name choice! It's better than I've ever given!", "Old man")
            storyTeller("You start thinking about what names the old man could even give to his pets if the name you gave is considered really good...")
            npcMon("Now. This Bottyamon has an affinity to three types. Choose one now and train it good!", "Old man", isEnter=False)
            time.sleep(1)
            taskTeller("Choose from one of these options:", isEnter=False)
            
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
                except (ValueError, TypeError):
                    badUsage("Only numbers allowed!")
                    continue
                if choice > 3 or choice < 1:
                    badUsage("Only numbers 1-3!")
                    continue
                else:
                    break
            
            bottyamonType = got[choice - 1]

            playerMon(f"I'll try to train {bottyamonName} the best I can as a {bottyamonType} type!")
            typeText("...", "green", 1, isEnter=False)

            self.bottyamon = Bottyamon(bottyamonType, bottyamonName, 100)
            self.player = Player()
            self.console.print("[green]A week later[/green]")

            trainedStats = self.bottyamon.train(self.player.rebirths, self.current_world.seed)

            playerMon(f"I finally managed to train you, {bottyamonName}")
            self.console.print(f"The stats your Bottyamon got:\n\n[red]ATK[/red] :crossed_swords: : {trainedStats[0]}\n[blue]DEF[/blue] :shield: : {trainedStats[1]}\n\n:star: The rarity you got: [yellow]{trainedStats[2]}[/yellow]")
            time.sleep(1)
            storyTeller("Now that your Bottyamon is trained, you can go out in the wild and try to reach your destiny.")
            self.console.print("\n[white on green bold]And the game starts![/]\n")

            self.mainGame()
            
        elif args[0] == "save":
            data = loadSave(args[1])

            if not data:
                badUsage("Save doesn't exist! Create it with load new (save name).")
                return
            
            self.bottyamon = Bottyamon(data["Bottyamon"]["breed"], data["Bottyamon"]["name"], data["Bottyamon"]["hp"])
            self.bottyamon.baseAtk = data["Bottyamon"]["baseAtk"]
            self.bottyamon.defense = data["Bottyamon"]["defense"]
            self.bottyamon.isEvo = data["Bottyamon"]["isEvo"]
            self.bottyamon.rarity = data["Bottyamon"]["rarity"]

            self.player = Player()
            self.player.lvl = data["Player"]["lvl"]
            self.player.xp = data["Player"]["xp"]
            self.player.rebirths = data["Player"]["rebirths"]
            self.player.deaths = data["Player"]["deaths"]
            self.player.inventory = data["Player"]["inventory"]
            self.player.money = data["Player"]["money"]
            self.player.upgrades = data["Player"]["upgrades"]

            self.current_world = World(data["World"]["name"])
            self.current_world.events = data["World"]["events"]
            self.current_world.seed = data["World"]["seed"]
            self.current_world.length = data["World"]["length"]
            self.current_world.progress = data["World"]["progress"]


            if isDebug("data.json"):
                self.console.print(f"Loaded save: W: {self.current_world.name} P: {self.player.lvl} B: {self.bottyamon.name}")

            self.console.print ("[green]Loading save:[/green]", args[1])

            self.isLoaded = True

            self.mainGame()
        else:
            badUsage("Bad usage. Try: load save|new (name)")
    def do_quit(self, args):
        """quit
        Command to quit the game"""

        if self.isLoaded:
            self.console.print("Would you like to save your progress? (y/n)")
            choice = input()

            if choice == 'y':
                save(self.bottyamon, self.player, self.current_world)
                self.console.print("[green]Saved.[/]")
            elif choice == 'n':
                self.console.print("[yellow]Your choice.[/]")
            else:
                badUsage("Incorrect response")
                self.console.print('[yellow]Defaulting to "y"[/]')
                save(self.bottyamon, self.player, self.current_world)
                self.console.print("[green]Saved.[/]")
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
            

            rebirth = False
            length = int(args[2])
            seed = int(args[1])
            if len(args) >= 4 and args[3].lower() == "true":
                rebirth = True

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

            rebirthMultiplier = 1
            if rebirth == True:
                rebirthMultiplier = 1.25

            random.seed(seed)

            baseAtk = round(random.randint(5, 15) * rebirthMultiplier)
            defense = round(random.randint(10, 20) * rebirthMultiplier)

            self.console.print(f"Bottyamon atk:{baseAtk}, def: {defense}")

        if args[0] == "play_intro":
            playIntro()

        if args[0] == "gen_shop":
            
            tryShop = Shop()
            tryShop.generateShop()

            self.console.print(f"Generated shop: {tryShop.shopItems}")

            shopShow(tryShop.shopItems)
    def do_buy(self, args):

        args = args.lower().split()

        if self.current_shop == None:
            badUsage("You're not at a shop!")
            return
        
        if len(args) < 1:
            badUsage("Needs argument!")
            return

        if args[0] == "checkout":
            money = self.player.money
            definedItems = self.current_shop.shopItems
            inBasket = self.current_shop.basket
            basketPrice = 0           

            for key, item in inBasket.items():
                basketPrice += int(definedItems[key]["price"]) * int(item)

            if money < basketPrice:
                badUsage("You don't have enough money!")
                self.console.print("[yellow]Your basket has been emptied.[/]")
                taskTeller("Place the items you want to buy once again in the basket!")
                self.current_shop.basket = {}
                return
            
            npcMon("Thank you for your purchase!", "Shopkeeper", isEnter=False)
            
            self.console.print(f"{len(inBasket.keys())} [green]item(s) added to your inventory![/]")
            self.player.money -= basketPrice

            for key, item in inBasket.items():
                self.player.inventory[key] = item
            
            self.console.print(f"[yellow]Your new balance:money_with_wings:: {self.player.money}[/]")
            self.current_shop = None

            storyTeller("After putting your item(s) in your backpack, you go and look for a place to stay for the night.")
            typeText("...", "green bold", 1, isEnter=False)

            self.current_world.progress += 1
            self.mainGame()

            return
        if args[0] == "cancel":

            self.current_shop = None
            playerMon("Bye!")
            npcMon("Have a nice day!", "Shopkeeper")
            storyTeller("After going past the Shop, you go and look for a place to stay for the night.")
            typeText("...", "green bold", 1, isEnter=False)

            self.current_world.progress += 1
            self.mainGame()

            return
        if len(args) < 2:
            badUsage("You have to give an Id and an Amount!")
            return
        
        exists = False
        for item, key in self.current_shop.shopItems.items():
            if str(key["iid"]) == str(args[0]):
                exists = True
                if int(key["amount"]) < int(args[1]):
                    npcMon("Sorry, I don't have that many on stock!", "Shopkeeper", isEnter=False)
                    return

                self.current_shop.basket[item] = args[1]
                self.console.print(f"You added [yellow]{args[1]}[/] [blue]{item}[/] to your basket.")

                break
        
        if not exists:
            badUsage("The Id you provided doesn't exists!")
            return
        
        return
    
    def do_inventory(self, args):
        """inventory
        Command to display your inventory"""

        if not self.isLoaded:
            badUsage("No world is loaded!")
            return

        inv = self.player.inventory

        table = Table(title="Inventory", show_lines=True)
        table.add_column("Name", justify="right", style="cyan", no_wrap=True)
        table.add_column("Amount", style="magenta")

        for key, item in inv.items():
            table.add_row(
                key,
                str(item)
            )

        self.console.print(table)

    

if __name__ == '__main__':
    BottyamonCmd().cmdloop()