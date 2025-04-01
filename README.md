# Path Exploration using MCTs and Value Learning
---
## Description
This project explores the path between Charleston and Charlotte using MCTS. This will be done by creating a graph structure where Charleston is the starting point and Charlotte is the desination. Each time the algorithm will choose 5 random points, from the set of locations in assignment 2, to stop at (delivery points).
Use value learning to ensure your algorithm reaches its desination through the shortest path. Assign moves with positive or negitative points, end the traversal once the desination (Charlotte) is reached or once a set negative value is returned.
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
    
   from collections import deque
   import math
    

## Usage

Run the program with:

```sh
python PathOpt-Learning.py  # Python

```

## Features

-prepare_data() 
-- Where the cites and the graph are initialized.
- bfs_shortest_path(start, end)
- - uses bfs to traverse through the graph, starts at Charleston and ends at Charlotte or until score is too low.
  - class Node
  - - initilizes a current city, parent, children, visits, tot_vale, depth, and the visited nodes.
    - - _get visited_path
      - is_fully_espanded: expands a current node to its children
      - best_child: returns the best child and adds its value to the score
- rollout: sets a node to visited on the current path, calculates the score and updates through the path. Appends the next step(city) to the path and the list of visited for the learning.
- key features: selection with strict visit tracking, expansion ensuring no revisits, prioritize unvisited deliveries making progress, simulation, backpropagation
## Technologies Used

- Python 3.10
- Github


## Contact

- GitHub: @pallasmorgan, @aylenemce, @jacko123456
- Email: pallasmv@g.cofc.edu, mcentireak@g.cofc.edu, keimjm@g.cofc.edu
