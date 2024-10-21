import tkinter as tk
from PIL import Image, ImageTk
import time
from heapq import heappush, heappop  # For priority queue
from checkSolvability import is_solvable  # Import your solvability checker

class Node:
    """Structure of a puzzle node."""
    def __init__(self, state, parent, action, depth, cost, heuristic):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost  # g(n) = path cost
        self.heuristic = heuristic  # h(n) = heuristic value
        self.f_value = cost + heuristic  # f(n) = g(n) + h(n)

    def __lt__(self, other):
        """For priority queue comparison."""
        return self.f_value < other.f_value

    def path_from_start(self):
        """Retrieve the path from the initial state to the goal."""
        path = []
        current = self
        while current:
            path.append(current.state)
            current = current.parent
        return path[::-1]

def manhattan_distance(state, goal_state):
    """Calculate the Manhattan Distance between the current state and the goal."""
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:  # Skip the empty tile
            goal_index = goal_state.index(tile)
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(goal_index, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def get_neighbors(state):
    """Generate valid neighboring states."""
    neighbors = []
    index = state.index(0)  # Find the empty tile (0)
    moves = [(-3, "up"), (3, "down"), (-1, "left"), (1, "right")]

    for move, action in moves:
        new_index = index + move
        if 0 <= new_index < 9 and not (index % 3 == 0 and action == "left") and not (index % 3 == 2 and action == "right"):
            new_state = state[:]
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append((new_state, action))
    return neighbors

def a_star_search(start_state, goal_state):
    """A* search algorithm for solving the 8-puzzle."""
    open_list = []
    closed_set = set()

    start_node = Node(start_state, None, None, 0, 0, manhattan_distance(start_state, goal_state))
    heappush(open_list, start_node)

    while open_list:
        current_node = heappop(open_list)

        if current_node.state == goal_state:
            return current_node.path_from_start()

        closed_set.add(tuple(current_node.state))

        for neighbor, action in get_neighbors(current_node.state):
            if tuple(neighbor) in closed_set:
                continue

            cost = current_node.depth + 1
            heuristic = manhattan_distance(neighbor, goal_state)
            neighbor_node = Node(neighbor, current_node, action, cost, cost, heuristic)
            heappush(open_list, neighbor_node)

    return None  # No solution found

class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Game")

        self.puzzle_state = [None] * 9  # Initial empty state
        self.next_tile_index = 0  # Tracks the next tile to place
        self.goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Goal state

        self.load_images()
        self.create_gui()

    def load_images(self):
        """Load images for the tiles."""
        self.images = [ImageTk.PhotoImage(Image.open(f"girl/{i}girl.png").resize((100, 100))) 
                       for i in range(1, 9)]
        self.images.insert(0, ImageTk.PhotoImage(Image.open("girl/blank.png").resize((100, 100))))

    def create_gui(self):
        self.left_frame = tk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)

        full_image = Image.open("girl/girl.png").resize((300, 300))
        self.full_image = ImageTk.PhotoImage(full_image)

        self.left_image_label = tk.Label(self.left_frame, image=self.full_image)
        self.left_image_label.pack()

        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.right_frame, command=lambda i=i, j=j: self.set_tile(i, j))
                button.grid(row=i, column=j, sticky='nsew', padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        for i in range(3):
            self.right_frame.grid_rowconfigure(i, weight=1)
            self.right_frame.grid_columnconfigure(i, weight=1)

        self.start_button = tk.Button(self.root, text="Start", command=self.solve_puzzle)
        self.start_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.step_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.step_label.grid(row=2, column=0, columnspan=2)

        self.time_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.time_label.grid(row=3, column=0, columnspan=2)

    def set_tile(self, i, j):
        index = i * 3 + j
        if self.puzzle_state[index] is None and self.next_tile_index < 9:
            self.puzzle_state[index] = self.next_tile_index
            self.buttons[i][j].config(image=self.images[self.next_tile_index])
            self.next_tile_index += 1

    def solve_puzzle(self):
        if None in self.puzzle_state:
            print("Please complete the puzzle first.")
            return

        if is_solvable(self.puzzle_state):
            start_time = time.time()
            solution = a_star_search(self.puzzle_state, self.goal_state)
            self.animate_solution(solution, start_time)
        else:
            print("No solution exists for this state.")

    def animate_solution(self, solution, start_time):
        total_steps = len(solution)
        for step_number, state in enumerate(solution, start=1):
            self.update_grid(state)
            self.step_label.config(text=f"Step: {step_number}/{total_steps}")
            self.root.update()
            time.sleep(1)

        elapsed_time = time.time() - start_time
        self.time_label.config(text=f"Total Time: {elapsed_time:.2f} seconds")
        self.step_label.config(text="Solved!")

    def update_grid(self, state):
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                tile = state[index]
                self.buttons[i][j].config(image=self.images[tile])

if __name__ == "__main__":
    root = tk.Tk()
    game = PuzzleGame(root)
    root.mainloop()
