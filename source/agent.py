from mesa import Agent
from random import randint
from math import sin, cos, floor

MAX_DISPERSION = 5
class TreeCell(Agent):
    def __init__(self, pos, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                will_get_fire = randint(1, 100) < self.model.intensity
                if neighbor.condition == "Fine" and will_get_fire:
                    neighbor.condition = "On Fire"
                elif neighbor.condition == "Secondary Flame":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"

            if (
                randint(1, 100) >= self.model.intensity / 4
                or self.model.wind_speed == 0
            ):
                return

            dispersion_distance = randint(1, self.model.wind_speed) * MAX_DISPERSION
            x, y = self.pos
            x += sin(self.model.wind_direction) * dispersion_distance
            y += cos(self.model.wind_direction) * dispersion_distance
            x, y = floor(x), floor(y)
            if 0 <= x <= self.model.grid.width and 0 <= y <= self.model.grid.height:
                try:
                    tree = self.model.grid[x][y]
                    if tree and tree.condition == "Fine":
                        self.model.secondary_flame_count += 1
                        tree.condition = "Secondary Flame"
                except:
                    pass

        if self.condition == "Secondary Flame":
            self.model.secondary_flame_count += 1
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fine" and randint(1, 10) < self.model.wind_speed:
                    neighbor.condition = "Secondary Flame"
            self.condition = "Burned Out"
