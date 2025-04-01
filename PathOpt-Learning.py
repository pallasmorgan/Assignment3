from collections import deque
import math
 

def prepare_data():

    cities = ["Charleston", "Summerville", "Santee", "Columbia", "Rock Hill", "Charlotte",

              "Orangeburg", "Camden", "Lancaster", "Fort Mill"]

   

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

   

    def bfs_shortest_path(start, end):

        queue = deque([[start]])

        while queue:

            path = queue.popleft()

            node = path[-1]

            if node == end:

                return path

            for neighbor in graph[node]:

                if neighbor not in path:

                    new_path = list(path)

                    new_path.append(neighbor)

                    queue.append(new_path)

        return []

 

    shortest_path = bfs_shortest_path("Charleston", "Charlotte")

    delivery_points = list(set(graph.keys()) - set(shortest_path))

   

    # precompute distances to Charlotte for each city

    distances = {}

    for city in graph:

        distances[city] = len(bfs_shortest_path(city, "Charlotte")) - 1

   

    return graph, shortest_path, delivery_points, distances

 

class Node:

    def __init__(self, city, parent=None):

        self.city = city

        self.parent = parent

        self.children = []

        self.visits = 0

        self.total_value = 0

        self.depth = parent.depth + 1 if parent else 0

        self.visited = self._get_visited_path()

       

    def _get_visited_path(self):

        visited = set()

        node = self

        while node:

            visited.add(node.city)

            node = node.parent

        return visited

       

    def is_fully_expanded(self, graph):

        return len(self.children) == len([n for n in graph[self.city] if n not in self.visited])

   

    def best_child(self, c=1.414):

        if not self.children:

            return None

           

        best_score = -float('inf')

        best_child = None

       

        for child in self.children:

            if child.visits == 0:

                return child

               

            exploit = child.total_value / child.visits

            explore = c * math.sqrt(math.log(self.visits) / child.visits)

            progress = 2.0 * (self.depth - child.depth)  # huge progress bonus

            score = exploit + explore + progress

           

            if score > best_score:

                best_score = score

                best_child = child

               

        return best_child

 

def rollout(node, graph, delivery_points, distances, max_steps=15):

    current = node.city

    path = [current]

    visited = set(node.visited)

    score = 0

   

    for _ in range(max_steps):

        if current == "Charlotte":

            score += 1000 - 20*len(path)  # huge destination reward

            break

            

        if current in delivery_points and current not in node.visited:

            score += 200  # huge delivery point reward

            visited.add(current)

       

        # only consider unvisited neighbors

        neighbors = [n for n in graph[current] if n not in visited]

       

        if not neighbors:

            if "Charlotte" in graph[current]:

                path.append("Charlotte")

                score += 1000 - 20*len(path)

                break

            return score, path  # terminate if stuck

       

        # smart selection with strict priorities

        groups = [

            [n for n in neighbors

             if n in delivery_points and

             n not in visited and

             distances[n] < distances[current]],

            [n for n in neighbors

             if n in delivery_points and

             n not in visited],

            [n for n in neighbors

             if distances[n] < distances[current]],

            neighbors

        ]

       

        for group in groups:

            if group:

                next_city = min(group, key=lambda x: distances[x])

                break

       

        path.append(next_city)

        visited.add(next_city)

        current = next_city

   

    # final score calculation

    unique_deliveries = len(visited & set(delivery_points))

    revisited = len(path) - len(set(path))

   

    score += 150 * unique_deliveries  # huge unique delivery bonus

    score -= 20 * len(path)  # huge path length penalty

    score -= 500 * revisited  # huge penalty for revisits

   

    if unique_deliveries < len(delivery_points):

        score -= 1000  # huge penalty for missing deliveries

   

    return score, path

 

def mcts(root, graph, delivery_points, distances, iterations=5000):

    best_path = []

    best_score = -float('inf')

   

    for _ in range(iterations):

        node = root

        path = [root.city]

       

        # selection with strict visit tracking

        while node.is_fully_expanded(graph) and node.children and len(path) < 10:

            node = node.best_child()

            path.append(node.city)

            if node.city == "Charlotte":

                break

       

        # expansion ensuring no revisits

        if not node.is_fully_expanded(graph) and len(path) < 10:

            unexplored = [n for n in graph[node.city]

                         if n not in node.visited and

                         not any(c.city == n for c in node.children)]

           

            # prioritize unvisited deliveries making progress

            candidates = [

                n for n in unexplored

                if n in delivery_points and

                distances[n] < distances[node.city]

            ]

           

            if not candidates:

                candidates = [n for n in unexplored if n in delivery_points]

           

            if not candidates:

                candidates = [n for n in unexplored if distances[n] < distances[node.city]]

           

            if not candidates:

                candidates = unexplored

           

            next_city = min(candidates, key=lambda x: distances[x]) if candidates else None

            if next_city:

                new_node = Node(next_city, node)

                node.children.append(new_node)

                node = new_node

                path.append(node.city)

       

        # simulation

        if node.city != "Charlotte":

            score, sim_path = rollout(node, graph, delivery_points, distances)

            full_path = path[:-1] + sim_path

           

            if score > best_score:

                best_score = score

                best_path = full_path

           

            # backpropagation

            temp = node

            while temp:

                temp.visits += 1

                temp.total_value += score

                temp = temp.parent

   

    return best_path, best_score

 

def main():

    graph, shortest_path, delivery_points, distances = prepare_data()

    print(f"Shortest path ({len(shortest_path)}): {shortest_path}")

    print(f"Delivery points: {delivery_points}")

   

    root = Node("Charleston")

    best_path, best_score = mcts(root, graph, delivery_points, distances)

   

    visited_deliveries = set(best_path) & set(delivery_points)

    missing = set(delivery_points) - visited_deliveries

    if missing:

        print("\nWARNING: Missing delivery points:", missing)

   

    print(f"\nOptimized path ({len(best_path)}): {best_path}")

    print(f"Delivery points visited: {visited_deliveries}")

    print(f"Path score: {best_score}")

 

if __name__ == "__main__":

    main()