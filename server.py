import mesa
import solara
from matplotlib.figure import Figure
from mesa.visualization import SolaraViz, make_plot_component, make_space_component
from mesa.visualization.utils import update_counter
from model import RobotMission
from agents import greenAgent, yellowAgent, redAgent
from objects import Radioactivity, WasteDisposalZone, Waste
import matplotlib.pyplot as plt


def agent_portrayal(agent): 
    
    if isinstance(agent, Radioactivity):
        if agent.color == "green":
            color = "#C7F6C7" 
        elif agent.color == "yellow":
            color = "#FFFDD0" 
        elif agent.color == "red":
            color = "#F19396" 
        size = 1650
        marker = "s"
        zorder = 0  # to put it behind the other agents/objects

    elif isinstance(agent, greenAgent):
        color = "#00C000" 
        size = 800
        marker = "."
        zorder = 1

    elif isinstance(agent, yellowAgent):
        color = "#F6C324" 
        size = 800
        marker = "."
        zorder = 1  

    elif isinstance(agent, redAgent):
        color = "#E32227" 
        size = 800
        marker = "."
        zorder = 1  

    elif isinstance(agent, WasteDisposalZone):
        color = "black" 
        size = 1650
        marker = "s"
        zorder = 1 
    
    elif isinstance(agent, Waste):
        radioactivity_level = agent.radioactivity_level
        if radioactivity_level=='green':
            color = "#2FF924"
        if radioactivity_level=='yellow':
            color = "#AC9F3C"
        if radioactivity_level=='red':
            color = "#EB212E"
        size = 60
        marker = "s"
        zorder = 1 
    
    else:
        raise Exception(f"Unknown Object {type(agent)}")

    return {"size": size, "color": color, "marker": marker, "zorder": zorder}


model_params = {
    "n_g": 1,
    "n_y": 1,
    "n_r": 1,
    "n_waste": 12,
    "width": 10,
    "height": 10,
}


model = RobotMission(1,1,1,12,10,10)

plt.rcParams["figure.figsize"] = (8, 8)
SpaceGraph = make_space_component(agent_portrayal)

# Dashboard
page = SolaraViz(
    model,
    components=[SpaceGraph],
    model_params=model_params,
    name="Self-organization of Robots in a Hostile Environment",
)


# to start : "solara run server.py"
