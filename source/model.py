from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agent import TreeCell


class ForestFireResistance(Model):
    """
    Simple Forest Fire model.
    """

    secondary_flame_count = 0
    wind_direction = 90

    def __init__(
        self,
        width=100,
        height=100,
        density=0.5,
        intensity=80,
        wind_speed=5
    ):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)
        self.density = density
        self.intensity = intensity
        self.wind_speed = wind_speed

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Secondary Flame": lambda m: self.count_type(m, "Secondary Flame"),
                "Secondary Flame Count": lambda m: self.secondary_flame_count,
            }
        )

        # Place a tree in each cell with Prob = density
        for (_, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self, intensity)
                if (49 <= x <= 51 and 49 <= y <= 51 ):
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") + self.count_type(self, "Secondary Flame") == 0:
            self.running = False
            self.datacollector.collect(self)

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        agents = model.schedule.agents
        return len([tree for tree in agents if tree.condition == tree_condition])