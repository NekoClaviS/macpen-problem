import numpy as np
from cell import Cell
from pacman import Pacman
from global_vars import TRAIT


class Grid:
    def __init__(self, init_dict):
        self.init_dict = init_dict
        self.rows = self.init_dict["rows"]
        self.cols = self.init_dict["cols"]
        self.num_canteens = self.init_dict["num_canteens"]
        self.canteen_life = self.init_dict["canteen_life"]
        self.ghost_tax = self.init_dict["ghost_tax"]
        self.canteen_food_packet = self.init_dict["canteen_food_packet"]
        self.grid = np.zeros((self.init_dict["rows"], self.init_dict["cols"]))
        self.cells = []
        for i in range(self.rows * self.cols):
            row = i // self.cols
            col = i % self.cols
            self.cells.append(Cell(row, col, [], [], [], init_dict))

    def spawn_canteen(self, num_canteens):
        """
        randomly generate canteens in the grid
        """
        self.grid = np.zeros((self.rows, self.cols))
        row_indices = np.random.randint(0, self.rows, num_canteens)
        col_indices = np.random.randint(0, self.cols, num_canteens)
        for idx in range(num_canteens):
            self.grid[row_indices[idx]][col_indices[idx]] = 1

    def display(self):
        g_mat = np.zeros((self.rows, self.cols))
        u_mat = np.zeros((self.rows, self.cols))
        t_mat = np.zeros((self.rows, self.cols))
        tot_mat = [[0 for _ in range(self.cols)] for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i * self.cols + j]
                g, u, t = cell.get_population()
                g_mat[i][j] = g
                u_mat[i][j] = u
                t_mat[i][j] = t
                tot_mat[i][j] = g + u + t
        return (g_mat, u_mat, t_mat, tot_mat)

    def __str__(self) -> str:
        return str(self.grid)


if __name__ == "__main__":
    grid = Grid()
    print(len(grid.cells[0].pacman_in_cell))
    grid.spawn_canteen()
    print(grid)
