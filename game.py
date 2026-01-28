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
            data = {"settings":{"skip_intro":False, "debug": False}, "saves": {}}
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=3)

            rprint(f"[green]File is created![/green]")
            return True
        else:
            rprint("[yellow]OK, try to find it then :)[/yellow]")
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
            "effects": Player.effects
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
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
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
    rprint(table,f"\n[yellow]Your balance: :money_with_wings: {playerMoney}[/]\n\n[yellow]Help:[/]\nYou can buy items using: [blue bold]buy (ID) (amount)[/]\nYou can check out with [blue bold]buy checkout[/]\nOr you can cancel with: [blue bold]buy cancel[/]")

def applyEffect(type, effects):
    if type == "dmg":
        if "Strength Potion (+3)" in effects:
            return 3  
        
        if "Strength Potion (+5)" in effects:
            return 5

        return 0
    if type == "def":
        if "Defense Potion (+5)" in effects:
            return 5
        if "Defense Potion (+8)" in effects:
            return 8

        return 0
    if type == "hp":
        if "HP Potion (+25)" in effects:
            return 25
        if "HP Potion (+50)" in effects:
            return 50

        return 0
def fight(bottyamon, player, enemyHp, enemy, NumOfRound=1, overallDmg = 0):
        strengths = {
            "Fire":      ["Earth", "Gas"],
            "Water":     ["Fire", "Stone"],
            "Stone":     ["Shadow", "Earth"],
            "Shadow":    ["Fire"],
            "Lightning": ["Water", "Shadow"],
            "Gas":       ["Lightning"],
            "Earth":     ["Water", "Lightning"],
            "Darkness":  ["Fire", "Water", "Stone", "Earth", "Lightning", "Gas", "Shadow"]
        }

        weaknesses = {
            "Fire":      ["Water", "Shadow"],
            "Water":     ["Lightning", "Earth"],
            "Stone":     ["Water"],
            "Shadow":    ["Stone", "Lightning"],
            "Lightning": ["Earth", "Gas"],
            "Gas":       ["Fire"],
            "Earth":     ["Fire", "Stone"],
            "Darkness": []
        }

        enemyDef = random.randint(1,10)

        playerTypeEffect = 1
        enemyTypeEffect = 1

        if enemy[1] in weaknesses[bottyamon.breed]:
            playerTypeEffect = 1.5
        if enemy[1] in strengths[bottyamon.breed]:
            enemyTypeEffect = 1.5

        time.sleep(1)
        rprint(f"[black on white]Round: {NumOfRound}[/]")
        time.sleep(1)
        rprint(f"[yellow]{bottyamon.name}[/] attacks!")
        time.sleep(3)
        finalAttack = (bottyamon.baseAtk + applyEffect("dmg", player.effects)) * playerTypeEffect
        trueDmg = max(1, int(finalAttack - enemyDef))

        overallDmg += trueDmg

        rprint(f"[green bold]You did :crossed_swords: :[yellow] {trueDmg}[/] dmg![/]")
        time.sleep(1)
        if trueDmg >= enemyHp:
            rprint(f"\nResults:\n[green bold]You defeated: {enemy[0]}![/]\n[blue bold]Overall dmg: {overallDmg}[/]\n[red bold]Remaining hp: {bottyamon.hp}[/]")
            return [True, overallDmg]
        enemyHp -= trueDmg
        rprint(f"Remaining health of enemy: {enemyHp}")

        time.sleep(1)
        rprint("[yellow]Will you try to dodge? (50% success) (y/n)[/]")
        choice = input().lower()
        while choice != "y" and choice != "n":
            badUsage("Only y/n options!")
            choice = input().lower()

        success = random.choice([True, False])

        finalAttack = (random.randint(5, 10) * enemyTypeEffect) * round(random.uniform(1, 1.5), 2) 
        trueDmg = int(finalAttack - bottyamon.defense - applyEffect("def", player.effects))

        rprint(f"[yellow]{enemy[0]}[/] attacks!")

        if choice == "y" and not success:
            rprint("[red]Your dodge attempt failed! The dmg got x1.35![/]")
            trueDmg = trueDmg * 1.35
        
        if choice == "y" and success:
            rprint(f"[green bold]You dodged a {trueDmg} dmg attack![/]")

        else:
            rprint(f"[yellow bold]{enemy[0]} did {trueDmg} dmg to you![/]")
            time.sleep(1)
            if trueDmg >= bottyamon.hp:
                
                rprint(f"\nResults:\n[red bold]You lost![/]\n[blue bold]Overall dmg: {overallDmg}[/]\n[red bold]Enemy HP: {enemyHp}[/]")
                return [False, overallDmg, enemyHp]
            bottyamon.hp -= trueDmg
            rprint(f"Your health: [red]{bottyamon.hp}[/]")

        return fight(bottyamon, player, enemyHp, enemy, NumOfRound + 1, overallDmg)
        
