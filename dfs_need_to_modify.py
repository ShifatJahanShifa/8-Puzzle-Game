class PuzzleDFS:
    def __init__(self, initial_grid, goal_grid):
        self.initial_grid = initial_grid
        self.goal_grid = goal_grid
        self.n = len(initial_grid) 

    def get_blank_pos(self, grid):
        for i in range(self.n):
            for j in range(self.n):
                if grid[i][j] == 0:
                    return i, j
        return None

    def is_goal(self, grid):
        return grid == self.goal_grid

    def move(self, grid, blank_pos, direction):
        x, y = blank_pos
        new_grid = [row[:] for row in grid] 

        if direction == "up" and x > 0:
            new_grid[x][y], new_grid[x-1][y] = new_grid[x-1][y], new_grid[x][y]
        elif direction == "down" and x < self.n - 1:
            new_grid[x][y], new_grid[x+1][y] = new_grid[x+1][y], new_grid[x][y]
        elif direction == "left" and y > 0:
            new_grid[x][y], new_grid[x][y-1] = new_grid[x][y-1], new_grid[x][y]
        elif direction == "right" and y < self.n - 1:
            new_grid[x][y], new_grid[x][y+1] = new_grid[x][y+1], new_grid[x][y]
        else:
            return None  

        return new_grid

    def print_grid(self, grid):
        """Print the current state of the grid."""
        for row in grid:
            print(row)
        print()  

    def solve(self, max_depth=50):
        """Solve the puzzle using DFS."""
        stack = [(self.initial_grid, self.get_blank_pos(self.initial_grid), [], 0)]  # (grid, blank_pos, path, depth)
        visited = set()
        visited.add(tuple(map(tuple, self.initial_grid)))

        directions = ["up", "down", "left", "right"]

        while stack:
            current_grid, blank_pos, path, depth = stack.pop()

            print(f"Iteration: {len(path)}, Depth: {depth}")
            self.print_grid(current_grid)

          
            if self.is_goal(current_grid):
                print("Solution found! Moves: ", path)
                return path

           
            if depth >= max_depth:
                continue

            
            for direction in directions:
                new_grid = self.move(current_grid, blank_pos, direction)

                if new_grid is not None and tuple(map(tuple, new_grid)) not in visited:
                    visited.add(tuple(map(tuple, new_grid)))
                    stack.append((new_grid, self.get_blank_pos(new_grid), path + [direction], depth + 1))

        return None  


initial_grid = [[1, 2, 3],
                [0, 4, 6],
                [7, 5, 8]]

goal_grid = [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 0]]

puzzle = PuzzleDFS(initial_grid, goal_grid)
solution = puzzle.solve(max_depth=50)

if solution:
    print("Solution found! Moves: ", solution)
else:
    print("No solution exists.")
