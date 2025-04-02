# Path Exploration using MCTs and Value Learning
---
## Description
his project explores the optimal path between Charleston and Charlotte using Monte Carlo Tree Search (MCTS) with value learning. The algorithm dynamically selects five random delivery points from a predefined list of cities and ensures efficient path traversal while minimizing negative scores.

The goal is to reach Charlotte using the shortest possible route while maximizing rewards from deliveries and minimizing penalties for revisits or inefficiencies.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Contact](#contact)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/pallasmorgan/assignment3.git
	```

2. Navigate to the project directory:
    
    ```sh
    cd assignment3
    ```
    
3. Install dependencies (if applicable):
    
   pip install -r requirements.txt
    

## Usage

Run the program with:

```sh
python PathOpt-Learning.py  # Python

```

## Features

1. Graph Representation & Initialization
   - prepare_data() – Initializes the graph structure with predefined city connections and computes shortest paths from each city to Charlotte using BFS.

3. Pathfinding Algorithms
   - bfs_shortest_path(start, end) – Uses Breadth-First Search (BFS) to determine the shortest path from Charleston to Charlotte.

   - rollout(node, graph, delivery_points, distances, max_steps=15) – Simulates path traversal, selecting the next city based on priority rules while updating scores.

3. Monte Carlo Tree Search (MCTS)
   - MCTS consists of four main steps:

 - Selection: Chooses the best child node using a balance of exploitation and exploration.

   - Expansion: Expands new nodes only when necessary, prioritizing unvisited deliveries and cities leading toward Charlotte.

   - Simulation (Rollout): Runs a simulated path to evaluate the effectiveness of a given route.

   - Backpropagation: Updates values in the tree to refine future decisions.

4. Node Class for MCTS
   - Node(city, parent=None): Represents a city in the search tree, tracking visits, values, depth, and explored paths.

   - is_fully_expanded(graph): Checks if all possible children of a node have been expanded.

   - best_child(c=1.414): Selects the optimal next city based on a UCT formula, ensuring balance between exploration and exploitation.


## Technologies Used

- Python 3.10
- math (mathematical calculations for scoring)
- collections.deque (used in BFS for shortest pathfinding)
- Github


## Contact

- GitHub: @pallasmorgan, @aylenemce, @jacko123456
- Email: pallasmv@g.cofc.edu, mcentireak@g.cofc.edu, keimjm@g.cofc.edu
