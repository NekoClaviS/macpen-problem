from time_ import Time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
from global_vars import *
from experiments import simulate_heatmap

iterate = 10
day_max = 25

strategy = "religion"

init_dict = {
    "rows": rows,
    "cols": cols,
    "num_pacmen": num_pacmen,
    "ghost_tax": ghost_tax,
    "num_canteens": num_canteens,
    "charity_thresh": charity_thresh,
    "reproduction_thresh": reproduction_thresh,
    "num_food_excess_given": num_food_excess_given,
    "canteen_life": canteen_life,
    "canteen_food_packet": canteen_food_packet,
    "g_percent": 0.33333,
    "u_percent": 0.33333,
    "t_percent": 0.33333,
    "starting_food": starting_food,
}

simulate_heatmap(iterate, days_max=day_max, init_dict=init_dict, strategy=strategy)
