from grid import Grid
from pacman import Pacman
import numpy as np
from global_vars import TRAIT


class Time:
    """
    time object acting as control flow of the entire simulation
    """

    def __init__(self, init_dict):
        """format of init_dict
        init_dict = {
            "rows": rows,
            "cols": cols,
            "num_pacmen": num_pacmen,
            "ghost_tax": ghost_tax,
            "num_canteens": num_canteens,
            "num_food_excess_given": num_food_excess_given,
            "canteen_life": canteen_life,
            "canteen_food_packet": canteen_food_packet,
            "g_percent": g_percent,
            "u_percent": u_percent,
            "t_percent": t_percent,
            "starting_food": starting_food,
        }
        """
        self.day = 1
        self.init_dict = init_dict
        # self.cells = [[self.Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.grid = Grid(self.init_dict)
        self.grid.spawn_canteen(init_dict["num_canteens"])

        self.u = int(self.init_dict["u_percent"]
                     * self.init_dict["num_pacmen"])
        self.g = int(self.init_dict["g_percent"]
                     * self.init_dict["num_pacmen"])
        self.t = int(self.init_dict["t_percent"]
                     * self.init_dict["num_pacmen"])

        # generate u population and put them into their own cells
        row_indices = np.random.randint(0, self.grid.rows, self.u)
        col_indices = np.random.randint(0, self.grid.cols, self.u)
        for i in range(self.u):
            new = Pacman(
                starting_food=self.init_dict["starting_food"],
                trait=TRAIT.UNGRATEFUL,
                x_cord=row_indices[i],
                y_cord=col_indices[i],
                init_dict=self.init_dict,
            )
            idx = row_indices[i] * self.grid.cols + col_indices[i]
            self.grid.cells[idx].pacmen[TRAIT.UNGRATEFUL].append(new)

        # generate g population and put them into their own cells
        row_indices = np.random.randint(0, self.grid.rows, self.g)
        col_indices = np.random.randint(0, self.grid.cols, self.g)
        for i in range(self.g):
            new = Pacman(
                starting_food=self.init_dict["starting_food"],
                trait=TRAIT.GRATEFUL,
                x_cord=row_indices[i],
                y_cord=col_indices[i],
                init_dict=self.init_dict,
            )
            idx = row_indices[i] * self.grid.cols + col_indices[i]
            self.grid.cells[idx].pacmen[TRAIT.GRATEFUL].append(new)

        # generate t population and put them into their own cells
        row_indices = np.random.randint(0, self.grid.rows, self.t)
        col_indices = np.random.randint(0, self.grid.cols, self.t)
        for i in range(self.t):
            new = Pacman(
                starting_food=self.init_dict["starting_food"],
                trait=TRAIT.TITFORTAT,
                x_cord=row_indices[i],
                y_cord=col_indices[i],
                init_dict=self.init_dict,
            )
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
        spawn canteens at random locations in the grid after self.init_dict["canteen_life"]
        """
        food_final_list = []
        if (self.day % self.init_dict["canteen_life"]) == 0:
            self.grid.spawn_canteen(
                self.init_dict["num_canteens"])  # update canteens
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                idx = i * self.grid.cols + j
                cell = self.grid.cells[idx]  # iterate through each cell
                for trait in cell.pacmen.keys():
                    # iterate through each pacmen
                    for pacman in cell.pacmen[trait]:
                        if self.grid.grid[i][j] == 1:
                            pacman.refill(
                                self.init_dict["canteen_food_packet"]
                            )  # refill

                for trait in TRAIT:
                    for pacman in cell.pacmen[trait]:
                        if pacman.food >= self.init_dict["reproduction_thresh"]:
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
                            pacman.move(self.grid.rows, self.grid.cols)  # move
                            newIdx = pacman.x_cord * self.grid.cols + pacman.y_cord
                            self.grid.cells[newIdx].pacmen[pacman.trait].append(
                                pacman
                            )

                        food_final_list = food_final_list + cell.get_pacmen_food()
        self.day += 1
        return food_final_list  # add on the new cel
