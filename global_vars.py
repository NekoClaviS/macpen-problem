from enum import Enum


class TRAIT(Enum):
    GRATEFUL = 69
    UNGRATEFUL = -69
    TITFORTAT = 0


rows = 10
cols = 10
num_canteens = 10  #!
canteen_life = 4  #!
ghost_tax = 1
canteen_food_packet = 6  #!
charity_thresh = 5  #!
reproduction_thresh = 10  #!
num_food_excess_given = 3
starting_food = 4
num_pacmen = 1000
u_percent = 0.33
g_percent = 0.33
t_percent = 1 - u_percent - g_percent

possible_num_canteens = [1, 4, 20]
possible_canteen_life = [1, 4, 256]

possible_canteen_food_packet = [5, 20]
possible_num_pacmen = [1, 10, 1000]
possible_charity_thresh = [5, 20]
possible_reproduction_thresh = [10, 40]
possible_g_percent = [0.1, 0.333, 0.8]
possible_u_percent = [0.8, 0.333, 0.1]
possible_t_percent = [1 - x - y for x, y in zip(possible_g_percent, possible_u_percent)]

init_dict = {
    "rows": rows,
    "cols": cols,
    "num_pacmen": num_pacmen,
    "ghost_tax": ghost_tax,
    "num_canteens": num_canteens,
    "num_food_excess_given": num_food_excess_given,
    "canteen_life": canteen_life,
    "canteen_food_packet": canteen_food_packet,
    "g_per": g_percent,
    "u_per": u_percent,
    "t_per": t_percent,
    "starting_food": starting_food,
}
