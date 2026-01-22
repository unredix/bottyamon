import random


class Battle:
    def __init__(self, player, bottyamon, enemy):
        self.player = player
        self.bottyamon = bottyamon
        self.enemy = enemy

class Shop:
    def __init__(self):
        self.shopItems = None
        self.possibleItems = ["Strength Potion (+3)", "Strength Potion (+5)", "Defense Potion (+5)", "Defense Potion (+8)", "HP Potion (+5)", "HP Potion (+8)", "Pickaxe", "Axe", "Retrain pill", "Rope", "Duck tape", "Flashlight"] 
        
    def generateShop(self, seed):
        random.seed(seed)

        numOfItems = random.randint(3,8)

        for _ in range(numOfItems):
            chosen = random.choice(self.possibleItems)
            amount = random.randint(1,4)

            self.shopItems[chosen] = amount
        