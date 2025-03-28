from mesa import Model
from mesa.space import MultiGrid
from agents import greenAgent, yellowAgent, redAgent
from objects import Radioactivity, WasteDisposalZone, Waste
from random import random


class RobotMission(Model):
    def __init__(self, n_g, n_y, n_r, n_waste, width=10, height=10, seed=None):
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
                agent = agent_type(self)
                self.grid.place_agent(agent, agent.knowledge.position)
        
        ## place waste
        for _ in range(self.num_waste):
            agent = Waste(self)
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
            

    def step(self):
        self.agents.shuffle_do("step_agent")
        
        
    def do(self, agent, action):
        if action == "MOVE":
            # check if it is feasible
            new_position = agent.move()
            if new_position is not None:
                self.grid.move_agent(agent, new_position)
                agent.knowledge.position = new_position
                                
        elif action == "PICKUP":
            agent.pickup()
        elif action == "TRANSFORM":
            agent.transform()
        elif action == "PUTDOWN":
            agent.putdown()
            
        percepts = {
                    neighbor_pos: [obj for obj in self.grid.get_cell_list_contents(neighbor_pos)]
                    for neighbor_pos in self.grid.iter_neighbors(new_position, moore=True, include_center=True)
                }
        
        return percepts


    def get_all_agents_positions(self):
        return [a.knowledge.position for a in self.agents]