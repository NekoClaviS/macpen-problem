from time_ import Time
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from tqdm import tqdm
from global_vars import g_percent, u_percent, t_percent, rows, cols


def simulate_heatmap(iterate, days_max, init_dict, strategy):
    populations = []
    for i in tqdm(range(iterate)):
        population = []
        Environment = Time(init_dict)
        T = -1
        g_pop = u_pop = t_pop = tot_pop = np.zeros((rows, cols))
        while Environment.day <= days_max:
            g, u, t, T = Environment.get_population()
            (g_pop_day, u_pop_day, t_pop_day, tot_pop_day) = Environment.grid.display()
            g_pop = g_pop + g_pop_day
            u_pop = u_pop + u_pop_day
            t_pop = t_pop + t_pop_day
            tot_pop = tot_pop + tot_pop_day
            population.append((g, u, t, T))
            # number_canteens = np.sum(Environment.grid.grid)
            # print(
            #     f"Day: {Environment.day}| Population: {(g, u, t, T)}; Canteens: {number_canteens}"
            # )
            Environment.update()
        populations.append(population)
        g_pop /= days_max
        u_pop /= days_max
        t_pop /= days_max

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.set_title(f"Spatial Distribution of Macpen")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_title("Spatial distribution of grateful Macpen")
    ax2.set_title("Spatial distribution of ungrateful Macpen")
    ax3.set_title("Spatial distribution of tit-for-tat Macpen")
    ax4.set_title("Spatial distribution of total Macpen")
    sns.heatmap(g_pop, ax=ax1)
    sns.heatmap(u_pop, ax=ax2)
    sns.heatmap(t_pop, ax=ax3)
    sns.heatmap(tot_pop, ax=ax4)
    ax1.set_title("Spatial distribution of grateful Macpen")
    ax2.set_title("Spatial distribution of ungrateful Macpen")
    ax3.set_title("Spatial distribution of tit-for-tat Macpen")
    ax4.set_title("Spatial distribution of total Macpen")
    sns.heatmap(g_pop, ax=ax1)
    sns.heatmap(u_pop, ax=ax2)
    sns.heatmap(t_pop, ax=ax3)
    sns.heatmap(tot_pop, ax=ax4)
    fig.show()
    populations = np.array(populations)
    populations_mean = np.mean(populations, axis=0)
    populations_std = np.std(populations, axis=0)

    fig, ax = plt.subplots(1, 1)
    ax.errorbar(
        np.linspace(0, days_max - 1, days_max),
        populations_mean[:, 0],
        populations_std[:, 0],
        label=f"grateful",
    )
    ax.errorbar(
        np.linspace(0, days_max - 1, days_max),
        populations_mean[:, 1],
        populations_std[:, 1],
        label=f"ungrateful",
    )
    ax.errorbar(
        np.linspace(0, days_max - 1, days_max),
        populations_mean[:, 2],
        populations_std[:, 2],
        label=f"titfortat",
    )
    ax.errorbar(
        np.linspace(0, days_max - 1, days_max),
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
        f"./assets/{strategy}_g{g_percent:0.2f}_u{u_percent:0.2f}_t{t_percent:0.2f}.png"
    )
    plt.show()



def simulate_population_statistics(populations, iterate, days):
    for i in range(iterate):
        population = []
        Environment = Time()
        T = -1
        while Environment.day < days and T != 0:
            g, u, t, T = Environment.get_population()
            population.append((g, u, t, T))
            number_canteens = np.sum(Environment.grid.grid)
            print(
                f"Day: {Environment.day}| Population: {(g, u, t, T)}; Canteens: {number_canteens}"
            )
            Environment.update()
        populations.append(population)

    fig, ax = plt.subplots(1, 1)
    for i in range(iterate):
        population = populations[i]
        population_tuple = tuple(zip(*population))
        ax.plot(population_tuple[0], alpha=0.3, label=f"grateful {i}")
        ax.plot(population_tuple[1], alpha=0.3, label=f"ungrateful {i}")
        ax.plot(population_tuple[2], alpha=0.3, label=f"titfortat {i}")
        ax.plot(population_tuple[3], "-x", label=f"Total {i}")
    ax.set_title(
        f"g_per: {g_percent:0.2f}, u_per: {u_percent:0.2f}, t_per: {t_percent:0.2f}"
    )
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Population")
    ax.legend()
    fig.show()
    input()