def playIntro():
    time.sleep(1.5)
    typeText("...", "green", 1, False)
    clearScreen()
    storyTeller("You open your eyes and see an unfamiliar ceiling. You don't remember anything or anyone. As you sit up, you try desperately to remember anything that might give you a clue about who you might be.")
    playerMon("It's no use...")
    storyTeller("After some time, you decide to go out of your room and look around.")
    playerMon("...")
    storyTeller("The sight of a small tavern's interior welcomed you. As you walk down the stairs toward the exit, the receptionist calls after you.")
    npcMon("Hey! I got something for you!", "Receptionist")
    storyTeller("As you walk up to the counter, the receptionist hands you a map.")
    npcMon("Here, take a look. Something tells me that you might need this.", "Receptionist")
    playerMon("Thank you...")
    storyTeller("As you look at the map the receptionist gave you, out of the corner of your eye you catch something. A name you think you're familiar with but don't actually know...")
    playerMon("!!!")
    storyTeller("This is your only chance, you think to yourself.")
    playerMon("How can I get to *there*?")
    npcMon("The thing is... it's really difficult even for seasoned hunters to get to *there*...","Receptionist")
    npcMon("I think I can help.", "???")
    storyTeller("An old man sitting at one of the many tables in the tavern spoke up.")
    npcMon("I just wanted to sell my untrained Bottyamon to someone... I'll give it to you if you promise to tell me your tales when we next meet.", "Old man")
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
    Next day: next
    Exit game: quit
                  
    Use the "help" command to learn about other commands.""")
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
        self.current_battle = None
        self.waiting_for_next = True

    def nextEvent(self, progress):

        currentEvent = self.current_world.events[progress]

        rprint(f"\n[white on green]{progress + 1}. Day[/]\n")

        if currentEvent == 1:
            self.current_shop = Shop()
            self.current_shop.generateShop()
            generatedItems = self.current_shop.shopItems

            storyTeller("As you walk out of the dark interior of the forest, your eyes catch something.")
            playerMon("It's a Shop!")
            storyTeller("You go and get closer to the Shop to see its offerings.")

            shopShow(generatedItems, self.player.money)
            return True
        
        if currentEvent == 15:
            self.current_savePoint = SafePoint()
            self.current_savePoint.generateTrader()
            data = self.current_savePoint.traderItem
    
            storyTeller("You notice a busy-looking road next to the trail you were following. You decide to check it out.")
            npcMon("Welcome!", "???")
            storyTeller("On the side of the road a guard stood proudly.")
            npcMon("Can I see some identification?", "Guard")
            storyTeller("You hand your ID to him.")
            npcMon("It's all right, you might get through.", "Guard")
            storyTeller("As you walk to the big front gate of the Safe Point, a trader approaches you...")
            npcMon("Would you mind trading with me?", "Trader")
            self.console.print("Would you like to see the trader's offer? (y/n)")
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
                        npcMon("It was a pleasure doing business with you!", "Trader")
                        self.console.print(f"[red]- 1 {data["name"]}[/]\n[green]+ {data['price']} money[/]")
                    else:
                        badUsage("You don't have the necessary item!")
                        npcMon("Too bad.", "Trader")

                elif choice == "n":
                    npcMon("All right, let's meet again sometime!", "Trader")
                
            elif choice == "n":
                npcMon("Let's meet again sometime.", "Trader")
            
            storyTeller("After you leave the trader, you go to the Safe Zone's main gate.")
            npcMon("Have a nice stay!", "Guard 2")
            typeText("...", "green bold", 1, isEnter=False)
            self.bottyamon.hp = 100
            self.console.print(f"[green]{self.bottyamon.name}'s health maxed![/]")

            self.current_savePoint = None

            return False
        
        if currentEvent in [2,3,4,5]:
            self.current_battle = Battle(self.player, self.bottyamon)
            self.current_battle.genEnemy()
            enemy = self.current_battle.enemy

            meetType = random.randint(1,3)

            if meetType == 1:
                storyTeller("As you wander in the woods of the great forest, which you decided to go through as a shortcut, something large is coming toward you.")
                playerMon("!!!")
                storyTeller(f"It's a {enemy[0]}!")

            if meetType == 2:
                storyTeller("You're climbing a mountain in order to get to its other side, but your feet slip on one of the small rocks. As you try to regain consciousness, you see something strange before your eyes.")
                playerMon("!!!")
                storyTeller(f"It's a {enemy[0]}!")
            
            if meetType == 3:
                storyTeller("When you wake up you usually look around really carefully before continuing your journey. This time it really came in handy as you did your morning routine.")
                playerMon("!!!")
                storyTeller("At a nearby tree you see something...")
                playerMon(f"A {enemy[0]}!")
            
            self.console.print("\n[black on yellow bold]BATTLE TIME![/]\n")
            enemyHp = random.randint(30,60)
            self.console.print(f"[gray]The enemy:\n[/][yellow]Type: {enemy[1]}[/]\n[red]Health: {enemyHp}[/]\n")
            self.console.print(f"[gray]You:\n[/][yellow]Type: {self.bottyamon.breed}[/]\n[red]Health: {self.bottyamon.hp}[/]\n")

            self.console.print("\n[cyan]Would you like to use a potion before the battle? (y/n)[/]")
            choice = input().lower()
            while choice != "y" and choice != "n":
                badUsage("Only y/n options!")
                choice = input().lower()
            
            if choice == "y":
                available_potions = []
                potion_list = [
                    "Strength Potion (+3)",
                    "Strength Potion (+5)",
                    "Defense Potion (+5)",
                    "Defense Potion (+8)",
                    "HP Potion (+25)",
                    "HP Potion (+50)"
                ]
                
                for potion in potion_list:
                    if potion in self.player.inventory:
                        available_potions.append(potion)
                
                if not available_potions:
                    self.console.print("[red]You don't have any potions![/]")
                else:
                    self.console.print("\n[yellow]Available potions:[/]")
                    for idx, potion in enumerate(available_potions, 1):
                        self.console.print(f"[cyan]{idx}.[/] {potion} (x{self.player.inventory[potion]})")
                    
                    self.console.print("[cyan]0.[/] Cancel")
                    
                    while True:
                        try:
                            potion_choice = int(input("\nSelect a potion number: "))
                            if potion_choice == 0:
                                self.console.print("[yellow]Cancelled.[/]")
                                break
                            elif potion_choice > 0 and potion_choice <= len(available_potions):
                                selected_potion = available_potions[potion_choice - 1]
                                
                                success = self.player.removeItem(selected_potion, 1)
                                if success:
                                    self.player.effects.append(selected_potion)
                                    self.console.print(f"[green]Used {selected_potion}![/]")
                                    
                                    if "HP Potion" in selected_potion:
                                        hp_boost = applyEffect("hp", [selected_potion])
                                        self.bottyamon.hp = min(100, self.bottyamon.hp + hp_boost)
                                        self.console.print(f"[green]HP restored! Current HP: {self.bottyamon.hp}[/]")
                                break
                            else:
                                badUsage(f"Please enter a number between 0 and {len(available_potions)}")
                        except (ValueError, TypeError):
                            badUsage("Please enter a valid number!")
            
            self.console.print()

            results = fight(self.bottyamon, self.player, enemyHp, enemy)

            if results[0] == True:
                rewards = [round((results[1] * 0.25)), results[1]]
                self.console.print(f"\nRewards:\n:money_with_wings: {rewards[0]}\nxp {rewards[1]}\n")
                didLvlUp = self.player.addXp(rewards[1])
                self.player.addMoney(rewards[0])

                if didLvlUp:
                    self.console.print(f"[green bold]Lvl up! You're now lvl {self.player.lvl}![/]")

                    lvluprewards = {5: "Evolve chance", 10 : "Strength Potion (+3)", 15: "Retrain pill", 20: "Evolve chance"}
                    reward = lvluprewards[self.player.lvl]

                    if reward:
                        if reward != "Evolve chance":
                            self.console.print(f"[green]Reward: {reward}[/]")
                            self.console.print(f"+ 1 {reward}")
                            self.player.addItem(reward, 1)
                        else:
                            self.console.print("[yellow bold]:star: Your Bottyamon is evolving![/]")
                            time.sleep(2)
                            self.console.print("[green]Your Bottyamon successfully evolved![/]")
                            self.bottyamon.isEvo = True
                
            if results[0] == False:
                self.console.print(f"\nYou lost:\n:money_with_wings: -50%")
                self.player.money *= 0.5

        if currentEvent in [6, 7]:
            storyTeller("You woke up at night after a long day of walking in a big wheat farm as you heard a shout from the distance.")
            playerMon("Might as well check it out...")

            self.console.print("[yellow]Will you use a flashlight? (y/n)[/]")
            usedItem = False

            choice = input()
            while choice != "y" and choice != "n": 
                badUsage("Only options: y/n")
                choice = input().lower()

            if choice == "y":
                success = self.player.removeItem("Flashlight", 1)

                if not success:
                    badUsage("You don't have a Flashlight!")

                else:
                    self.console.print("[red]- 1 Flashlight[/]")
                    usedItem = True
            
            storyTeller("As you try to go towards the source of the sound, you see something in the dark.")
            playerMon("What's that?")
            if usedItem:
                storyTeller("When you point your flashlight at that something it starts to move.")
                playerMon("It's a monster!")
                storyTeller("You throw the flashlight in a bush as you start to run back to your camp. The monster doesn't seem to follow you...")
            else:
                storyTeller("When you try to get closer to the thing in the dark to get a better look at it, it moved.")
                playerMon("!!!")
                storyTeller("You start running as fast as you can but that something is running after you.")
                playerMon("Get away from me!")
                doHit = random.choice([True, False])

                if doHit:
                    storyTeller("The something got closer and closer until it reached your leg. With its sharp teeth it bit you.")
                    playerMon("Agh!")
                    self.console.print("[red]- 10 hp [/]")
                    
                    if self.bottyamon.hp - 10 <= 0:
                        self.console.print("\n[red bold] You died! [/]\nPenalty: -20 :money_with_wings:\n")
                    else:
                        self.bottyamon.hp -= 10
                
                else:
                    storyTeller("With a kick backwards you manage to hit it. The something don't follow you anymore.")
                    playerMon("What was that...")

        if currentEvent in [8,9]:
            storyTeller("Next to a cliff side you hear something...")
            npcMon("Help me!", "???")
            npcMon("Someone help me please!", "???")

            storyTeller("You look down and see a middle-aged man shouting up from a small edge of the hill.")
            playerMon("Hey! I think I can help you!")

            self.console.print("[yellow]Will you use a Rope? (y/n)[/]")
            usedItem = False

            choice = input()
            while choice != "y" and choice != "n": 
                badUsage("Only options: y/n")
                choice = input().lower()

            if choice == "y":
                success = self.player.removeItem("Rope", 1)

                if not success:
                    badUsage("You don't have a Rope!")

                else:
                    self.console.print("[red]- 1 Rope[/]")
                    usedItem = True
            
            if usedItem:
                storyTeller("You get your rope out of your backpack and you start to lower it for him.")
                playerMon("Grab it!")
                npcMon("I'll try!", "Man")
                storyTeller("The stranger grabbed the rope and you pulled him up.")
                npcMon("Thank you very much!", "Man")
                self.console.print("[green]As a reward for your efforts you get 20 :money_with_wings:.[/]")
                self.player.addMoney(20)
            else:
                storyTeller("You get on your stomach and offer your hand to him.")
                playerMon("Here! Try grabbing it!")
                isFail = random.choice([True, False])
                if isFail:
                    storyTeller("As you try to pull him up, your hand slips...")
                    playerMon("!!!")
                    storyTeller("The stranger you met just a minute ago has fallen into the darkness of the hillside...")
                
                else:
                    storyTeller("You start to pull him up!")
                    playerMon("Almost there!")
                    storyTeller("You successfully pulled the stranger up!")
                    npcMon("Thank you very much for your help!", "Man")
                    self.console.print("[green]As a reward for your help, the man gave you 10 :money_with_wings:!")
                    self.player.addMoney(10)

        if currentEvent in [10, 11]:
            storyTeller("You're going through a small village when you come across a crowd forming at one of the shops.")
            playerMon("What happened?")
            npcMon("The fish bowl the shopkeeper uses to store live fish has a crack in it, and they're trying to figure out what to do.", "Bystander")
            playerMon("I think I can help!")
            storyTeller("You go directly to the shopkeeper and ask if you can help figure out the problem.")
            playerMon("Hello! I think I have a solution!")
            npcMon("Really, son? Then out with it!", "Shopkeeper")
            
            self.console.print("[yellow]Will you use Duck Tape? (y/n)[/]")
            usedItem = False

            choice = input()
            while choice != "y" and choice != "n": 
                badUsage("Only options: y/n")
                choice = input().lower()

            if choice == "y":
                success = self.player.removeItem("Duck tape", 1)

                if not success:
                    badUsage("You don't have Duck Tape!")

                else:
                    self.console.print("[red]- 1 Duck Tape[/]")
                    usedItem = True
            
            if usedItem:
                storyTeller("The shopkeeper's eyes widened as you pulled a piece of duck tape from your backpack...")
                npcMon("AND WHAT WOULD THAT DO!?", "Shopkeeper")
                playerMon("Now, now... Just look and see the magic!")
                storyTeller("You placed the Duck Tape on the leaking bowl.")
                npcMon("!!!", "Shopkeeper")
                storyTeller("The leak stopped in an instant.")
                playerMon("I told you!")
                self.console.print("[green]As a reward for your help the Shopkeeper gave you 15 :money_with_wings:![/]")
                self.player.addMoney(15)
            else:
                storyTeller("You look at the bowl carefully and start thinking about a solution.")
                playerMon("Hmm... Maybe I can seal it with something from nature...")
                storyTeller("You go outside and find some tree resin on a nearby tree. You apply it carefully to the crack.")
                npcMon("I don't really trust you with this one...", "Shopkeeper")
                playerMon("Let's just see...")
                isSuccess = random.choice([True, False])
                
                if isSuccess:
                    storyTeller("To everyone's amazement, the resin hardens and the leak stops completely!")
                    npcMon("You're a genius! Thank you!", "Shopkeeper")
                    self.console.print("[green]As a reward for your creative solution, the Shopkeeper gave you 10 :money_with_wings:![/]")
                    self.player.addMoney(10)
                else:
                    storyTeller("The resin doesn't hold and the bowl continues to leak...")
                    playerMon("Oh no...")
                    npcMon('YEAH, "OH NO"!', "Shopkeeper")
                    storyTeller("The shopkeeper chased you away with a fish...")

        if currentEvent == 12:
            storyTeller("You encounter a massive stone wall blocking a mountain pass.")
            playerMon("There must be a way through...")
            storyTeller("You notice the wall appears to have weak points that could be broken.")
            
            self.console.print("[yellow]Will you use a Pickaxe to break through? (y/n)[/]")
            usedItem = False

            choice = input()
            while choice != "y" and choice != "n": 
                badUsage("Only options: y/n")
                choice = input().lower()

            if choice == "y":
                success = self.player.removeItem("Pickaxe", 1)

                if not success:
                    badUsage("You don't have a Pickaxe!")

                else:
                    self.console.print("[red]- 1 Pickaxe[/]")
                    usedItem = True
            
            if usedItem:
                storyTeller("You swing the Pickaxe with all your power against the weak point!")
                playerMon("Break already!")
                storyTeller("Rocks crumble and fall, creating an opening in the wall.")
                playerMon("Yes! I made it through!")
                self.console.print("[green]You broke through the wall! +25 :money_with_wings:[/]")
                self.player.addMoney(25)
            else:
                storyTeller("You search for another way around the wall.")
                playerMon("There has to be a way...")
                storyTeller("After careful exploration, you find a narrow path along the side of the mountain.")
                isFound = random.choice([True, False])
                
                if isFound:
                    storyTeller("The path is treacherous but passable. You carefully make your way across.")
                    playerMon("Got it!")
                    self.console.print("[green]You found an alternate route! +15 :money_with_wings:[/]")
                    self.player.addMoney(15)
                else:
                    storyTeller("The path is too dangerous and unstable. You have to find another route.")
                    playerMon("...")
                    storyTeller("You spend extra time finding your way around.")

        if currentEvent == 13:
            storyTeller("You come across a dense forest with overgrown vegetation blocking your path.")
            playerMon("This is getting in my way...")
            storyTeller("The vines and branches are too thick to push through easily.")
            
            self.console.print("[yellow]Will you use an Axe to clear the path? (y/n)[/]")
            usedItem = False

            choice = input()
            while choice != "y" and choice != "n": 
                badUsage("Only options: y/n")
                choice = input().lower()

            if choice == "y":
                success = self.player.removeItem("Axe", 1)

                if not success:
                    badUsage("You don't have an Axe!")

                else:
                    self.console.print("[red]- 1 Axe[/]")
                    usedItem = True
            
            if usedItem:
                storyTeller("You swing the Axe efficiently, cutting through the dense vegetation.")
                playerMon("Why is it so dense?")
                storyTeller("You carve a clear path through the forest, and in doing so, discover a hidden area.")
                playerMon("And what is this?")
                storyTeller("You open the chest.")
                
                self.console.print("[green]The chest had 20 :money_with_wings:![/]")
                self.player.addMoney(20)
            else:
                storyTeller("You carefully squeeze through the dense vegetation without cutting it.")
                playerMon("Slowly... slowly...")
                storyTeller("It's a tight squeeze, but you manage to navigate through the overgrown forest.")
                isMade = random.choice([True, False])
                
                if isMade:
                    storyTeller("You finally emerge on the other side, exhausted but unharmed.")
                    playerMon("Made it!")
                else:
                    storyTeller("The vegetation becomes increasingly entangled, and you get stuck.")
                    playerMon("I'm stuck!")
                    storyTeller("After struggling for a while, you manage to break free and find another way around the forest.")
                    playerMon("Finally... free...")

        if currentEvent == 14:
            storyTeller("You discover an abandoned mine with glimmering ore in the walls.")
            playerMon("Is that... valuable ore?")
            storyTeller("The ore looks precious, but it's embedded deep within the rock walls.")
            
            self.console.print("[yellow]Will you use a Pickaxe to mine the ore? (y/n)[/]")
            usedItem = False

            choice = input()
            while choice != "y" and choice != "n": 
                badUsage("Only options: y/n")
                choice = input().lower()

            if choice == "y":
                success = self.player.removeItem("Pickaxe", 1)

                if not success:
                    badUsage("You don't have a Pickaxe!")

                else:
                    self.console.print("[red]- 1 Pickaxe[/]")
                    usedItem = True
            
            if usedItem:
                storyTeller("You carefully mine the ore using the Pickaxe.")
                playerMon("Just don't break on me...")
                storyTeller("You successfully harvest some chunks of valuable ore!")
                playerMon("This is great!")
                self.console.print("[green]You mined a precious ore! +30 :money_with_wings:[/]")
                self.player.addMoney(30)
            else:
                storyTeller("You attempt to extract the ore using a nearby stone.")
                playerMon("Hope it works...")
                storyTeller("You strike the ore repeatedly with a rock.")
                isMined = random.choice([True, False])
                
                if isMined:
                    storyTeller("Some ore chunks break free from the wall!")
                    playerMon("At least something!")
                    self.console.print("[green]You gathered some ore! +15 :money_with_wings:[/]")
                    self.player.addMoney(15)
                else:
                    storyTeller("The ore is too hard to mine this way. Most of your strikes are wasted.")
                    playerMon("This isn't working...")
                    storyTeller("You eventually give up and move on, disappointed.")
        return False
        
    def mainGame(self):
        self.waiting_for_next = False
        self.isLoaded = True
        while self.current_world.progress < self.current_world.length:
            should_wait = self.nextEvent(self.current_world.progress)
            if not should_wait:
                self.current_world.progress += 1
                self.waiting_for_next = True
                self.console.print("\n[cyan bold]Type 'next' to continue, until then you can use any other command![/]\n")
                return
            else:
                return
            
        self.console.print("\n[white on green]Final[/]\n")
        storyTeller("You look at the local map of the nearby towns and cities.")
        playerMon("So I'm finally here...")
        storyTeller("After a quick chat with the local guards, you go through the big brown door that leads to your final destination.")
        playerMon("Woah!")
        storyTeller("A big, lively city's main square welcomed you. After a brief stop, you start walking again.")
        npcMon("Hey Mister! Would you like some apples?", "???")
        storyTeller("A man who sells apples called you over.")
        playerMon("Yes, why not.")
        if self.player.money - 5 < 0:
                    npcMon("This one is on the house, since you're new here!", "Apple seller")
        else:
            self.player.money -= 5
            self.console.print("[red] - 5 :money_with_wings:")
            npcMon("Thank you!", "Apple seller")

        storyTeller("When you took a bite from the apple...")
        typeText("...", "red", 1, isEnter=False)
        self.console.print("[black on white bold]\n\nDarkness...[/]\n\n")
        time.sleep(5)

        self.console.print("\n[green bold]Thank you very much for playing the game![/]\n")
        time.sleep(2)

        typeText("Would you like to be reborn? (y/n)", "gold bold", 0.1, isEnter=False)

        choice = input()
        while choice != "y" and choice != "n": 
            badUsage("Only options: y/n")
            choice = input().lower()

        if choice == "y":
            saveName = self.current_world.name
            rebirthCount = self.player.rebirths + 1
            
            with open("data.json", "r") as file:
                data = json.load(file)
            
            if saveName in data["saves"]:
                del data["saves"][saveName]
            
            with open("data.json", "w") as file:
                json.dump(data, file, indent=3)
            
            self.console.print("[yellow]Your old save has been cleared...[/]")
            time.sleep(1)
            
            self.current_world = None
            self.bottyamon = None
            self.battle = None
            self.player = None
            self.isLoaded = False
            self.current_shop = None
            self.current_savePoint = None
            self.current_battle = None
            self.waiting_for_next = True
            
            self.console.print("[green]Starting a new adventure...[/]")
            typeText("...", "green", 1, isEnter=False)
            clearScreen()
            
            self.current_world = createWorld(saveName, 20)
            self.player = Player()
            self.player.rebirths = rebirthCount
            self.isLoaded = True
            
            self.console.print(f"[cyan]Rebirth #{rebirthCount}[/]")
            time.sleep(1)
            
            self.mainGame()
        else:
            self.console.print("\n[yellow bold]I hope you had fun! :DD[/]\n")
            time.sleep(5)
            self.isLoaded = False
            return False

    def do_load(self, args):
        """load save|saves|new (save name)
        Loads a save, lists them or creates one"""

        if checkFile("data.json"):
            return

        args = args.lower().split()

        if len(args) < 1:
            badUsage("Bad usage. Try: load save|saves|new (name)")
            return

        if not args:
            badUsage("You must give a save name or start a new save with load new (name)")
            return
        if args[0] == "new":
            
            if len(args) < 2:
                badUsage("You have to give a name!")
                return
            
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
                    self.player.effects = data["Player"]["effects"]

                    self.current_world = World(data["World"]["name"])
                    self.current_world.events = data["World"]["events"]
                    self.current_world.seed = data["World"]["seed"]
                    self.current_world.length = data["World"]["length"]
                    self.current_world.progress = data["World"]["progress"]

                    self.mainGame()
                    return
                elif choice == "n":
                    self.console.print("[yellow]Choose a different name then[/yellow]")
                    return
                else:
                    badUsage('Different choice was made! Defaulting to "n"...')
                    return
            self.current_world = createWorld(name, 15)
            
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
            
            npcMon("I didn't give it a name, so please give it one...", "Old man", isEnter=False)
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
            npcMon("Great name choice! It's better than any I've ever given!", "Old man")
            storyTeller("You start thinking about what names the old man could give his pets if the name you gave is considered really good...")
            npcMon("Now, this Bottyamon has an affinity for three types. Choose one now and train it well!", "Old man", isEnter=False)
            time.sleep(1)
            taskTeller("Choose one of these options:", isEnter=False)
            
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
            storyTeller("Now that your Bottyamon is trained, you can go out into the wild and try to reach your destiny.")
            self.console.print("\n[white on green bold]And the game starts![/]\n")

            self.mainGame()
            
        elif args[0] == "save":
            
            if len(args) < 2:
                badUsage("You have to name a save!")
                return
            
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
            self.player.effects = data["Player"]["effects"]

            self.current_world = World(data["World"]["name"])
            self.current_world.events = data["World"]["events"]
            self.current_world.seed = data["World"]["seed"]
            self.current_world.length = data["World"]["length"]
            self.current_world.progress = data["World"]["progress"]


            if isDebug("data.json"):
                self.console.print(f"Loaded save: W: {self.current_world.name} P: {self.player.lvl} B: {self.bottyamon.name}")

            self.console.print ("[green]Loading save:[/green]", args[1])
            typeText("...", "green", 1, isEnter=False)
            
            clearScreen()
            self.isLoaded = True

            self.mainGame()

        elif args[0] == "saves":
            
            with open("data.json", "r") as file:
                data = json.load(file)        
            table = Table(title="Saves")

            table.add_column("Save")
            table.add_column("Days")

            for key, item in data["saves"].items():
                table.add_row(key, str(item["World"]["progress"]))

            rprint(table)

        else:
            badUsage("Bad usage. Try: load save|saves|new (name)")
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
            
            self.console.print("[yellow]Returning to starter screen...[/]")
            self.current_world = None
            self.bottyamon = None
            self.battle = None
            self.player = None
            self.isLoaded = False
            self.current_shop = None
            self.current_savePoint = None
            self.current_battle = None
            self.waiting_for_next = True
            clearScreen()
            print(r"""    _____                                                                 _____ 
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
    Next day: next
    Exit game: quit
                  
    Use the "help" command to learn about other commands.""")
            return False
        else:
            self.console.print("[yellow]Bye! :)[/yellow]")
            return True
    
    def do_save(self, args):
        """save
        Command to save your progress"""

        if not self.isLoaded:
            badUsage("No world is loaded!")
            return
        
        save(self.bottyamon, self.player, self.current_world)
        self.console.print("[green]Game saved successfully![/]")

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
        """buy (ID) (amount)
        Command to put items in your basket"""
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
                self.player.inventory[key] = int(item)
            
            self.console.print(f"[yellow]Your new balance: :money_with_wings: {self.player.money}[/]")
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
            badUsage("You have to give an ID and an amount!")
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
            badUsage("The ID you provided doesn't exist!")
            return
        
        return
    
    def do_next(self, args):
        """next
        Command to continue to the next event"""

        if not self.isLoaded:
            badUsage("No world is loaded!")
            return
        
        if not self.waiting_for_next:
            badUsage("Not waiting for next command!")
            return
        
        self.waiting_for_next = False
        self.mainGame()
    
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

    def do_stats(self, args):
        """stats
        Command to display all your stats"""

        if not self.isLoaded:
            badUsage("No world is loaded!")
            return

        player_table = Table(title="Player Stats", show_lines=True)
        player_table.add_column("Stat", style="cyan", no_wrap=True)
        player_table.add_column("Value", style="yellow")

        player_table.add_row("Level", str(self.player.lvl))
        player_table.add_row("XP", f"{self.player.xp}/100")
        player_table.add_row("Money :money_with_wings:", str(self.player.money))
        player_table.add_row("Rebirths", str(self.player.rebirths))
        player_table.add_row("Deaths", str(self.player.deaths))
        
        effects_display = ", ".join(self.player.effects) if self.player.effects else "None"
        player_table.add_row("Active Effects", effects_display)

        self.console.print(player_table)
        self.console.print()

        bottyamon_table = Table(title=f"{self.bottyamon.name}'s Stats", show_lines=True)
        bottyamon_table.add_column("Stat", style="cyan", no_wrap=True)
        bottyamon_table.add_column("Value", style="yellow")

        bottyamon_table.add_row("Name", self.bottyamon.name)
        bottyamon_table.add_row("Type", self.bottyamon.breed)
        bottyamon_table.add_row("HP :heart:", str(self.bottyamon.hp))
        bottyamon_table.add_row("Attack :crossed_swords:", str(self.bottyamon.baseAtk))
        bottyamon_table.add_row("Defense :shield:", str(self.bottyamon.defense))
        bottyamon_table.add_row("Rarity :star:", self.bottyamon.rarity)
        bottyamon_table.add_row("Evolved", "Yes" if self.bottyamon.isEvo else "No")

        self.console.print(bottyamon_table)
        self.console.print()

        world_table = Table(title="Journey Progress", show_lines=True)
        world_table.add_column("Stat", style="cyan", no_wrap=True)
        world_table.add_column("Value", style="yellow")

        world_table.add_row("World Name", self.current_world.name)
        world_table.add_row("Current Day", str(self.current_world.progress + 1))
        world_table.add_row("Total Days", str(self.current_world.length))
        progress_percent = round((self.current_world.progress / self.current_world.length) * 100, 1)
        world_table.add_row("Progress", f"{progress_percent}%")
        world_table.add_row("Seed", str(self.current_world.seed))

        self.console.print(world_table)

    def do_retrain(self, args):
        """retrain
        Command to retrain your Bottyamon using a Retrain pill"""

        if not self.isLoaded:
            badUsage("No world is loaded!")
            return

        if "Retrain pill" not in self.player.inventory or self.player.inventory["Retrain pill"] < 1:
            badUsage("You don't have a Retrain pill!")
            return

        self.console.print(f"[yellow]Current stats of {self.bottyamon.name}:[/]")
        self.console.print(f"[red]ATK[/red] :crossed_swords: : {self.bottyamon.baseAtk}")
        self.console.print(f"[blue]DEF[/blue] :shield: : {self.bottyamon.defense}")
        self.console.print(f":star: Rarity: [yellow]{self.bottyamon.rarity}[/yellow]\n")

        self.console.print("[yellow]Are you sure you want to use a Retrain pill? Your Bottyamon will get new random stats. (y/n)[/]")
        choice = input().lower()
        
        while choice != "y" and choice != "n":
            badUsage("Only options: y/n")
            choice = input().lower()

        if choice == "n":
            self.console.print("[yellow]Retrain cancelled.[/]")
            return

        success = self.player.removeItem("Retrain pill", 1)
        
        if not success:
            badUsage("Failed to use Retrain pill!")
            return

        self.console.print("[green]Using Retrain pill...[/]")
        typeText("...", "green", 1, isEnter=False)

        trainedStats = self.bottyamon.train(self.player.rebirths, self.current_world.seed)

        self.console.print(f"[green]{self.bottyamon.name} has been retrained![/]\n")
        self.console.print(f"New stats:\n[red]ATK[/red] :crossed_swords: : {trainedStats[0]}\n[blue]DEF[/blue] :shield: : {trainedStats[1]}\n:star: Rarity: [yellow]{trainedStats[2]}[/yellow]")

if __name__ == '__main__':
    BottyamonCmd().cmdloop()