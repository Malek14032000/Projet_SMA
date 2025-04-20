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
   target_positions:np.ndarray # grid width x grid heigth x 3
   my_zone:Tuple[int, int, int, int] # x_min, x_end, y_min, y_end
   allowed_zone:Tuple[int, int, int, int]
   available_agents_pos:dict={'green':{}, 'yellow':{}, 'red':{}}
   reset_zone:bool=True
   model_config = ConfigDict(arbitrary_types_allowed=True)

class Robot(Agent):
    def __init__(self, model:Model, knowledge:Knowledge, color, strategy=3):
      super().__init__(model)
      self.knowledge=knowledge
      self.color=color
      self.waste_carried=[]
      self.available=True # is carrying at most one waste of their own color
      self.strategy=strategy
      self.terminated = False

    #  allows the agent to get information from the environment.
    def update(self, percepts):
        """Collects information from the environment."""
        for position, contents in percepts['waste'].items():
            x,y=position
            waste = [0,0,0]
            for agent_color in contents:
                waste[COLOR_CODE[agent_color]]+=1
            self.knowledge.target_positions[x, y, :] = waste
        agent, position = percepts['agent']
        assert isinstance(agent, Robot)
        
        if not agent.available:
            position=None
        agent_id = agent.unique_id
        self.knowledge.available_agents_pos[agent.color][agent_id]=position
          
    def is_at_limit(self):
        """Check if the agent is at the limit of its zone."""
        x,y=self.knowledge.position
        x_min, x_end, y_min, y_end = self.knowledge.my_zone
        return x==x_end
    
    def target_is_free(self, nearest_target, distance_self, target_positions):
        """Check if the target is free."""
        for agent_id, position in self.knowledge.available_agents_pos[self.color].items():
            if position is None: # The agent is not available
                continue
            distance_other_agent =np.abs(position[0] - nearest_target[0])\
                + np.abs(position[1] - nearest_target[1])
            if (distance_self>distance_other_agent) \
                or (distance_self==distance_other_agent and self.unique_id<agent_id) :
                # The agent has priority on the waste, but he might be focused on something else
                distances = np.abs(target_positions[:, 0] - position[0]) + np.abs(target_positions[:, 1] - position[1])
                i=np.argmin(distances)
                if (nearest_target == target_positions[i]).all():
                    return False
        return True

    def get_assigned_target(self):
       """Get the assigned target for the agent."""
       x,y = self.knowledge.position
       color_code = COLOR_CODE[self.color]
       targets = self.knowledge.target_positions[:,:,color_code]

       target_positions_arr = np.argwhere(targets > 0)
       
       distances = list(np.abs(target_positions_arr[:, 0] - x) + np.abs(target_positions_arr[:, 1] - y))
       target_positions = list(target_positions_arr)
       while len(distances)>0:
           i=np.argmin(distances)
           nearest_target = target_positions[i]
           if self.target_is_free(nearest_target, distances[i], target_positions_arr):
               return nearest_target
           distances.pop(i)
           target_positions.pop(i)
       return None
    
    def get_exploratory_target(self):
        """Get the exploratory target for the agent."""
        x,y = self.knowledge.position
        color_code = COLOR_CODE[self.color]
        x_min, x_end, y_min, y_end=self.knowledge.my_zone
        targets = self.knowledge.target_positions[x_min:x_end+1,:,color_code]
        target_positions_arr = np.argwhere(targets < 0)
        distances = list(np.abs(target_positions_arr[:, 0] - x) + np.abs(target_positions_arr[:, 1] - y))
        target_positions=list(target_positions_arr)

        while len(distances)>0:
           i=np.argmin(distances)
           nearest_target = target_positions[i]
           if self.target_is_free(nearest_target, distances[i], target_positions_arr):
               return nearest_target
           distances.pop(i)
           target_positions.pop(i)
        return None
    
    def go_to(self, target):
        """Move towards the target."""
        target_x, target_y = target
        x,y = self.knowledge.position
        if target_x < x:
            return 'MOVE LEFT'
        elif target_x > x:
            return 'MOVE RIGHT'
        elif target_y < y:
            return 'MOVE DOWN'
        elif target_y > y:
            return 'MOVE UP'
        
    
    def deliberate(self):
        """Decide the next action. Corresponds to the “reasoning” step of the agent. It takes as input the “knowledge” """
        if self.strategy<3:
            action=self.deliberate_v2()
        else:
            action=self.deliberate_v3()
        return action

    def deliberate_v2(self):
        
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
       unknown=np.argwhere(targets < 0)
       
       if target_positions.size>0:
            distances = np.abs(target_positions[:, 0] - x) + np.abs(target_positions[:, 1] - y)
            nearest_target = target_positions[np.argmin(distances)]
            return self.go_to(nearest_target)
       
       if unknown.size>0 or self.strategy==1:
           return 'MOVE'
       
       return self.gather_remaining_waste()


    def deliberate_v3(self):
        if len(self.waste_carried)==2:
            return 'TRANSFORM'
        elif not self.available and self.is_at_limit():
            return 'PUTDOWN'
        elif not self.available:
            return 'MOVE RIGHT'
       
        assigned_target=self.get_assigned_target()

        if assigned_target is not None \
            and assigned_target[0]==self.knowledge.position[0] \
            and assigned_target[1]==self.knowledge.position[1]:
            return 'PICKUP'
        
        if assigned_target is not None:
            return self.go_to(assigned_target)
        
        assigned_target=self.get_exploratory_target()
        if assigned_target is not None and not (assigned_target==self.knowledge.position).all():
            return self.go_to(assigned_target)
        
        return self.gather_remaining_waste()

    def gather_remaining_waste(self):
        """Gather the remaining waste."""
        # the grid is known and empty
        targets = self.knowledge.target_positions[:,:,COLOR_CODE[self.color]]
        empty = (targets == 0).all()
        if not empty:
            return 'NONE'
    
        carrying_agents = [agent_id for agent_id, position in \
             self.knowledge.available_agents_pos[self.color].items() \
                 if position is None]
        carrying_agents.sort()
        if self.unique_id not in carrying_agents:
            self.terminated=True
            return 'NONE'
        idx = carrying_agents.index(self.unique_id)
        if idx<len(carrying_agents)//2:
            if self.is_at_limit():
                self.terminated=True
                return 'PUTDOWN'
            return 'MOVE RIGHT'
        if self.is_at_limit():
            return 'NONE'
        return 'MOVE RIGHT'
        
    def step_agent(self): 
        if self.terminated:
            return 'NONE'
        action = self.deliberate()
        percepts = self.model.do(self, action)
        self.update(percepts)

        # Communication with other agents
        if self.strategy>1:
            for agent in self.model.agents:
                if isinstance(agent, Robot):
                    agent.update(percepts)

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
    def __init__(self, model: Model, strategy=3):
        width, height = model.width, model.height
        my_zone = (0, width // 3 - 1, 0, height - 1)
        allowed_zone = (0, width // 3 - 1, 0, height - 1)
        position = (random.randint(my_zone[0], my_zone[1]), random.randint(my_zone[2], my_zone[3]))
        target_positions = -np.ones((width, height, 3), dtype=int)
        knowledge = Knowledge(position=position, target_positions=target_positions, my_zone=my_zone, allowed_zone=allowed_zone)
        super().__init__(model, knowledge, 'green', strategy)

class yellowAgent(Robot):
    def __init__(self, model: Model, strategy=3):
        width, height = model.width, model.height
        my_zone = (width // 3, 2 * width // 3 - 1, 0, height - 1)
        allowed_zone = (0, 2 * width // 3 - 1, 0, height - 1)
        position = (random.randint(my_zone[0], my_zone[1]), random.randint(my_zone[2], my_zone[3]))
        target_positions = -np.ones((width, height, 3), dtype=int)
        knowledge = Knowledge(position=position, target_positions=target_positions, my_zone=my_zone, allowed_zone=allowed_zone)
        super().__init__(model, knowledge, 'yellow', strategy)

class redAgent(Robot):
    def __init__(self, model: Model, strategy=3):
        width, height = model.width, model.height
        my_zone = (2 * width // 3, width - 1, 0, height - 1)
        allowed_zone = (0, width - 1, 0, height - 1)
        position = (random.randint(my_zone[0], my_zone[1]), random.randint(my_zone[2], my_zone[3]))
        target_positions = -np.ones((width, height, 3), dtype=int)
        knowledge = Knowledge(position=position, target_positions=target_positions, my_zone=my_zone, allowed_zone=allowed_zone)
        super().__init__(model, knowledge, 'red', strategy)

    def deliberate_v2(self):
       x_min, x_end, y_min, y_end = self.knowledge.my_zone
       waste_disposal = (x_end, (y_end+1)//2)
       x, y = self.knowledge.position

       if not self.available:
           if self.knowledge.position == waste_disposal:
               return 'PUTDOWN'
           return self.go_to(waste_disposal)
       
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
       
    def deliberate_v3(self):
        x_min, x_end, y_min, y_end = self.knowledge.my_zone
        waste_disposal = (x_end, (y_end+1)//2)

        if not self.available:
            if self.knowledge.position == waste_disposal:
                return 'PUTDOWN'
            return self.go_to(waste_disposal)

        assigned_target=self.get_assigned_target()
        if assigned_target is not None \
            and assigned_target[0]==self.knowledge.position[0] \
            and assigned_target[1]==self.knowledge.position[1]:
            return 'PICKUP'

        if assigned_target is not None:
            return self.go_to(assigned_target)

        assigned_target=self.get_exploratory_target()
        if assigned_target is not None and not (assigned_target==self.knowledge.position).all():
            return self.go_to(assigned_target)

        return "NONE"
