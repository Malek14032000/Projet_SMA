from mesa import Model
from mesa.space import MultiGrid
from agents import greenAgent, yellowAgent, redAgent
from random import random


class RobotMission(Model):
    def __init__(self, n_g, n_y, n_r, width=10, height=10, seed=None):
        super().__init__(seed=seed)
        self.num_green_agents = n_g
        self.num_yellow_agents = n_y
        self.num_red_agents = n_r
        
        self.grid = MultiGrid(width, height, torus=True)
        
        agent_mapping = {
            greenAgent: self.num_green_agents,
            yellowAgent: self.num_yellow_agents,
            redAgent: self.num_red_agents,
        }

        for agent_type, num_agents in agent_mapping.items():
            for _ in range(num_agents):
                agent = agent_type(self)

                # Assign a random position within the agent's zone
                x = self.random.randrange(start=self.agent.knowledge.my_zone[0][0], stop=self.agent.knowledge.my_zone[1][0])
                y = self.random.randrange(start=self.agent.knowledge.my_zone[0][1], stop=self.agent.knowledge.my_zone[1][1])

                self.grid.place_agent(agent, (x, y))

        self.running = True

    def step(self):
        self.agents.shuffle_do("step_agent")

    def get_all_agents_positions(self):
        return [a.knowledge.position for a in self.agents]