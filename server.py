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
    "n_waste": 48,
    "width": 12,
    "height": 12,
}


model = RobotMission(n_g=model_params["n_g"],
             n_y=model_params["n_y"],
             n_r=model_params["n_r"],
             n_waste=model_params["n_waste"],
             width=model_params["width"],
             height=model_params["height"],
             seed=None, strategy=3)

plt.rcParams["figure.figsize"] = (7, 7)
SpaceGraph = make_space_component(agent_portrayal)
TotalWasteDisposedPlot = make_plot_component("Total_waste_disposed")
# GreenWasteLeftPlot = make_plot_component("Left_waste_green")


# Dashboard
page = SolaraViz(
    model,
    components=[SpaceGraph, TotalWasteDisposedPlot],
    model_params=model_params,
    name="Self-organization of Robots in a Hostile Environment",
)


# to start : "solara run server.py"
