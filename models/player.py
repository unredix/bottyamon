class Player:
    def __init__(self):
        self.lvl = 0
        self.xp = 0
        self.rebiths = 0
        self.deaths = 0
        self.inventory = {}
        self.money = 20
        self.upgrades = []
    
    def addItem(self, item, amount):
        self.inventory[item] += amount

        return True
    
    def removeItem(self, item, amount):
        if not self.inventory[item]:
            return False
        
        if self.inventory[item] < amount:
            return ValueError

        if self.inventory[item] == amount:
            del self.inventory[item]
            return True
        
        self.inventory[item] -= amount
        return True
        
    def addMoney(self, amount):
        self.money += amount

        return True

