import solara
import matplotlib.pyplot as plt
from mesa.visualization import make_space_component, SolaraViz
from mesa.visualization.utils import update_counter
from model import RobotMission
from agents import greenAgent, yellowAgent, redAgent
from objects import Radioactivity, WasteDisposalZone, Waste
from matplotlib.ticker import MaxNLocator
    
    
## Visualisation des agents
def agent_portrayal(agent): 
    
    if isinstance(agent, Radioactivity):
        color = {"green": "#C7F6C7", "yellow": "#FFFDD0", "red": "#F19396"}[agent.color]
        return {"size": 1100, "color": color, "marker": "s", "zorder": 0}
    
    elif isinstance(agent, (greenAgent, yellowAgent, redAgent)):
        color_map = {
            greenAgent: "#00C000",
            yellowAgent: "#F6C324",
            redAgent: "#E32227"
        }
        return {"size": 800, "color": color_map[type(agent)], "marker": ".", "zorder": 1}
    elif isinstance(agent, WasteDisposalZone):
        
        return {"size": 1100, "color": "black", "marker": "s", "zorder": 1}
    elif isinstance(agent, Waste):
        
        color = {"green": "#2FF924", "yellow": "#AC9F3C", "red": "#EB212E"}[agent.radioactivity_level]
        return {"size": 60, "color": color, "marker": "s", "zorder": 1}
    else:
        raise Exception(f"Unknown Object {type(agent)}")






## Courbe de suivi des déchets
@solara.component
def WasteSinglePlot(model, color: str, label: str, line_color: str):
    
    update_counter.get()
    if model is None:
        return solara.Text("Modèle non chargé.")
    
    df = model.datacollector.get_model_vars_dataframe()
    if df.empty or f"Left_waste_{color}" not in df.columns:
        return solara.Text(f"Pas encore de données pour {label}.")

    fig, ax = plt.subplots()
    ax.plot(df.index, df[f"Left_waste_{color}"], label=label, color=line_color,linewidth=3.5)
    ax.set_title(f"{label} over time",fontsize=30)
    ax.set_xlabel("Step")
    ax.set_ylabel("Quantité")
    ax.tick_params(axis='both', labelsize=20)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend()
    ax.grid(True)

    return solara.FigureMatplotlib(fig)


## Courbe de suivi du déchet neutralisé
@solara.component
def WasteDisposedPlot(model):
    
    update_counter.get()
    if model is None:
        return solara.Text("Modèle non chargé.")

    df = model.datacollector.get_model_vars_dataframe()
    if df.empty or "Total_waste_disposed" not in df.columns:
        return solara.Text("Pas encore de données.")

    fig, ax = plt.subplots()
    ax.plot(df.index, df["Total_waste_disposed"], label="Disposed", color="black",linewidth=3.5)
    ax.set_title("Total_waste_disposed",fontsize=30)
    ax.set_xlabel("Step")
    ax.set_ylabel("Quantité")
    ax.tick_params(axis='both', labelsize=20)
    ax.legend()
    ax.grid(True)

    return solara.FigureMatplotlib(fig)

## Plot de suivi des 4 métriques
@solara.component
def WastePlotsAll(model):
    
    with solara.GridFixed(columns=2):
        with solara.Card(elevation=0, margin=-2):  
            WasteSinglePlot(model, "green", "Green Waste", "green")
        with solara.Card(elevation=0, margin=-2):
            WasteSinglePlot(model, "yellow", "Yellow Waste", "#DAA520")
        with solara.Card(elevation=0, margin=-2):
            WasteSinglePlot(model, "red", "Red Waste", "red")
        with solara.Card(elevation=0, margin=-2):
            WasteDisposedPlot(model)
       

## Page principale avec panneau gauche customisé
@solara.component
def Page():
    
    n_g = solara.use_reactive(1)
    n_y = solara.use_reactive(1)
    n_r = solara.use_reactive(1)
    n_waste = solara.use_reactive(12)

    # Paramètres pour le modèle
    model_params = {
        "n_g": n_g,
        "n_y": n_y,
        "n_r": n_r,
        "n_waste": n_waste
    }

    model = solara.use_memo(lambda: RobotMission(
        n_g.value, n_y.value, n_r.value, n_waste.value, 12, 12
    ), [n_g.value, n_y.value, n_r.value, n_waste.value, 12, 12])
    
    plt.rcParams["figure.figsize"] = (7, 7)  
    SpaceGraph = make_space_component(agent_portrayal)

    with solara.Columns([3, 9]):
        with solara.Column():
            solara.Markdown("### Model Parameters")
            solara.SliderInt("green agents", value=n_g, min=0, max=10)
            solara.SliderInt("yellow agents", value=n_y, min=0, max=10)
            solara.SliderInt("red agents", value=n_r, min=0, max=10)
            solara.SliderInt("number of waste", value=n_waste, min=0, max=50)

        with solara.Column():
            solara.Markdown("<h3 style='text-align: center;'> Spatial and Temporal Dynamics </h3>")
            SolaraViz(
                model,
                model_params={key: val.value for key, val in model_params.items()},
                components=[SpaceGraph, WastePlotsAll],
                name="Self-organization of Robots in a Hostile Environment",
            )