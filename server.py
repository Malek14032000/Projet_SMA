import solara
import matplotlib.pyplot as plt
from mesa.visualization import make_space_component, SolaraViz
from mesa.visualization.utils import update_counter
from model import RobotMission
from agents import greenAgent, yellowAgent, redAgent
from objects import Radioactivity, WasteDisposalZone, Waste

# === Visualisation des agents ===
def agent_portrayal(agent): 
    if isinstance(agent, Radioactivity):
        color = {"green": "#C7F6C7", "yellow": "#FFFDD0", "red": "#F19396"}[agent.color]
        return {"size": 1650, "color": color, "marker": "s", "zorder": 0}
    elif isinstance(agent, (greenAgent, yellowAgent, redAgent)):
        color_map = {
            greenAgent: "#00C000",
            yellowAgent: "#F6C324",
            redAgent: "#E32227"
        }
        return {"size": 800, "color": color_map[type(agent)], "marker": ".", "zorder": 1}
    elif isinstance(agent, WasteDisposalZone):
        return {"size": 1650, "color": "black", "marker": "s", "zorder": 1}
    elif isinstance(agent, Waste):
        color = {"green": "#2FF924", "yellow": "#AC9F3C", "red": "#EB212E"}[agent.radioactivity_level]
        return {"size": 60, "color": color, "marker": "s", "zorder": 1}
    else:
        raise Exception(f"Unknown Object {type(agent)}")

# === Courbe de suivi des déchets ===
@solara.component
def WastePlot(model):
    update_counter.get()
    if model is None:
        return solara.Text("Modèle non chargé.")
    df = model.datacollector.get_model_vars_dataframe()
    if df.empty:
        return solara.Text("Pas encore de données.")
    
    fig, ax = plt.subplots()
    if "Left_waste_green" in df.columns:
        ax.plot(df.index, df["Left_waste_green"], label="Green Waste", color="green")
    if "Left_waste_yellow" in df.columns:
        ax.plot(df.index, df["Left_waste_yellow"], label="Yellow Waste", color="gold")
    if "Left_waste_red" in df.columns:
        ax.plot(df.index, df["Left_waste_red"], label="Red Waste", color="red")
    if "Total_waste_disposed" in df.columns:
        ax.plot(df.index, df["Total_waste_disposed"], label="Disposed", color="black", linestyle="--")

    ax.set_title("Évolution des déchets")
    ax.set_xlabel("Step")
    ax.set_ylabel("Quantité")
    ax.legend()
    ax.grid(True)

    return solara.FigureMatplotlib(fig)

# === Page principale avec panneau gauche custom ===
@solara.component
def Page():
    # Sliders réactifs
    n_g = solara.use_reactive(1)
    n_y = solara.use_reactive(1)
    n_r = solara.use_reactive(1)
    n_waste = solara.use_reactive(12)
    width = solara.use_reactive(9)
    height = solara.use_reactive(9)

    # Paramètres pour le modèle
    model_params = {
        "n_g": n_g,
        "n_y": n_y,
        "n_r": n_r,
        "n_waste": n_waste,
        "width": width,
        "height": height,
    }

    model = solara.use_memo(lambda: RobotMission(
        n_g.value, n_y.value, n_r.value, n_waste.value, width.value, height.value
    ), [n_g.value, n_y.value, n_r.value, n_waste.value, width.value, height.value])

    SpaceGraph = make_space_component(agent_portrayal)

    with solara.Columns([3, 9]):
        with solara.Column():
            solara.Markdown("### Model Parameters")
            solara.SliderInt("Agents verts", value=n_g, min=0, max=10)
            solara.SliderInt("Agents jaunes", value=n_y, min=0, max=10)
            solara.SliderInt("Agents rouges", value=n_r, min=0, max=10)
            solara.SliderInt("Nombre de déchets", value=n_waste, min=0, max=50)
            solara.SliderInt("Largeur de la grille", value=width, min=5, max=20)
            solara.SliderInt("Hauteur de la grille", value=height, min=5, max=20)

        with solara.Column():
            solara.Markdown("### Simulation")
            SolaraViz(
                model,
                model_params={key: val.value for key, val in model_params.items()},
                components=[SpaceGraph, WastePlot],
                name="Self-organization of Robots in a Hostile Environment",
            )





