import random

class Battle:
    def __init__(self, player, bottyamon, enemy):
        self.player = player
        self.bottyamon = bottyamon
        self.enemy = enemy

class Shop:
    def __init__(self):
        self.shopItems = {}
        self.possibleItems = ["Strength Potion (+3)", "Strength Potion (+5)", "Defense Potion (+5)", "Defense Potion (+8)", "HP Potion (+5)", "HP Potion (+8)", "Pickaxe", "Axe", "Retrain pill", "Rope", "Duck tape", "Flashlight"] 
        self.basket = {}

    def generateShop(self):

        numOfItems = random.randint(3,8)
        itemPrices = {self.possibleItems[0]:10,self.possibleItems[1]:15,self.possibleItems[2]:10,self.possibleItems[3]:15,self.possibleItems[4]:10,self.possibleItems[5]:15, self.possibleItems[6]:5, self.possibleItems[7]:5, self.possibleItems[8]:25, self.possibleItems[9]:5, self.possibleItems[10]:5, self.possibleItems[11]:5}

        counter = 1
        for _ in range(numOfItems):
            chosen = random.choice(self.possibleItems)
            amount = random.randint(1,4)
            price = itemPrices[chosen]

            self.shopItems[chosen] = {"iid": counter,"amount":amount, "price":price}

            counter += 1

class SafePoint:
    def __init__(self):
        self.traderItem = {}
        self.possibleItems = ["Pickaxe", "Axe", "Rope", "Duck tape", "Flashlight"] 

    def generateTrader(self):
        self.traderItem= {"name": random.choice(self.possibleItems), "price": random.randint(5,20)}
