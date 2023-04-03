import random
import numba
import numpy as np
from global_vars import (
    TRAIT,
    reproduction_thresh,
    charity_thresh,
    num_food_excess_given,
    ghost_tax,
    starting_food,
    rows, cols
)
from cell import Cell


class Pacman:
    """
    Pacman class encompasses a single being in the macpan universe, capable of moving, reproducing, sharing, having people issues, has hunger, knows to obtain food and can die.
    """

    def __init__(self, starting_food, trait, x_cord, y_cord):
        numba.types.int32
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.food = starting_food
        self.trait = trait
        if self.trait == TRAIT.TITFORTAT:
            self.history = random.choice([True, False])
        elif self.trait == TRAIT.GRATEFUL:
            self.history = True

    def move(self, m, n):
        """
        defines movement of pacman
        1 = up, 2 = down, 3 = left, 4 = right
        """
        direction = random.randint(1, 4)
        if direction == 1:
            self.y_cord = (self.y_cord + 1) % m

        if np.random.uniform() > 0.5 and del_x != 0:
            self.x_cord = (self.x_cord + del_x) % m
        elif del_y != 0:
            self.y_cord = (self.y_cord + del_y) % n

    def reproduce(self, cell: Cell):
        """
        pacman reproduce if it's food count become greater than reproduction_thresh
        """
        daughter = Pacman(
            starting_food=self.food // 2,
            trait=self.trait,
            x_cord=self.x_cord,
            y_cord=self.y_cord,
        )
        self.food = self.food // 2
        cell.pacmen[self.trait].append(daughter)

    def share(self):
        """
        Share food available according to availability
        """
        if self.trait == TRAIT.UNGRATEFUL:
            return 0
        else:
            willHelp = self.history
            excess = self.food - charity_thresh
            if willHelp and excess > 0:
                excess = self.food - charity_thresh
                food_shared = min(excess, num_food_excess_given)
                self.food -= food_shared
                return food_shared
            else:
                return 0

    def update_history(self, received: bool):
        if received:
            self.history = True  # had faced gratefulness
        else:
            self.history = False

    def consume_ghost_tax(self):
        """
        deduct a certain amount of food(ghost_tax) from all the pacman at the end of each day
        """
        self.food -= ghost_tax

    def refill(self, amount: int):
        """
        increase the pacmen food count by the amount of food found
        """
        NORMAL_FILLING = True
        COMMUNISM_LOW_RESOURCES = False
        COMMUNISM = False
        LEFT_RIGHT = False
        if NORMAL_FILLING:
            self.food += amount
        elif COMMUNISM_LOW_RESOURCES:
            self.food = self.init_dict["charity_thresh"]
        elif COMMUNISM:
            self.food = self.init_dict["reproduction_thresh"]
        elif LEFT_RIGHT:
            if self.x_cord > self.init_dict["cols"] / 2:
                self.food += 2 * self.food
            else:
                self.food = self.init_dict["reproduction_thresh"]

    def die(self, cell: Cell):
        cell.pacmen[self.trait].remove(self)
        del self

    def kill(self, pacman, cell: Cell):
        self.food += int(pacman.food / 2)
        # pacman.die(cell)

    def __str__(self) -> str:
        return str(
            {
                "food": self.food,
                "trait": self.trait,
                "location": (self.x_cord, self.y_cord),
                "history": self.history,
            }
        )


if __name__ == "__main__":
    pacman = Pacman(6, TRAIT.TITFORTAT, 3, 4)
    print(pacman)
    pacman.move(10, 10)  # check movement
    print(pacman)
    inCell = Cell(pacman.x_cord, pacman.y_cord)
    pacman.share()
    print(pacman)
    pacman.update_history(True)
    print(pacman)
    pacman.consume_ghost_tax()
    print(pacman)
    pacman.refill(69, inCell)
    print(inCell)
    print(inCell)
