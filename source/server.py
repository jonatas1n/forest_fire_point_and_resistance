from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFire

COLORS = {
    "Fine": "#00AA00",
    "On Fire": "#880000",
    "Burned Out": "#000000",
    "Escaped the Fire": "#f6781d",
}


def forest_fire_portrayal(tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]
    return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)

tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
escaped_chart = ChartModule([{"Label": "Escaped the Fire", "Color": "#f6781d"}])
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    "start_pos_x": UserSettableParameter(
        "slider", "X Point of Fire Start", 50, 1, 100, 1
    ),
    "start_pos_y": UserSettableParameter(
        "slider", "Y Point of Fire Start", 50, 1, 100, 1
    ),
    "intensity": UserSettableParameter("slider", "Fire Intensity", 80, 1, 100, 1),
}
server = ModularServer(
    ForestFire,
    [canvas_element, tree_chart, escaped_chart, pie_chart],
    "Forest Fire",
    model_params,
)
