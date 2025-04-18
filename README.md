# 🤖 Self-organization of Robots in a Hostile Environment  

This project simulates the mission of autonomous robots tasked with collecting, transforming, and transporting hazardous waste in a radioactive environment. The robots operate in three distinct zones, each with varying levels of radioactivity, and each robot type has specific capabilities and restrictions. This simulation uses a multi-agent system (MAS) to model collaborative behavior in a hostile environment.

## Table of Contents  

- [Project Overview](#project-overview)
- [Structure](#structure)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Methodology](#methodology)
- [Results](#results)
- [Limits & Improvements](#limits)
- [Contributors](#contributors)

## Project Overview

This project simulates a multi-agent system where robots cooperate to clean hazardous waste in a radioactive environment. The environment is divided into three zones based on radioactivity levels, and each type of robot has specialized tasks within these zones:

### **Zones:**

1. **Zone 1 (Low Radioactivity):** Contains green waste, accessible only to **Green Robots**.
2. **Zone 2 (Medium Radioactivity):** Contains yellow waste, accessible to **Yellow** and **Red Robots**.
3. **Zone 3 (High Radioactivity):** A storage area for fully processed waste, accessible only to **Red Robots**.

### **Key Features:**

- **Robot Types:**  
  - **Green Robots:** Collect and transform green waste into yellow waste.  
  - **Yellow Robots:** Collect and transform yellow waste into red waste.  
  - **Red Robots:** Transport red waste to the disposal zone.  

- **Agent Behaviors:**  
  - Perception, deliberation, and action cycles for autonomous decision-making.  
  - Communication capabilities between robots for improved collaboration (this will be added in future steps).  

- **Visualization:**  
  - Real-time simulation with an interactive visualization to observe robot behaviors and waste processing in action.


## Structure

  - `agents.py`: Agents implementation.
  - `model.py`: Environment implementation.
  - `objects.py`: Objects implementation as inactive agents (waste/radioactivity cells...)
  - `server.py`: Contains all the necessary for running the visualisation.
  - `run.py`: Handles the launch of the simulation.
  - `metrics.py`: Implementation of monitoring metrics used to compare agent strategies.

## Prerequisites  

Ensure the following tools and libraries are installed:  

- **Python 3.11+**  
- **Required Libraries:** You will find the required packages in the [requirements.txt](#requirements.txt) file.


## Usage  

1. Clone this repository:
    ```bash
    git clone https://github.com/Malek14032000/Projet_SMA.git
    cd Projet_SMA
    ```
   
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the simulation:
    ```bash
    python run.py
    ```

4. Visualisation: 
Once the simulation starts, a browser-based visualization will automatically open to allow you to observe the robots' activities in real-time. You can set up your own configuration by modifying the parameters `number of green agents`, `number of yellow agents`, `number of red agents` and  `number of waste`.

## Methodology

In this project, we experimented 3 strategies of agent behaviours. We will explain each one of them below and present the comparaison results in the next section.

#### **Agents class inheritance**
The following UML class diagram is explains the inheritance links between all different types of agents we will present later. It is the same for the 3 strategies.
```
               Agent (mesa)
                 ↑ 
               Robot
     ↑          ↑          ↑
GreenAgent  YellowAgent  RedAgent
```
All moving agents inherent from class `Robot`, present in `agents.py` module. This class contains an argument named `strategy` that allows us to choose the strategy `1`, `2` or `3`.

#### **Agents knowledge**
The `Knowledge` class, also present in `agents.py` module, represents the knowledge of an agent and its state during the simulation. Its main attributes are:

- `position`: represents the current position of the agent.
- `target_positions`: the vision of the agent of all the grid. It is a matrix size of the grid * 3, 3 as there are 3 types of waste possible. each time the agent moves, it will update this matrix with what it sees. In fact, meanwhile the other agents can pickup and transform waste. This new information will not update the matrix in this cas as the agents do not communicate.
- `my_zone`: represents the coordinates of the corners of the zone assigned to the agent. For the green/yellow/red agent, it will be a tuple of the corner coordinates of respectively the green/yellow/red zone.
- `allowed_zone`: represents the coordinates of the corners of the allowed zone for the agent. In fact, the green agent can only move in the green zone, the yellow agent can move in the green and the yellow zones, and finally the red agent can move in all 3 zones.
- `available_agents_pos`: only used when agents communicate. This allows each agent to know where the other agents, green/yellow/red, are in the grid.

### Strategy 1 : Agents with no communication, moving greedily

In this first approach, we made the following choices:
- agents move greedily in the grid (move to the next column in the grid only after having moved in all cells in the previous column)
- agents cannot communicate between each other. 
- if sees something goes back to it directly 






### Strategy 2 : Agents with communication
- greedy
- a une meilleur vue car ils communiquent et donc va à des endroits que les autres ont vu quelque chose. et si un waste a été pris, ça s'update pour tout les agents. ici y a juste un risque que deux agents vont aux meme endroit et comme ça on perd du temps


### Strategy 3 : Agents with advanced communication

- même strategy que 2 sauf on ajoute que les agents quand ils communiquent, le plus proche qu waste vu, va au waste et si y a deux qui sont equidistant, il y a un autre de priorité. l'agent qui a l'id le plus bas va le prendre et l'autre cherche un autre.
.....

## Results
We ran the simulations using a `batch_size` of 3  to take into account the randomness in both waste placement and the behavior of the chosen strategy. For each configuration, we varied the number of waste items and agents per zone. Then, we ran the simulation multiple times (equal to the batch size) and computed the average time taken to fully clean the grid.

- show table !!!

We clearly see that the agent following 



## Limits & Improvements
In this project, we implemented and benchmarked three distinct behavior strategies for the agents. However, our methodology has a few limitations:

- The simulation currently operates on a grid with a fixed size and fixed regions, which limits flexibility for testing in different environments. It would 

- Although we ran multiple simulations per configuration to reduce the variance, the overall batch size remains small, making our results not reliable enough.

- We could enhance our monitoring by introducing additional performance indicators, such as the time an agent spents not performing any useful action. This would help clarify our optimization goals — are we aiming solely for fast map cleaning, or do we also want to minimize energy/resource usage?

- In our implementation, each of the three zones contains the same amount of waste. However, this causes an imbalance since the red zone ends up being consistently overloaded compared to the others. A potential improvement would be to vary the waste density across zones and observe how it impacts the overall efficiency.

## Contributors

- Ammar Mariem
- Ben Younes Lina
- Bouhadida Malek