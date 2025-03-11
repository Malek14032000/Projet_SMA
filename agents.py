from mesa import Agent, Model
from pydantic import BaseModel
from typing import Tuple, List

class Knowledge(BaseModel):
   position:Tuple[int, int]
   target_positions:List[Tuple[int, int]]
   my_zone:Tuple[int, int, int, int] # x_min, x_end, y_min, y_end
   allowed_zone:Tuple[int, int, int, int]
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
       self.model.grid.place_agent(self, new_position)
       self.knowledge.position=new_position

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