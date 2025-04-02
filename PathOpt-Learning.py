from collections import deque
import math

# Function to prepare the graph, shortest paths, and delivery points
def prepare_data():
    # List of cities
    cities = ["Charleston", "Summerville", "Santee", "Columbia", "Rock Hill", "Charlotte",
              "Orangeburg", "Camden", "Lancaster", "Fort Mill"]

    # Graph representation of cities and their direct connections
    graph = {
        "Charleston": ["Summerville", "Orangeburg"],
        "Summerville": ["Charleston", "Santee"],
        "Santee": ["Summerville", "Columbia", "Orangeburg"],
        "Columbia": ["Santee", "Rock Hill", "Camden"],
        "Rock Hill": ["Columbia", "Charlotte", "Fort Mill"],
        "Charlotte": ["Rock Hill", "Lancaster"],
        "Orangeburg": ["Charleston", "Santee", "Camden"],
        "Camden": ["Orangeburg", "Columbia", "Lancaster"],
        "Lancaster": ["Camden", "Charlotte"],
        "Fort Mill": ["Rock Hill"]
    }
    
    # Function to find the shortest path between two cities using BFS
    def bfs_shortest_path(start, end):
        queue = deque([[start]])  # Initialize queue with start city as a path
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == end:
                return path  # Return the first found shortest path
            for neighbor in graph[node]:
                if neighbor not in path:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return []  # Return empty if no path found

    # Find shortest path from Charleston to Charlotte
    shortest_path = bfs_shortest_path("Charleston", "Charlotte")
    
    # Identify delivery points (all cities except those on the shortest path)
    delivery_points = list(set(graph.keys()) - set(shortest_path))
    
    # Precompute distances to Charlotte for each city using BFS path length
    distances = {city: len(bfs_shortest_path(city, "Charlotte")) - 1 for city in graph}
    
    return graph, shortest_path, delivery_points, distances

# Class representing a node in the MCTS tree
class Node:
    def __init__(self, city, parent=None):
        self.city = city  # Current city
        self.parent = parent  # Parent node (previous city in path)
        self.children = []  # List of child nodes
        self.visits = 0  # Number of times node has been visited
        self.total_value = 0  # Total accumulated score
        self.depth = parent.depth + 1 if parent else 0  # Depth of the node in the search tree
        self.visited = self._get_visited_path()  # Track visited nodes
    
    # Create a set of all visited cities along the path to this node
    def _get_visited_path(self):
        visited = set()
        node = self
        while node:
            visited.add(node.city)
            node = node.parent
        return visited
    
    # Check if all possible child nodes (neighboring cities) have been expanded
    def is_fully_expanded(self, graph):
        return len(self.children) == len([n for n in graph[self.city] if n not in self.visited])
    
    # Select the best child node based on Upper Confidence Bound (UCB) formula
    def best_child(self, c=1.414):
        if not self.children:
            return None
        
        best_score = -float('inf')
        best_child = None
        
        for child in self.children:
            if child.visits == 0:
                return child  # Prioritize unvisited children
            
            exploit = child.total_value / child.visits  # Average value
            explore = c * math.sqrt(math.log(self.visits) / child.visits)  # Exploration term
            progress = 2.0 * (self.depth - child.depth)  # Bonus for progress toward goal
            score = exploit + explore + progress
            
            if score > best_score:
                best_score = score
                best_child = child
                
        return best_child

# Simulate random path traversal to estimate value of a given node
def rollout(node, graph, delivery_points, distances, max_steps=15):
    current = node.city
    path = [current]
    visited = set(node.visited)
    score = 0
    
    for _ in range(max_steps):
        if current == "Charlotte":  # Reward for reaching the destination
            score += 1000 - 20 * len(path)
            break
        
        if current in delivery_points and current not in node.visited:
            score += 200  # Bonus for visiting a delivery point
            visited.add(current)
        
        neighbors = [n for n in graph[current] if n not in visited]
        if not neighbors:
            return score, path  # Terminate if no valid moves
        
        # Select next city prioritizing progress toward Charlotte and delivery points
        groups = [
            [n for n in neighbors if n in delivery_points and distances[n] < distances[current]],
            [n for n in neighbors if n in delivery_points],
            [n for n in neighbors if distances[n] < distances[current]],
            neighbors
        ]
        
        for group in groups:
            if group:
                next_city = min(group, key=lambda x: distances[x])
                break
        
        path.append(next_city)
        visited.add(next_city)
        current = next_city
    
    return score, path

# Monte Carlo Tree Search algorithm
def mcts(root, graph, delivery_points, distances, iterations=5000):
    best_path = []
    best_score = -float('inf')
    
    for _ in range(iterations):
        node = root
        path = [root.city]
        
        # Selection phase
        while node.is_fully_expanded(graph) and node.children:
            node = node.best_child()
            path.append(node.city)
            if node.city == "Charlotte":
                break
        
        # Expansion phase
        unexplored = [n for n in graph[node.city] if n not in node.visited]
        if unexplored:
            next_city = min(unexplored, key=lambda x: distances[x])
            new_node = Node(next_city, node)
            node.children.append(new_node)
            node = new_node
            path.append(node.city)
        
        # Simulation phase
        score, sim_path = rollout(node, graph, delivery_points, distances)
        full_path = path[:-1] + sim_path
        
        if score > best_score:
            best_score = score
            best_path = full_path
        
        # Backpropagation phase
        temp = node
        while temp:
            temp.visits += 1
            temp.total_value += score
            temp = temp.parent
    
    return best_path, best_score

# Main function to execute the algorithm
def main():
    graph, shortest_path, delivery_points, distances = prepare_data()
    root = Node("Charleston")
    best_path, best_score = mcts(root, graph, delivery_points, distances)
    print(f"Optimized path: {best_path}")
    print(f"Path score: {best_score}")

if __name__ == "__main__":
    main()
