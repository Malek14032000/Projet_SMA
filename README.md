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

The following UML class diagram is explains the inheritance links between all different types of agents we will present later. It is the same for the 3 strategies.

```
              Robot
     ↑          ↑         ↑
GreenAgent YellowAgent RedAgent
```

All moving agents inherent from class `Robot`. This class contains an argument named `strategy` that allows us to choose the strategy `1`, `2` or `3`.


### Strategy 1 : Agents with no communication, moving greedily

In this first approach, we made the following choices:
- agents move greedily in the grid (move to the next column in the grid only after having moved in all cells in the previous column)
- agents cannot communicate between each other. 

.......






#### **Agents knowledge**
The `Knowledge` class, also present in `agents.py` module, represents the knowledge of an agent and its state during the simulation. It has the following attributes:

- `position`: represents the current position of the agent.
- `target_positions`: the vision of the agent of all the grid. It is a matrix size of the grid * 3, 3 as there are 3 types of waste possible. each time the agent moves, it will update this matrix with what it sees. In fact, meanwhile the other agents can pickup and transform waste. This new information will not update the matrix in this cas as the agents do not communicate.
- `my_zone`: represents the coordinates of the corners of the zone assigned to the agent. For the green/yellow/red agent, it will be a tuple of the corner coordinates of respectively the green/yellow/red zone.
- `allowed_zone`: represents the coordinates of the corners of the allowed zone for the agent. In fact, the green agent can only move in the green zone, the yellow agent can move in the green and the yellow zones, and finally the red agent can move in all 3 zones.
- `actions`: represents the list of actions
- `reset_zone`: ...
- `model_config`: ...

### Strategy 2 : Agents with communication

.....


### Strategy 3 : Agents with advanced communication

.....

## Results
- to run the simulations, we chose a `batch_size` of 3 in order to take into account the fact the randomness in the placement of the waste as well as the potential randomness in the chosen strategy. so the différence in results may be due to randomness
- show table



## Limits & Improvements
- fixed grid size
- batch size is low, keep the variance high
- we can implement and monitor other KPIs, notably the time an agent spent not doing anything. In fact, it depends on our purpose: do we want to clean the map fast or do we want to clean it fast and also not use a lot of energy..
- same number of waste in the 3 regions. the red one is always loaded compared to the other two


## Contributors

- Ammar Mariem
- Ben Younes Lina
- Bouhadida Malek