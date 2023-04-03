from time_ import Time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
from global_vars import *
import os

iterate = 5
day_max = 10

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
    "g_percent": 1/3,
    "u_percent": 1/3,
    "t_percent": 1/3,
    "starting_food": starting_food,
}
food_list_1 = []
populations = []
record = []
for i in tqdm(range(iterate)):
    population = []
    Environment = Time(init_dict=init_dict)
    T = -1
    while Environment.day <= day_max:
        print(Environment.day)
        g, u, t, T = Environment.get_population()
        population.append((g, u, t, T))
        number_canteens = np.sum(Environment.grid.grid)
        food_list = []
        food_list = Environment.update()
        food_list_1 = food_list_1+food_list
    populations.append(population)
    record.append([g, u, t, T])

df = pd.DataFrame(record)
print(init_dict)
print("Last_Day:", day_max)
print("Population Details")
print(df.describe())

populations = np.array(populations)
populations_mean = np.mean(populations, axis=0)
populations_std = np.std(populations, axis=0)

fig, ax = plt.subplots(1, 1)
ax.errorbar(
    np.linspace(0, day_max - 1, day_max),
    populations_mean[:, 0],
    populations_std[:, 0],
    label=f"grateful",
)
ax.errorbar(
    np.linspace(0, day_max - 1, day_max),
    populations_mean[:, 1],
    populations_std[:, 1],
    label=f"ungrateful",
)
ax.errorbar(
    np.linspace(0, day_max - 1, day_max),
    populations_mean[:, 2],
    populations_std[:, 2],
    label=f"titfortat",
)
ax.errorbar(
    np.linspace(0, day_max - 1, day_max),
    populations_mean[:, 3],
    populations_std[:, 3],
    label=f"total",
)
g_percent = init_dict["g_percent"]
u_percent = init_dict["u_percent"]
t_percent = init_dict["t_percent"]
ax.set_title(
    f"g_per: {g_percent:0.2f}, u_per: {u_percent:0.2f}, t_per: {t_percent:0.2f}"
)
ax.legend()
ax.set_xlabel("Time steps")
ax.set_ylabel("Population")
plt.savefig(
    os.path.join("assets",
                 f"aa_dead_communism_g{int(g_percent*100)}_u{int(u_percent*100)}_t{int(t_percent*100)}.png")
)

plt.show()

food_list_1 = np.array(food_list_1)
food_list_1 = pd.DataFrame(food_list_1)
print(food_list_1.describe())
plt.hist(food_list_1, bins=100, edgecolor='black')
plt.xlabel('food')
plt.ylabel('number of pacmen')

plt.show()
