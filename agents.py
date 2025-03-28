from mesa import Agent, Model
from pydantic import BaseModel
from typing import Tuple, List
import random

class Knowledge(BaseModel):
   position:Tuple[int, int]
   target_positions:List[Tuple[int, int]]
   my_zone:Tuple[int, int, int, int] # x_min, x_end, y_min, y_end
   allowed_zone:Tuple[int, int, int, int]
   carrying:int # 0 if nothing, 
                # 1 if carrying one of the robot's own color,
                # 2 if carrying one of the next color
   percepts:List[str] # list of percepts
   actions:List[str]# list of actions

class Robot(Agent):
    def __init__(self, model:Model, knowledge:Knowledge):
      super().__init__(model)
      self.knowledge=knowledge

    def update(self, percepts):
       self.knowledge.percepts.append(percepts)

    def deliberate(self):
       return "MOVE"

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
        
    def move(self):
       possible_moves = self.get_possible_moves()
       new_position = self.random.choice(possible_moves)
       return new_position

    def pickup(self):
       pass
   
    def transform(self):
        pass
    
    def putdown(self):
        pass


class greenAgent(Robot):
    def __init__(self, model: Model):
        width, height = model.width, model.height
        my_zone = (0, width // 3 - 1, 0, height - 1)
        allowed_zone = (0, width // 3 - 1, 0, height - 1)
        position = (random.randint(my_zone[0], my_zone[1]), random.randint(my_zone[2], my_zone[3]))
        knowledge = Knowledge(position=position, target_positions=[], my_zone=my_zone, allowed_zone=allowed_zone, carrying=0, percepts=[], actions=[])
        super().__init__(model, knowledge)

class yellowAgent(Robot):
    def __init__(self, model: Model):
        width, height = model.width, model.height
        my_zone = (width // 3, 2 * width // 3 - 1, 0, height - 1)
        allowed_zone = (0, 2 * width // 3 - 1, 0, height - 1)
        position = (random.randint(my_zone[0], my_zone[1]), random.randint(my_zone[2], my_zone[3]))
        knowledge = Knowledge(position=position, target_positions=[], my_zone=my_zone, allowed_zone=allowed_zone, carrying=0, percepts=[], actions=[])
        super().__init__(model, knowledge)

class redAgent(Robot):
    def __init__(self, model: Model):
        width, height = model.width, model.height
        my_zone = (2 * width // 3, width - 1, 0, height - 1)
        allowed_zone = (0, width - 1, 0, height - 1)
        position = (random.randint(my_zone[0], my_zone[1]), random.randint(my_zone[2], my_zone[3]))
        knowledge = Knowledge(position=position, target_positions=[], my_zone=my_zone, allowed_zone=allowed_zone, carrying=0, percepts=[], actions=[])
        super().__init__(model, knowledge)