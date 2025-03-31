from mesa import Agent, Model
from pydantic import BaseModel, ConfigDict
from typing import Tuple, List
from objects import Waste
import numpy as np
import random

COLOR_CODE = {'green':0, 'yellow':1, 'red':2}
CODE_COLOR =  {v: k for k, v in COLOR_CODE.items()}

class Knowledge(BaseModel):
   position:Tuple[int, int]
   target_positions:np.ndarray
   my_zone:Tuple[int, int, int, int] # x_min, x_end, y_min, y_end
   allowed_zone:Tuple[int, int, int, int]
   actions:List[str]=[] # list of actions
   reset_zone:bool=True
   model_config = ConfigDict(arbitrary_types_allowed=True)

class Robot(Agent):
    def __init__(self, model:Model, knowledge:Knowledge, color):
      super().__init__(model)
      self.knowledge=knowledge
      self.color=color
      self.waste_carried=[]
      self.available=True # is carrying at most one waste of their own color

    #  allows the agent to get information from the environment.
    def update(self, percepts):
        for position, contents in percepts.items():
            x,y=position
            waste = [0,0,0]
            for agent_color in contents:
                waste[COLOR_CODE[agent_color]]+=1
            self.knowledge.target_positions[x, y, :] = waste
        
    def is_at_limit(self):
        x,y=self.knowledge.position
        x_min, x_end, y_min, y_end = self.knowledge.my_zone
        return x==x_end
   
    # corresponds to the “reasoning” step of the agent. It takes as input the “knowledge” 
    def deliberate(self):
       if len(self.waste_carried)==2 and self.color!='red':
           return 'TRANSFORM'
       elif not self.available and self.is_at_limit():
           return 'PUTDOWN'
       elif not self.available:
           # go right to drop it off
           return 'MOVE RIGHT'
       
       x,y = self.knowledge.position
       color_code = COLOR_CODE[self.color]
       targets = self.knowledge.target_positions[:,:,color_code]

       if targets[x,y]>0:
          return 'PICKUP'
       
       target_positions = np.argwhere(targets > 0)

       if target_positions.size == 0:
           return 'MOVE'
       
       distances = np.abs(target_positions[:, 0] - x) + np.abs(target_positions[:, 1] - y)
       nearest_target = target_positions[np.argmin(distances)]
       target_x, target_y = nearest_target
       
       if target_x < x:
           return 'MOVE LEFT'
       elif target_x > x:
          return 'MOVE RIGHT'
       elif target_y < y:
           return 'MOVE DOWN'
       elif target_y > y:
           return 'MOVE UP'
            
    def step_agent(self): 
        action = self.deliberate()
        percepts = self.model.do(self, action)
        self.update(percepts)

    def get_possible_moves(self):
        possible_moves = []
        x,y=self.knowledge.position
        x_min, x_end, y_min, y_end = self.knowledge.allowed_zone
        if x > x_min:
            possible_moves.append((x-1, y))
        if x < x_end:
            possible_moves.append((x+1, y))
        if y > y_min:
            possible_moves.append((x, y-1))
        if y < y_end:
            possible_moves.append((x, y+1))
        return possible_moves
     
    def get_logical_moves(self):
        possible_moves = []
        x,y=self.knowledge.position
        x_min, x_end, y_min, y_end = self.knowledge.my_zone
        if x >= x_min and self.color!='green':
            possible_moves.append((x-1, y))
        elif x > x_min:
            possible_moves.append((x-1, y))
        if x < x_end:
            possible_moves.append((x+1, y))
        if y > y_min:
            possible_moves.append((x, y-1))
        if y < y_end:
            possible_moves.append((x, y+1))
        return possible_moves

    def move(self):
        x, y = self.knowledge.position
        x_min, x_end, y_min, y_end = self.knowledge.my_zone
        y_direction = 1 if x%2 else -1
        x_direction = 1 if self.knowledge.reset_zone else -1

        possible_moves = self.get_logical_moves()
        candidate = (x, y+y_direction)

        if candidate in possible_moves:
            return candidate
        candidate = (x+x_direction, y)
        if candidate in possible_moves:
            return candidate
        
        self.knowledge.reset_zone = not self.knowledge.reset_zone
        candidate = (x-x_direction, y)
        assert candidate in possible_moves
        return candidate
        
    def pickup(self, obj):
       self.waste_carried.append(obj)
       if len(self.waste_carried)==2 or self.color=='red':
           self.available=False
           
   
    def transform(self, new_waste):
        self.waste_carried = [new_waste]
    
    def putdown(self, obj):
        self.waste_carried.remove(obj)
        self.available=True


class greenAgent(Robot):
    def __init__(self, model: Model):
        width, height = model.width, model.height
        my_zone = (0, width // 3 - 1, 0, height - 1)
        allowed_zone = (0, width // 3 - 1, 0, height - 1)
        position = (random.randint(my_zone[0], my_zone[1]), random.randint(my_zone[2], my_zone[3]))
        target_positions = np.zeros((width, height, 3), dtype=int)
        knowledge = Knowledge(position=position, target_positions=target_positions, my_zone=my_zone, allowed_zone=allowed_zone, actions=[])
        super().__init__(model, knowledge, 'green')

class yellowAgent(Robot):
    def __init__(self, model: Model):
        width, height = model.width, model.height
        my_zone = (width // 3, 2 * width // 3 - 1, 0, height - 1)
        allowed_zone = (0, 2 * width // 3 - 1, 0, height - 1)
        position = (random.randint(my_zone[0], my_zone[1]), random.randint(my_zone[2], my_zone[3]))
        target_positions = np.zeros((width, height, 3), dtype=int)
        knowledge = Knowledge(position=position, target_positions=target_positions, my_zone=my_zone, allowed_zone=allowed_zone, actions=[])
        super().__init__(model, knowledge, 'yellow')

class redAgent(Robot):
    def __init__(self, model: Model):
        width, height = model.width, model.height
        my_zone = (2 * width // 3, width - 1, 0, height - 1)
        allowed_zone = (0, width - 1, 0, height - 1)
        position = (random.randint(my_zone[0], my_zone[1]), random.randint(my_zone[2], my_zone[3]))
        target_positions = np.zeros((width, height, 3), dtype=int)
        knowledge = Knowledge(position=position, target_positions=target_positions, my_zone=my_zone, allowed_zone=allowed_zone, actions=[])
        super().__init__(model, knowledge, 'red')

    def deliberate(self):
       x_min, x_end, y_min, y_end = self.knowledge.my_zone
       waste_disposal = (x_end, (y_end+1)//2)
       x, y = self.knowledge.position

       if not self.available:
           if self.knowledge.position == waste_disposal:
               return 'PUTDOWN'
           if x<x_end:
               return 'MOVE RIGHT'
           if y>waste_disposal[1]:
               return 'MOVE DOWN'
           return 'MOVE UP'
       
       color_code = COLOR_CODE[self.color]
       targets = self.knowledge.target_positions[:,:,color_code]

       if targets[x,y]>0:
          return 'PICKUP'
       
       target_positions = np.argwhere(targets > 0)

       if target_positions.size == 0:
           return 'MOVE'
       
       distances = np.abs(target_positions[:, 0] - x) + np.abs(target_positions[:, 1] - y)
       nearest_target = target_positions[np.argmin(distances)]
       target_x, target_y = nearest_target
       
       if target_x < x:
           return 'MOVE LEFT'
       elif target_x > x:
          return 'MOVE RIGHT'
       elif target_y < y:
           return 'MOVE DOWN'
       elif target_y > y:
           return 'MOVE UP'