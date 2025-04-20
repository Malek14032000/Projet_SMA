from mesa import Model
from mesa.space import MultiGrid
from agents import greenAgent, yellowAgent, redAgent, Robot, CODE_COLOR, COLOR_CODE
from objects import Radioactivity, WasteDisposalZone, Waste
from random import random
import mesa
from metrics import *

class RobotMission(Model):
    def __init__(self, n_g, n_y, n_r, n_waste, width=10, height=10, seed=None, strategy=2):
        super().__init__(seed=seed)
        self.width = width 
        self.height = height
        self.num_green_agents = n_g
        self.num_yellow_agents = n_y
        self.num_red_agents = n_r
        self.num_waste = n_waste
        
        self.grid = MultiGrid(width, height, torus=False)
        
        ## place robots
        agent_mapping = {
            greenAgent: self.num_green_agents,
            yellowAgent: self.num_yellow_agents,
            redAgent: self.num_red_agents,
        }
        for agent_type, num_agents in agent_mapping.items():
            for _ in range(num_agents):
                agent = agent_type(self, strategy)
                self.grid.place_agent(agent, agent.knowledge.position)
        
        ## place waste
        for _ in range(self.num_waste//3):
            agent = Waste(self, 'green')
            self.grid.place_agent(agent, agent.position)
        for _ in range(self.num_waste//3, 2*self.num_waste//3):
            agent = Waste(self, 'yellow')
            self.grid.place_agent(agent, agent.position)
        for _ in range(2*self.num_waste//3, self.num_waste):
            agent = Waste(self, 'red')
            self.grid.place_agent(agent, agent.position)
            
        ## place waste disposal zone
        agent = WasteDisposalZone(self)
        self.grid.place_agent(agent, agent.position)
        
        ## place radioactivity agents (with no behaviour, just to delimit the zones)
        for x in range(width):
            for y in range(height):
                if x >= 0 and x <= width // 3 - 1:
                    self.grid.place_agent(Radioactivity(self, (x,y), "green"), (x,y))
                elif x >= width // 3  and x <= 2 * width // 3 - 1:
                    self.grid.place_agent(Radioactivity(self, (x,y), "yellow"), (x,y))
                else:
                    self.grid.place_agent(Radioactivity(self, (x,y), "red"), (x,y))
        
        
        self.datacollector = mesa.DataCollector(
            model_reporters={
        "Total_waste_disposed": compute_disposed_waste,
        "Left_waste_green": lambda m: m.count_waste("green"),
        "Left_waste_yellow": lambda m: m.count_waste("yellow"),
        "Left_waste_red": lambda m: m.count_waste("red")
    })
        
        self.datacollector.collect(self)
            
    def step(self):
        self.agents.shuffle_do("step_agent")
        self.datacollector.collect(self)
        
    #  inform the environment of its actions
    def do(self, agent:Robot, action):   
        new_position=None      
        x,y=agent.knowledge.position

        if action == "PICKUP":
            self.pickup(agent)
        elif action == "TRANSFORM":
            self.transform(agent)
        elif action == "PUTDOWN":
            self.putdown(agent)
        elif action == "MOVE":
            new_position = agent.move()
        elif action == "MOVE RIGHT":
            new_position = (x+1, y)
        elif action == "MOVE LEFT":
            new_position = (x-1, y)
        elif action == "MOVE DOWN":
            new_position = (x, y-1)
        elif action == "MOVE UP":
            new_position = (x, y+1)
        elif action!="NONE":
            print('No action')
            raise Exception(f'no action {action}')
        
        new_position = self.move_agent(agent, new_position)
        
        percepts_waste = {
                    neighbor_pos: [obj.radioactivity_level for obj in self.grid.get_cell_list_contents([neighbor_pos])
                                   if (isinstance(obj, Waste) and obj.active)]
                    for neighbor_pos in self.grid.get_neighborhood(new_position, moore=False, include_center=True)
                }
        
        percepts_agent = [agent, new_position]
        percepts = {'agent': percepts_agent, 'waste': percepts_waste}
        return percepts

    def get_all_agents_positions(self):
        return [a.knowledge.position for a in self.agents]
    
    def putdown(self, agent):
        if len(agent.waste_carried)>=1:
            waste = agent.waste_carried[0]
            waste.active=True
            agent.putdown(waste)
        
        if agent.pos==(self.width-1, self.height//2):
            self.grid.remove_agent(waste)

    def move_agent(self, agent, new_position):
        if new_position in agent.get_possible_moves():
            self.grid.move_agent(agent, new_position)
            agent.knowledge.position=new_position
            for obj in agent.waste_carried:
                self.grid.move_agent(obj, new_position)
        else:
            new_position=agent.knowledge.position
        return new_position

    def pickup(self, agent):
        contents = self.grid.get_cell_list_contents([agent.knowledge.position])
        waste = [w for w in contents if isinstance(w, Waste) and w.radioactivity_level==agent.color and w.active]
        if len(waste)>0 and agent.available:
            agent.pickup(waste[0])
            waste[0].active=False

    def transform(self, agent):
        assert len(agent.waste_carried)==2
        for w in agent.waste_carried:
            assert w.radioactivity_level==agent.color
            if w.pos is not None:
                self.grid.remove_agent(w)
        new_waste = Waste(self, CODE_COLOR[1 + COLOR_CODE[agent.color]])
        self.grid.place_agent(new_waste, agent.knowledge.position)
        agent.transform(new_waste)
    def count_waste(self, color):
        count = 0
        for contents, (x, y) in self.grid.coord_iter():
            for agent in contents:
                if isinstance(agent, Waste) and agent.radioactivity_level == color and agent.active:
                    count += 1
        return count