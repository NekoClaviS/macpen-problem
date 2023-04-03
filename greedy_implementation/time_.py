from grid import Grid
from pacman import Pacman
import math
import numba
import numpy as np
from global_vars import (
    reproduction_thresh,
    num_pacmen,
    num_canteens,
    u_percent,
    g_percent,
    t_percent,
    starting_food,
    TRAIT,
    canteen_life,
    canteen_food_packet,
    ghost_tax,
)


class Time:
    """
    time object acting as control flow of the entire simulation
    """

    def __init__(self, init_dict):
        self.day = 1
        # self.cells = [[self.Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.grid = Grid(init_dict=init_dict)
        self.grid.spawn_canteen(num_canteens)

        self.u = int(u_percent * num_pacmen)
        self.g = int(g_percent * num_pacmen)
        self.t = int(t_percent * num_pacmen)

        # generate u population and put them into their own cells
        row_indices = np.random.randint(0, self.grid.rows, self.u)
        col_indices = np.random.randint(0, self.grid.cols, self.u)
        for i in range(self.u):
            new = Pacman(
                starting_food, TRAIT.UNGRATEFUL, row_indices[i], col_indices[i]
            )
            idx = row_indices[i] * self.grid.cols + col_indices[i]
            self.grid.cells[idx].pacmen[TRAIT.UNGRATEFUL].append(new)

        # generate g population and put them into their own cells
        row_indices = np.random.randint(0, self.grid.rows, self.g)
        col_indices = np.random.randint(0, self.grid.cols, self.g)
        for i in range(self.g):
            new = Pacman(starting_food, TRAIT.GRATEFUL,
                         row_indices[i], col_indices[i])
            idx = row_indices[i] * self.grid.cols + col_indices[i]
            self.grid.cells[idx].pacmen[TRAIT.GRATEFUL].append(new)

        # generate t population and put them into their own cells
        row_indices = np.random.randint(0, self.grid.rows, self.t)
        col_indices = np.random.randint(0, self.grid.cols, self.t)
        for i in range(self.t):
            new = Pacman(starting_food, TRAIT.TITFORTAT,
                         row_indices[i], col_indices[i])
            idx = row_indices[i] * self.grid.cols + col_indices[i]
            self.grid.cells[idx].pacmen[TRAIT.TITFORTAT].append(new)

    def get_population(self):
        """
        Iterate through all the cells in the grid and count the population of each type of pacman
        """
        u = g = t = 0
        for cell in self.grid.cells:
            u += len(cell.pacmen[TRAIT.UNGRATEFUL])
            g += len(cell.pacmen[TRAIT.GRATEFUL])
            t += len(cell.pacmen[TRAIT.TITFORTAT])
        return (g, u, t, g + u + t)

    def update(self):
        """
        spawn canteens at random locations in the grid after canteen_life
        """
        if (self.day % canteen_life) == 0:
            self.grid.spawn_canteen(num_canteens)  # update canteens
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                idx = i * self.grid.cols + j
                cell = self.grid.cells[idx]  # iterate through each cell
                for trait in cell.pacmen.keys():
                    # iterate through each pacmen
                    for pacman in cell.pacmen[trait]:
                        if self.grid.grid[i][j] == 1:
                            pacman.refill(canteen_food_packet)  # refill

                for trait in TRAIT:
                    for pacman in cell.pacmen[trait]:
                        if pacman.food >= reproduction_thresh:
                            pacman.reproduce(cell)

                cell.contri()  # contri of the cell

                for trait in cell.pacmen.keys():
                    for pacman in cell.pacmen[trait]:
                        pacman.consume_ghost_tax()
                        if pacman.food < 0:
                            pacman.die(cell)
                        else:
                            idx = i * self.grid.cols + j
                            self.grid.cells[idx].pacmen[pacman.trait].remove(
                                pacman
                            )  # remove from present cell
                            pacman.move(self.grid.rows,
                                        self.grid.cols, self.grid)  # move
                            newIdx = pacman.x_cord * self.grid.cols + pacman.y_cord
                            self.grid.cells[newIdx].pacmen[pacman.trait].append(
                                pacman
                            )  # add on the new cell
        self.day += 1


if __name__ == "__main__":
    step = Time(
        m=10, n=10, num_canteens=5, canteen_life=4, canteen_food_packet=6, ghost_tax=1
    )
