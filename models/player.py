class Player:
    def __init__(self):
        self.lvl = 0
        self.xp = 0
        self.rebirths = 0
        self.deaths = 0
        self.inventory = {}
        self.money = 20
        self.effects = []
    
    def addItem(self, item, amount):
        if item not in self.inventory:
            self.inventory[item] = 0
        self.inventory[item] += amount

        return True
    
    def removeItem(self, item, amount):
        if item not in self.inventory or not self.inventory[item]:
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
    
    def addXp(self, xp):
        if (self.xp + xp) >= 100:
            self.lvl += 1
            self.xp = 100 - (self.xp + xp)
        
            return True
        
        self.xp += xp
        return False
        


