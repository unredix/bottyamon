import random
from rich import print as rprint #type:ignore

class World:
    def __init__(self, name):
        self.events = 0
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

        for _ in range(length):
            events.append(random.randint(1, 15))
        
        self.events = events
        
        return events
        

