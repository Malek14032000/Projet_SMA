from mesa import Agent, Model
from mesa.space import MultiGrid
import random


class Radioactivity(Agent):
    def __init__(self, model, position, color):
        super().__init__(model)
        self.position = position
        self.color = color
    
    def step_agent(self): 
        pass

class  WasteDisposalZone(Agent):
    def __init__(self, model):
        super().__init__(model)
        width, height = model.width, model.height
        self.position = (width-1, height//2)
        
    def step_agent(self): 
        pass
    
class Waste(Agent):
    def __init__(self, model):
        super().__init__(model)
        width, height = model.width, model.height
        self.position = (random.randint(0, width-1), random.randint(0, height-1))
        
    def step_agent(self): 
        pass
