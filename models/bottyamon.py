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


        self.baseAtk = round(random.randint(5, 10) * rebirthMultiplier)
        self.defense = round(random.randint(1, 10) * rebirthMultiplier)

        rating = (self.baseAtk + self.defense)
        rarity = "C"

        if rating >= 10 and rating < 15:
            rarity = "B"
        elif rating >= 15 and rating < 20:
            rarity = "A"
        elif rating >= 21:
            rarity = "S"

        self.rarity = rarity
        return [self.baseAtk, self.defense, self.rarity]