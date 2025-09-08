import heapq

class AStarPathfinding:
    def __init__(self, maze, start_pos, target_pos):
        """
        Initialize the A* pathfinding algorithm.

        Args:
            maze (list of list of int): 2D grid representing the maze (1 = open, 0 = blocked).
            start_pos (tuple): Starting position (row, col).
            target_pos (tuple): Target position (row, col).
        """
        self.maze = maze
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.open_list = []
        self.closed_list = set()
        self.came_from = {}

    def heuristic(self, a, b):
        """
        Calculate the Manhattan distance heuristic between two points.

        Args:
            a (tuple): First position (row, col).
            b (tuple): Second position (row, col).

        Returns:
            int: Manhattan distance between a and b.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_neighbors(self, pos):
        """
        Get all valid neighboring positions (up, down, left, right) for a given position.

        Args:
            pos (tuple): Current position (row, col).

        Returns:
            neighbors: List of valid neighboring positions.
        """
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for d in directions:
            neighbor = (pos[0] + d[0], pos[1] + d[1])
            if self.is_valid(neighbor):
                neighbors.append(neighbor)
        return neighbors
    
    def is_valid(self, pos):
        """
        Check if a position is within the maze bounds and not blocked.

        Args:
            pos (tuple): Position to check (row, col).

        Returns:
            bool: True if position is valid and open, False otherwise.
        """
        row, col = pos
        return 0 <= row < len(self.maze) and 0 <= col < len(self.maze[0]) and self.maze[row][col] == 1
    
    def find_path(self):
        """
        Execute the A* algorithm to find the shortest path from start to target.

        Returns:
            list or None: List of positions representing the path, or None if no path exists.
        """
        heapq.heappush(self.open_list, (0, self.start_pos))  # Add start position to open list
        g_score = {self.start_pos : 0}  # Cost from start to current node
        f_score = {self.start_pos : self.heuristic(self.start_pos, self.target_pos)}  # Estimated total cost

        while self.open_list:
            _, current = heapq.heappop(self.open_list)  # Get node with lowest f_score
            if current == self.target_pos:
                return self.reconstruct_path(current)  # Path found
            self.closed_list.add(current)  # Mark current node as evaluated

            for neighbor in self.get_neighbors(current):
                if neighbor in self.closed_list:
                    continue  # Skip already evaluated neighbors
                tentative_g_score = g_score[current] + 1  # Cost from start to neighbor
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    self.came_from[neighbor] = current  # Track path
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, self.target_pos)
                    heapq.heappush(self.open_list, (f_score[neighbor], neighbor))  # Add neighbor to open list

        return None  # No path found
    
    def reconstruct_path(self, current):
        """
        Reconstruct the path from start to target by backtracking from the target.

        Args:
            current (tuple): Current position (target node).

        Returns:
            path: List of positions representing the path from start to target.
        """
        path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)
        path.reverse()  # Reverse to get path from start to target
        return path
    
if __name__ == "__main__":
    start = (0, 0)
    target = (7, 7)
    maze = [
        [1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 1],
        [0, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1],
    ]
    
    astar = AStarPathfinding(maze, start, target)
    path = astar.find_path()
    print("Path found:" if path else "No path found")
    if path:
        for step in path:
            print(step)