from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agent import TreeCell


class ForestFireResistance(Model):
    """
    Simple Forest Fire model.
    """
    
    last_escaped_tax = 0
    def __init__(self, width=100, height=100, density=0.65, start_pos_x=0, start_pos_y=0, intensity=80):
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
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.intensity = intensity

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Escaped the Fire": lambda m: self.count_type(m, "Escaped the Fire"),
                "Escaped Tax": lambda m: self.escaped_tax(m),
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self, intensity)
                # Set all trees in the first column on fire.
                if x >= start_pos_x + - 1 and x <= start_pos_x + 1  and y >= start_pos_y + -1 and y <= start_pos_y + 1:
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
        if self.count_type(self, "On Fire") == 0:
            self.running = False
            forest_model = self.datacollector.get_model_vars_dataframe()
            forest_model.to_csv('forest_model_density_' + str(self.density) + '_start-pos-x_' + str(self.start_pos_x) + '_start-pos-y_' + str(self.start_pos_y) + '.csv')

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        agents = model.schedule.agents
        return len([tree for tree in agents if tree.condition == tree_condition])

    @staticmethod
    def escaped_tax(model):
        escaped_tax = model.count_type(model, "Escaped the Fire")
        escaped_tax -= model.last_escaped_tax
        model.last_escaped_tax = escaped_tax
        return escaped_tax
