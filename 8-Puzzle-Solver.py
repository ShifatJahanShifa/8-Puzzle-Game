import sys
import numpy as np
# import tkinter as tk

class Node:
	def __init__(self, state, parent, action):
		self.state = state
		self.parent = parent
		self.action = action


class StackFrontier:
	def __init__(self):
		self.frontier = []

	def add(self, node):
		self.frontier.append(node)

	def contains_state(self, state):
		return any((node.state[0] == state[0]).all() for node in self.frontier)
	
	def empty(self):
		return len(self.frontier) == 0
	
	def remove(self):
		if self.empty():
			raise Exception("Empty Frontier")
		else:
			node = self.frontier[-1]
			self.frontier = self.frontier[:-1]
			return node


class QueueFrontier(StackFrontier):
	def remove(self):
		if self.empty():
			raise Exception("Empty Frontier")
		else:
			node = self.frontier[0]
			self.frontier = self.frontier[1:]
			return node


class Puzzle:
	def __init__(self, start, startIndex, goal, goalIndex):
		self.start = [start, startIndex]
		self.goal = [goal, goalIndex] 
		self.solution = None

	def neighbors(self, state):
		mat, (row, col) = state
		results = []
		
		if row > 0:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row - 1][col]
			mat1[row - 1][col] = 0
			results.append(('up', [mat1, (row - 1, col)]))
		if col > 0:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row][col - 1]
			mat1[row][col - 1] = 0
			results.append(('left', [mat1, (row, col - 1)]))
		if row < 2:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row + 1][col]
			mat1[row + 1][col] = 0
			results.append(('down', [mat1, (row + 1, col)]))
		if col < 2:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row][col + 1]
			mat1[row][col + 1] = 0
			results.append(('right', [mat1, (row, col + 1)]))

		return results

	def print(self):
		solution = self.solution if self.solution is not None else None

		#############   i tried to add tkinter gui here but ended up failing to create a beautiful gui 
		
		# # Initialize the Tkinter window
		# root=tk.Tk()
		# root.title("8-puzzle solution")
        # # Create and pack the labels
		# tk.Label(root, text="Start State: ", font=("Arial", 14)).pack()
		# tk.Label(root, text=str(self.start[0]), font=("Courier", 12), bg="lightgrey").pack(pady=(0, 10))
		# tk.Label(root, text="Goal State:", font=("Arial", 14)).pack()
		# tk.Label(root, text=str(self.goal[0]), font=("Courier", 12), bg="lightgrey").pack(pady=(0, 10))
		# tk.Label(root, text=f"States Explored: {self.num_explored}", font=("Arial", 12)).pack(pady=(0, 10))
		# tk.Label(root, text="Solution:", font=("Arial", 14)).pack()
		# for action, cell in zip(solution[0], solution[1]):
		# 	action_label = tk.Label(root, text=f"Action: {action}", font=("Arial", 12))
		# 	action_label.pack()
		# 	state_label = tk.Label(root, text=str(cell[0]), font=("Courier", 12), bg="lightgrey")
		# 	state_label.pack(pady=(0, 10))
		# tk.Label(root, text="Goal Reached!!", font=("Arial", 14)).pack()
		# root.mainloop()
	
		print("Start State:\n", self.start[0], "\n")
		print("Goal State:\n",  self.goal[0], "\n")
		print("\nStates Explored: ", self.num_explored, "\n")
		print("Solution:\n ")
		for action, cell in zip(solution[0], solution[1]):
			print("action: ", action, "\n", cell[0], "\n")
		print("Goal Reached!!")

	def does_not_contain_state(self, state):
		for st in self.explored:
			if (st[0] == state[0]).all():
				return False
		return True
	
	def solve(self):
		self.num_explored = 0

		start = Node(state=self.start, parent=None, action=None)
		frontier = QueueFrontier()
		frontier.add(start)

		self.explored = [] 

		while True:
			if frontier.empty():
				raise Exception("No solution")

			node = frontier.remove()
			self.num_explored += 1

			if (node.state[0] == self.goal[0]).all():
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions,  cells)
				return

			self.explored.append(node.state)

			for action, state in self.neighbors(node.state):
				if not frontier.contains_state(state) and self.does_not_contain_state(state):
					child = Node(state=state, parent=node, action=action)
					frontier.add(child)


start = np.array([
	[1, 4, 0], 
	[2, 3, 5], 
	[6, 7, 8]
	])
goal = np.array([
	[0, 1, 2], 
	[3, 4, 5], 
	[6, 7, 8]
	])


startIndex = (0, 2)
goalIndex = (0, 0)


p = Puzzle(start, startIndex, goal, goalIndex)
p.solve()
p.print()

# 'U', 'R', 'R', 'D', 'L', 'U', 'L', 'D', 'R', 'R', 'U', 'L', 'L'