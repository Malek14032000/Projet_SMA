from mesa import Agent, Model
from pydantic import BaseModel
from typing import Tuple, List

class Knowledge(BaseModel):
   position:Tuple[int, int]
   target_positions:List[Tuple[int, int]]
   my_zone:Tuple[int, int, int, int] # x_min, x_end, y_min, y_end
   allowed_zone:Tuple[Tuple[int, int]]
   carrying:int # 0 if nothing, 
                # 1 if carrying one of the robot's own color,
                # 2 if carrying one of the next color

class Robot(Agent):
    def __init__(self, model:Model, knowledge:Knowledge):
      super().__init__(model)
      self.knowledge=knowledge

    def update(self):
       pass

    def deliberate(self):
       pass

    def step_agent(self): 
        self.update() 
        action = self.deliberate() 
        self.model.do(self, action) 

    def move(self):
       
       possible_moves = []

    def pickup(self):
       pass

class greenAgent(Robot):
    def __init__(self, model:Model, knowledge:Knowledge):
      super().__init__(model, knowledge)


class yellowAgent(Robot):
    def __init__(self, model:Model, knowledge:Knowledge):
      super().__init__(model, knowledge)
 

class redAgent(Robot):
    def __init__(self, model:Model, knowledge:Knowledge):
      super().__init__(model, knowledge)