import random
from global_vars import TRAIT
from cell import Cell


class Pacman:
    """
    Pacman class encompasses a single being in the macpan universe, capable of moving, reproducing, sharing, having people issues, has hunger, knows to obtain food and can die.
    """

    def __init__(self, starting_food, trait, x_cord, y_cord, init_dict):
        self.init_dict = init_dict
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.food = starting_food
        self.trait = trait
        self.direction = random.randint(1, 4)
        if self.trait == TRAIT.TITFORTAT:
            self.history = random.choice([True, False])
        elif self.trait == TRAIT.GRATEFUL:
            self.history = True

    def move(self, m, n):
        # defines movement of pacman
        # 1 = up, 2 = down, 3 = left, 4 = right
        # direction = random.randint(1, 4)
        if self.direction == 1:
            self.y_cord = (self.y_cord + 1) % m

        elif self.direction == 2:
            self.y_cord = (self.y_cord - 1) % m

        elif self.direction == 3:
            self.x_cord = (self.x_cord - 1) % n

        elif self.direction == 4:
            self.x_cord = (self.x_cord + 1) % n

    def reproduce(self, cell: Cell):
        # pacman reproduce if it's food count become greater than reproduction_thresh
        daughter = Pacman(
            starting_food=self.food // 2,
            trait=self.trait,
            x_cord=self.x_cord,
            y_cord=self.y_cord,
            init_dict=self.init_dict,
        )
        if self.direction == 1:
            daughter.direction = 2
        elif self.direction == 2:
            daughter.direction = 1
        elif self.direction == 3:
            daughter.direction = 4
        elif self.direction == 4:
            daughter.direction = 3

        self.food = self.food // 2
        cell.pacmen[self.trait].append(daughter)

    def share(self):
        if self.trait == TRAIT.UNGRATEFUL:
            return 0
        else:
            willHelp = self.history
            excess = self.food - self.init_dict["charity_thresh"]
            if willHelp and excess > 0:
                excess = self.food - self.init_dict["charity_thresh"]
                food_shared = min(excess, self.init_dict["num_food_excess_given"])
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
        self.food -= self.init_dict["ghost_tax"]

    def refill(self, amount: int):
        # increase the pacmen food count by the amount of food found
        self.food += amount
        # self.food = self.init_dict["charity_thresh"]
        # self.food = self.init_dict["reproduction_thresh"]
        # self.food += self.food

    def die(self, cell: Cell):
        cell.pacmen[self.trait].remove(self)
        del self

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
