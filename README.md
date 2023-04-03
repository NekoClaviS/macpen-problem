# macpen-problem

Codebase for the implementation of the simulation for the BCS Problem Statement - Neuroeconomics in Takneek 2023. Submitted by Hall 2.

## Installation

This repository utilises python and basic libraries. Install via:

```bash
pip install -r requirements.txt
```

## main.py AND global_vars.py

Run the main code, aka simulate the universe through `main.py`. Change the parameters either directly in the dictionary present in `main.py` or `global_vars.py`.

## greedy_implementation

Move files within greedy_implementation directory to the current folder (note that you would need the same names to run them without any changes). Implements greedy_movement of pacman.

## conway_implementation

Move files within greedy_implementation directory to the current folder (note that you would need the same names to run them without any changes). Implements conway_implementation of pacman.

## food_distribution

Move files within greedy_implementation directory to the current folder (note that you would need the same names to run them without any changes). This implements visualization of food distribution throughout a timeline, averaged along multiple timelines.

## time.py

- `__init__(self, init_dict)`: initializes the Time object and sets the initial state of the grid and Pacman agents based on the given init_dict dictionary. It also generates the initial population of Pacman agents based on the proportions of each trait specified in the dictionary.
- `get_population(self)`: iterates through all the cells in the grid and counts the population of each type of Pacman. Returns a tuple of four integers: the number of grateful, ungrateful, tit-for-tat, and total Pacman agents in the grid.
- `update(self)`: updates the state of the grid and Pacman agents after each time step. It spawns new canteens at random locations in the grid after a specified number of days, refills Pacman agents' food levels from nearby canteens, allows Pacman agents to reproduce if their food levels exceed a certain threshold, calculates the contributions of each Pacman agent to their cell's food supply, and allows Pacman agents to fight each other if the fight flag is set to True.

## grid.py

The class has several attributes such as rows, cols, num_canteens, canteen_life, ghost_tax, canteen_food_packet, and grid. The class also has a constructor that initializes these attributes and creates a list of Cell objects that represent the cells in the grid.

The class has several methods:

- `spawn_canteen(num_canteens)`: This method randomly generates canteens in the grid.
- `display()`: This method returns four matrices that represent the population of ghosts, unicorns, and traitors in each cell of the grid, and the total number of agents in each cell.
- `__str__()`: This method returns a string representation of the grid.

The code also includes an if statement that checks if the code is being executed as the main module. If it is, it creates an instance of the Grid class, prints the number of Pacman objects in the first cell, calls the spawn_canteen() method to generate canteens in the grid, and then prints a string representation of the grid.

## pacman.py

The class has various methods to define the behavior of Pacman, such as moving, reproducing, sharing food, updating history, consuming ghost tax, refilling food, dying, and killing.

The class has the following attributes:

- `init_dict`: a dictionary that contains the initial values of various parameters.
- `x_cord`: an integer that represents the x-coordinate of Pacman's location.
- `y_cord`: an integer that represents the y-coordinate of Pacman's location.
- `food`: an integer that represents the amount of food that Pacman has.
- `trait`: a global variable from a module named global_vars that represents the personality trait of Pacman. There are four traits: GRATEFUL, UNGRATEFUL, TITFORTAT (G) and TITFORTAT (U).
- `history`: a boolean value that represents the history of Pacman's behavior.

The class has the following methods:

- `__init__(self, starting_food, trait, x_cord, y_cord, init_dict)`: This is the constructor method of the class, which initializes the attributes of Pacman with the given parameters.
- `move(self, m, n)`: This method defines the movement of Pacman in the Pacman universe. The movement is random and can be up, down, left, or right.
- `reproduce(self, cell: Cell)`: This method allows Pacman to reproduce if its food count becomes greater than the reproduction threshold. It creates a new Pacman with half the food of the parent Pacman.
- `share(self)`: This method allows Pacman to share food with others according to the availability of food and the Pacman's personality trait.
- `update_history(self, received: bool)`: This method updates Pacman's history of behavior based on whether Pacman received help from others.
    consume_ghost_tax(self): This method deducts a certain amount of food (ghost tax) from all the Pacman at the end of each day.
- `refill(self, amount: int)`: This method increases Pacman's food count by the amount of food found. The amount of food can be distributed based on different strategies, such as normal filling, communism in low resources, communism, or left-right distribution.
- `die(self, cell: Cell)`: This method removes Pacman from the Pacman universe when it dies.
- `kill(self, pacman, cell: Cell)`: This method allows Pacman to kill another Pacman and obtain half of its food.
- `__str__(self)`: This method returns a string representation of Pacman, which includes its food count, personality trait, location, and history.

## cell.py

The Cell class contains the following attributes:

- `init_dict`: a dictionary of initial values used for simulation.
- `x`: an integer representing the x-coordinate of the cell.
- `y`: an integer representing the y-coordinate of the cell.
- `pacmen`: a dictionary with keys representing different Pac-Man traits (Grateful, Ungrateful, and Tit-for-Tat) and values representing the list of Pac-Man instances with that trait in the cell.
- `near_death_pacman`: a list of Pac-Man instances that are close to death in the current cell.
- `food_pool`: an integer representing the amount of food available in the current cell.

The Cell class contains the following methods:

- `contri()`: a method that calculates the food distribution among Pac-Men in the current cell. The method calculates the number of near-death Pac-Men and sorts them in descending order based on their need for food. It then calculates the number of Pac-Men that can help the near-death Pac-Men survive and randomly selects which Pac-Men will help. After that, it distributes the available food among the near-death Pac-Men and the remaining food among the surviving Pac-Men.
- `get_population()`: a method that returns the population of each trait of Pac-Men in the current cell.
- `__str__()`: a method that returns a string representation of the current cell object, containing the x and y coordinates, and the population of each Pac-Man trait in the cell.

The Cell class depends on a global variable TRAIT and a NumPy library. The TRAIT variable contains an enumeration of different Pac-Man traits. NumPy is used to generate random numbers for the binomial distribution used in the contri() method.
