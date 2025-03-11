from mesa import Agent, Model
from mesa.space import MultiGrid
from random import random


class Radioactivity(Agent):
    def __init__(self, model, width=10, height=10, seed=None):
        super().__init__(model, seed=seed)
        self.position = (random.randrange(start=0, stop=width), random.randrange(start=0, stop=height))

class  WasteDisposalZone(Agent):
    def __init__(self, model, width=10, height=10, seed=None):
        super().__init__(model, seed=seed)
        self.position = (width, random.randrange(start=0, stop=height))

class Waste(Agent):
    def __init__(self, model, width=10, height=10, seed=None):
        super().__init__(model, seed=seed)
        self.position = (random.randrange(start=0, stop=width), random.randrange(start=0, stop=height))
