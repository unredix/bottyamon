import random
from rich import print as rprint #type:ignore
class World():
    def __init__(self, name):
        self.events = []
        self.name = name
        self.seed = 0
        self.progress = 0
        self.length = 0

    def genSeed(self):
        self.seed = random.randint(10000,99999)
        return self.seed
    
    def buildWorld(self, seed, length):
        self.length = length
        
        random.seed(seed)
        events = []

        shopPity = 0
        safePointPity = 0

        for _ in range(length):
            eventNum = random.randint(1,15)
            
            if shopPity >= 5:
                events.append(1)
                shopPity = 0
                continue

            if safePointPity >= 10:
                events.append(15)
                safePointPity = 0
                continue

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


        self.events = events
        
        return events
        
