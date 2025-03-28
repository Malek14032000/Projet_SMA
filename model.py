from mesa import Model
from mesa.space import MultiGrid
from agents import greenAgent, yellowAgent, redAgent, Robot, CODE_COLOR, COLOR_CODE
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
            
    def step(self):
        self.agents.shuffle_do("step_agent")
        
    #  inform the environment of its actions
    def do(self, agent:Robot, action):                 
        if action == "PICKUP":
            contents = self.grid.get_cell_list_contents([agent.knowledge.position])
            waste = [w for w in contents if isinstance(w, Waste) and w.radioactivity_level==agent.color]
            if len(waste)>0 and agent.available:
                agent.pickup(waste[0])

        elif action == "TRANSFORM":
            waste1, waste2= agent.waste_carried
            assert waste1.radioactivity_level==agent.color and waste2.radioactivity_level==agent.color  
            for w in agent.waste_carried:
                self.grid.remove_agent(w)
                new_waste = Waste(self, CODE_COLOR[1 + COLOR_CODE[agent.color]])
                self.grid.place_agent(new_waste, agent.knowledge.position)
                agent.transform(new_waste)

        if action == "PUTDOWN":
            agent.putdown()
        
        new_position=None
        if action == "MOVE":
            new_position = agent.move()
        x,y=agent.knowledge.position
        if action == "MOVE RIGHT":
            new_position = (x+1, y)
        if action == "MOVE LEFT":
            new_position = (x-1, y)
        if action == "MOVE DOWN":
            new_position = (x, y-1)
        if action == "MOVE UP":
            new_position = (x, y+1)
        
        if new_position in agent.get_possible_moves():
            self.grid.move_agent(agent, new_position)
            agent.knowledge.position=new_position
            for obj in agent.waste_carried:
                self.grid.move_agent(obj, new_position)
                  
        percepts = {
                    neighbor_pos: [obj.color for obj in self.grid.get_cell_list_contents([neighbor_pos]) if isinstance(obj, Waste)]
                    for neighbor_pos in self.grid.get_neighborhood(new_position, moore=True, include_center=True)
                }
        
        return percepts


    def get_all_agents_positions(self):
        return [a.knowledge.position for a in self.agents]