import time 
from checkSolvability import is_solvable

#display board
def displayBoard(state):
    print("--------------")
    print("| %i | %i | %i |" % (state[0], state[1], state[2]))
    print("--------------")
    print("| %i | %i | %i |" % (state[3], state[4], state[5]))
    print("--------------")
    print("| %i | %i | %i |" % (state[6], state[7], state[8]))
    print("--------------")

#structure of node
class Node:
    def __init__(self, state, parent, action, depth, cost):
        self.state=state  #current node
        self.parent=parent  # parent node
        self.action=action  # the action that generated this state
        self.depth=depth  # depth of this state
        self.cost=cost  #path cost
        
    def getState(self):
        return self.state
    def getParent(self):
        return self.parent
    def getMoves(self):
        return self.action
    def getCost(self):
        return self.cost
    
    def pathFromStart(self):
        stateList = []
        movesList = []
        currNode = self
        while currNode.getMoves() is not None:
            stateList.append(currNode.getState())
            movesList.append(currNode.getMoves())
            currNode = currNode.parent
        movesList.reverse()
        stateList.reverse()

        for state, moves in zip(stateList,movesList):
            print("move: ",moves)
            displayBoard(state)
        return movesList
    
def createNode(startState, parent, action, depth, cost):
    return Node(startState, parent, action, depth, cost)

def moveUp(state):
    newState= state[:]
    index = newState.index(0)
    if index not in [0,1,2]:
        temp = newState[index-3]
        newState[index-3]=newState[index]
        newState[index]=temp
        return newState
    else: return None

def moveDown(state):
    newState= state[:]
    index = newState.index(0)
    if index not in [6,7,8]:
        temp = newState[index+3]
        newState[index+3]=newState[index]
        newState[index]=temp
        return newState
    else: return None

def moveLeft(state):
    newState= state[:]
    index = newState.index(0)
    if index not in [0,3,6]:
        temp = newState[index-1]
        newState[index-1]=newState[index]
        newState[index]=temp
        return newState
    else: return None

def moveRight(state):
    newState= state[:]
    index = newState.index(0)
    if index not in [2,5,8]:
        temp = newState[index+1]
        newState[index+1]=newState[index]
        newState[index]=temp
        return newState
    else: return None
 
def expandedNodes(node):
    expaned_nodes = []
    expaned_nodes.append(createNode(moveUp(node.state), node, "up", node.depth+1, 0))
    expaned_nodes.append(createNode(moveDown(node.state), node, "down", node.depth+1, 0))
    expaned_nodes.append(createNode(moveLeft(node.state), node, "left", node.depth+1, 0))
    expaned_nodes.append(createNode(moveRight(node.state), node, "right", node.depth+1, 0))

    #if the node is not possible then move function will return none. so i am filtering none
    expaned_nodes = [node for node in expaned_nodes if node.state != None]
    return expaned_nodes

def dfs(startState, goalState):
   
    # this act as a stack
    nodes = []
    #insert the root node
    nodes.append(createNode(startState, None, None, 0, 0))
    count = 0
    explored = []
    while nodes:
        node =  nodes.pop(0)
        count+=1
        explored.append(node.getState())
        # print("current state", node.state, " move: ", node.action)

        if node.state == goalState:
            print("done. the number of nodes visited: ",count)
            print("states of the moves: ")
            return node.pathFromStart()
        else:
            expanded_nodes= expandedNodes(node)
            for item in expanded_nodes:
                state= item.getState()
                if state not in explored:
                    nodes.insert(0,item)


def main():
    #defined the start state
    startState=[1,2,3,0,4,5,6,7,8]
    goalState = [1,2,3,4,5,6,7,8,0]

    if not is_solvable(startState):
        return
    #start time
    start = time.time()
    result = dfs(startState,goalState)
    #end time
    end = time.time()
    #calculate total time
    totalTime = end-start
    if result == None:
        print("No solution found")
    elif result == [None]:
        print("start node was the goal node")
    else:
        # print(result)
        print(len(result), "moves")
    print("total time: %.5f" %(totalTime))

#the starting function
if __name__ == "__main__":
    main()
