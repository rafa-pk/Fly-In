*This project has been created as part of the 42 curriculum by rvaz-da-*

---

# Fly-In

## Description
Fly-in is a pathfinding project where the goal is to successfully and efficiently orientate a fleet of drones accross a node-graph, following strict constraints.

When run, the program runs an interactive menu for the user to chose the map file the program should take as a parameter. From there, the program parses it, creates a graph structure and finds the ideal algorithm to orientate all drones successfully. When that is done, it displays its feats in a graphical simulation.

The goal is to further learn about graph-theory, after a brief introduction with A-Maze-Ing and to confront ourselves with efficient pathfinding, which is used everywhere nowadays. As well as allowing for creative freedom with the graphical interface.


## Instructions:

### Execution
The program can be run via make with the following commands:
```bash
make install        # Installs virtual environment and required dependencies

make run            # Runs the program (and runs make instal if not done already)

make lint           # Runs flake8 and mypy for norm-checking

make lint-strict    # Runs flake8 and mypy --strict for strict typechecking

make clean          # Cleans cache files

make fclean         # Cleans cache files, virtual environment and everything else that was created at runtime

make re             # Runs make clean + make run
```

### Map file format:

- '#' define commented lines
- The first valid line has to define the number of drones, as a positive integer
- Hub definitions come first, as such: < type >: < name > < x-coord > < y-coord > [metadata] (optional)
- Connections are defined afterwards, as such: < connection >: < src_node >-< dest_node > [metadata] (optional)

Metadata varies depending on hub/connection, but is the following:

**For hubs:**
- < zone >: str, defaults to normal. Blocked means node is unaccessible, restricted that it takes 2 moves to get to it and priority that it should be prioritized in pathfinding.
- < color >: str, defines node's color
- < max_drones >: int, defaults to 1. Defines the maximum number of drones allowed in the zone simultaneously

**For connections:**
- < max_link_capacity >: int, defaults to 1. Defines the maximum number of drones allowed to move through the connection simultaneously

## Actions
ESC is always available to quit the program safely and close the window, the remaining actions are context-specific:

When in the map menu, the following actions are possible:
- ENTER: select file
- LEFT/L: move to directory
- RIGHT/H: move back one directory
- UP/K: move cursor to file above
- DOWN/J: move cursor to file below

When in the simulation, these are:
- SPACE: pause/resume simulation
- R: restart program from map menu
- Mouse hover over nodes: Displays node information
- Click on left joystick: fellow 42 students' screamers who block the simulation
- X: exit the secret screamers
- Click on up-right button: Rick-roll redirection
- Mouse click where you shouldn't: FAHHHHHH sound

## Algorithm:
After some trial and error, I decided to settle with a Space-Time A* variant, which uses a limited Reverse Dijkstra's algorithm as a dynamic heuristic.

This means for every node in my graph I do the following:
1. Run a Reverse Dijkstra from end to the current node, computing its cost, which I made dependent on its current affluence. This means the least-costly nodes will be the priority ones, and then the least-populated ones.
2. With that cost list, I look at every neighbour in that list and compute the cost of moving to it, in order to chose the cheapest one. Cost is the cost so far + the edge cost + the heuristic

By using a min-heap, the next itteration will pop the cheapest node, building the path backwards. I then call a method which retraces the path, ignoring the other possibilities that were considered, reverses it and stores it in a list. This list will be passed as the .path parameter for that drone, and will be its path from here on.

In order to keep track of which drone is occupying which node/edge at what time-step in the simulation, I use a reservation table, which is just a dynamic log of everything happening during the algorithm's execution.

I chose to do things this way because of the subject's inconsistency vis-a-vis the map files provided. This allows for an optimal-move choice per current state, which is not necessarily the most efficient path but maximises graph-area usage and respects limitations.


## Features:
The main features I added are the following:
- The program takes a map file as an argument, but also uses make. Which made it very unpractical to switch between two maps. To address this, I made a map menu, which allows the user to chose which map is going to be used. The interface works much like a file-manager.
- For the same practical reason, I added a refresh button which allows the program to run from the beginning and prompts the user to chose a file, never having to actually quit the program.
- Within my simulation, I added a dashboard which displays information dynamically, such as the move count. And a terminal emulation which displays the moves being made in real-time, like what is being printed to stdout.
- I also added easter-eggs such as a rick-roll and screamers with some of my peers' intra pictures.


## Resources:

### Documentation:
- [W3 Schools](www.w3schools.com) - General python information
- [GeeksforGeeks](www.geeksforgeeks.com) - General python information
- [A*-based Pathfinding in Modern Computer Games](https://www.researchgate.net/profile/Xiao-Cui-12/publication/267809499_A-based_Pathfinding_in_Modern_Computer_Games/links/54fd73740cf270426d125adc/A-based-Pathfinding-in-Modern-Computer-Games.pdf?__cf_chl_tk=tP3t_ZbwgEIQSjXcL1wagMH72oP1o.XZRiNuH25NNuA-1776164084-1.0.1.1-f.1jfE3azCfrfA0fAfg.1_Pxtkc2jffaqiQY4mmeqf0) - Paper about A* algorithm
- [Research on the A Star Algorithm for Finding Shortest Path](https://www.researchgate.net/publication/370573811_Research_on_the_A_Star_Algorithm_for_Finding_Shortest_Path) - Paper about A* algorithm
- [A*'s use of Heuristic](https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) - Blogpost discussing various heuristics for A*
- [Cooperative Pathfinding](https://davidstarsilver.wordpress.com/wp-content/uploads/2025/04/cooperative-pathefac81nding.-d.-silver.-ai-game-programming-wisdom-3.pdf) - Paper explaining the limitations of A* in regards to time and multi-agent pathfinding
- [Pygame docs](www.pygame.org) - Pygame documentation
- [Building an A* Pathfinding Visualizer in Python with Pygame](https://medium.com/@aggorjefferson/building-an-a-pathfinding-visualizer-in-python-with-pygame-a2cb3502f49e) - Medium article about pygame
- [Reddit](www.reddit.com) - General information and answers to similar questions I had
- [Stack Overflow](www.stackoverflow.com) - Search of answers to frequently asked questions

### AI usage
Claude was used in this project as a search-engine and peer only. This means I only used it to search for information or discuss and clear out ideas and doubts I had. I also asked it to review my code so that I could have a second pair of "eyes" looking at it. 
No claude-produced code is present in the project.