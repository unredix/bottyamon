import random

class Bottyamon:
    def __init__(self, breed, name, hp):
        self.breed = breed
        self.name = name
        self.baseAtk = 0
        self.defense = 0
        self.hp = hp
        self.rarity = "unknown"
        self.isEvo = False

    def train(self, rebirths, seed):
        
        rebirthMultiplier = 1
        if rebirths > 0:
            rebirthMultiplier = 1.25

        if seed:
            random.seed(seed)


        self.baseAtk = round(random.randint(5, 15) * rebirthMultiplier)
        self.defense = round(random.randint(10, 20) * rebirthMultiplier)

        # rating < 20 --> C
        # 20 <= rating < 30 --> B
        # rating > 30 --> A  
        # rating >= 35 --> S

        rating = (self.baseAtk + self.defense)
        rarity = "C"

        if rating >= 20 and rating < 30:
            rarity = "B"
        elif rating >= 30 and rating < 35:
            rarity = "A"
        elif rating >= 35:
            rarity = "S"

        self.rarity = rarity
        return [self.baseAtk, self.defense, self.rarity]