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
    def __init__(self, model, radioactivity_level):
        super().__init__(model)
        width, height = model.width, model.height
        self.radioactivity_level = radioactivity_level
        self.active = True # is not carried

        if radioactivity_level == "green":
            x_range = (0, width // 3 - 1)
        elif radioactivity_level == "yellow":
            x_range = (width // 3, 2 * width // 3 - 1)
        elif radioactivity_level == "red":
            x_range = (2 * width // 3, width - 1)
        else:
            raise ValueError("Invalid radioactivity level. Choose 'green', 'yellow', or 'red'.")

        y_range = (0, height - 1)
        self.position = (random.randint(*x_range), random.randint(*y_range))
        
        
    def step_agent(self): 
        pass
