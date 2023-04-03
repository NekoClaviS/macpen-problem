from global_vars import TRAIT
import numpy as np


class Cell:
    def __init__(
        self,
        cell_x_cord,
        cell_y_cord,
        g_population,
        u_population,
        t_population,
        init_dict,
    ):
        self.init_dict = init_dict
        self.x = cell_x_cord  # x_co-ordinate of cell
        self.y = cell_y_cord  # y_co-ordinate of cell
        self.pacmen = {
            TRAIT.GRATEFUL: g_population,
            TRAIT.UNGRATEFUL: u_population,
            TRAIT.TITFORTAT: t_population,
        }
        self.near_death_pacman = []
        self.food_pool = 0

    # define contri/distribution function
    def contri(self):
        """
        Make a pool of food available in the cell and store it in a variable.
        Make a sorted list (descending) of near death pacmen.
        While loop to give minimum survival food to all possible pacmen, until a
        case comes where food given to a pacman doesn't help it survive,
        that food will then be distributed equally to other surviving pacmen
        """
        # Finding out all near death pacman by food-self.init_dict["ghost_tax"] < 0
        flag = False
        self.near_death_pacman = []
        self.food_pool = 0  # for edge case handling

        for trait in TRAIT:
            for pacman in self.pacmen[trait]:
                flag = True
                if (pacman.food - self.init_dict["ghost_tax"]) < 0:
                    self.near_death_pacman.append(pacman)

        if not flag:  # for condition with no pacmen in cell
            return

        if len(self.near_death_pacman) == 0:
            # no one is dying
            return

        self.near_death_pacman.sort(
            key=lambda x: x.food - self.init_dict["ghost_tax"], reverse=True
        )

        helped_by = 0
        for trait in TRAIT:
            for pacman in self.pacmen[trait]:
                food_shared = pacman.share()
                if food_shared > 0:
                    helped_by += 1
                    self.food_pool += food_shared

        if helped_by == 0:
            # no one to help
            for pacman in self.near_death_pacman:
                pacman.history = False
            return

        total_healthy = (
            len(self.pacmen[TRAIT.GRATEFUL])
            + len(self.pacmen[TRAIT.UNGRATEFUL])
            + len(self.pacmen[TRAIT.TITFORTAT])
            - len(self.near_death_pacman)
        )

        ratio_helped = helped_by / total_healthy

        counter = 0
        willHelp = np.random.binomial(1, ratio_helped, len(self.near_death_pacman))
        for i, pacman in enumerate(self.near_death_pacman):
            if self.food_pool < self.init_dict["ghost_tax"] - pacman.food:
                break
            pacman.food = self.init_dict["ghost_tax"]
            self.food_pool -= self.init_dict["ghost_tax"] - pacman.food
            if pacman.trait == TRAIT.TITFORTAT:
                pacman.update_history(willHelp[i])
            counter += 1

        if counter == 0:
            return

        share_size = self.food_pool // counter
        excess = self.food_pool % counter
        for pacman in self.near_death_pacman[:counter]:
            self.food_pool -= share_size
            pacman.food += share_size
            self.food_pool -= share_size
            if excess > 0:
                excess -= 1
                pacman.food += 1
                self.food_pool -= 1

        # handled food handling of near dying pacmen, and restructured other pacmen's food

    def get_population(self):
        return (
            len(self.pacmen[TRAIT.GRATEFUL]),
            len(self.pacmen[TRAIT.UNGRATEFUL]),
            len(self.pacmen[TRAIT.TITFORTAT]),
        )

    def __str__(self) -> str:
        return str(
            {
                "location": (self.x, self.y),
                "g_population": len(self.pacmen[TRAIT.GRATEFUL]),
                "u_population": len(self.pacmen[TRAIT.UNGRATEFUL]),
                "t_population": len(self.pacmen[TRAIT.TITFORTAT]),
            }
        )
