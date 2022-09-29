from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFireResistance

COLORS = {
    "Fine": "#00AA00",
    "On Fire": "#880000",
    "Burned Out": "#000000",
    "Secondary Flame": "#f6781d",
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
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

secondary_flame_chart = ChartModule([{"Label": "Secondary flame", "Color": "#f6781d"}])

model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    "intensity": UserSettableParameter("slider", "Fire Intensity", 80, 1, 100, 1),
    "wind_speed": UserSettableParameter("slider", "Wind Speed", 5, 0, 10, 1),
}

server = ModularServer(
    ForestFireResistance,
    [canvas_element, tree_chart, pie_chart],
    "Forest Fire",
    model_params,
)
