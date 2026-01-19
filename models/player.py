class Player:
    def __init__(self):
        self.lvl = 0
        self.rebiths = 0
        self.deaths = 0
        self.inventory = {}
        self.money = 20
        self.upgrades = []
    
    def addItem(item, amount):
        
        if len(Player.inventory.keys()) >= 10:
            if ("invUpgrade" in Player.upgrades) and len(Player.inventory.keys()) <= 20:
                Player.inventory[item] += amount
            else:
                return ValueError
        
        elif len(Player.inventory.keys()) < 10:
            Player.inventory[item] += amount


