import heapq
import time

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def size(self):
        return len(self.elements)
    def empty(self):
        return len(self.elements) == 0
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    def get(self):
        return heapq.heappop(self.elements)[1]
    def pop(self):
        return heapq.heappop(self.elements)[1] if self.size() > 0 else None
    
global goal 
goal= [[1,2,3], [4,5,6],[7,8,'x']]   

class Node:
    def __init__(self, currentState, g, h, previousState = None):
        self.currentState = currentState
        self.g = g
        self.h = self.heuristic(currentState)
        self.previousState = previousState
    
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)
    
    def childStates(self):
        x,y = self.findBlank()
        moves = [[x+1,y], [x-1,y], [x,y+1], [x,y-1]]
        children = []
        for i in moves:
            x1,y1 = i[0],i[1]
            board = self.currentState.copy()
            new_board = [row[:] for row in board]  
            child = self.move(new_board, x, y, x1, y1)  
            if child is not None:
                child_node = Node(child, self.g + 1, self.h, self)
                children.append(child_node)

        return children       
    
    def findBlank(self):
        for row in range(len(self.currentState)):
            for col in range (len(self.currentState[row])):
                if self.currentState[row][col] == 'x':
                    return row,col
        
    def move(self, board, x, y, x1, y1):
        if x1 >=0 and x1 < len(board) and y1>=0 and y1 < len(board):
            temp_board = []
            temp_board = board.copy()
            temp = temp_board[x1][y1]
            temp_board[x1][y1] =  temp_board[x][y]
            temp_board[x][y] = temp
            return temp_board
        else:
            return None
    def heuristic(self, currentState):
        distance = 0
        for row in range(len(currentState)):
            for col in range(len(currentState[row])):
                if currentState[row][col] != 'x':
                    val = currentState[row][col]
                    exceptedval = getPos(goal, val)
                    distance += abs(row - exceptedval[0]) + abs(col - exceptedval[1])
        return distance
        
    

def getPos(currentState, element):
    for row in range (len(currentState)):
        if element in currentState[row]:
            return (row, currentState[row].index(element))
    
                     
board = [['-','-','-'],
         ['-','-','-'],
         ['-','-','-']]

print("Enter Board from top to left, press Enter to send number to board. For your blank space enter 'x'.")
for row in range(len(board)):
    for col in range (len(board[row])):
        print(board)
        i = input()
        if i == 'x':
            board[row][col] = 'x'
        else:
            board[row][col] = int(i)
print("Your Board: ", board)
print("testing possible moves")
path = []
open_list = PriorityQueue()
visited = set()
starting_node = Node(board, 0, 0, None)

# Add First Node
open_list.put(starting_node, 0)


while not open_list.empty():
    n = open_list.get()
    if n.currentState == goal:
        print(f'Found Answer: {n.currentState} g: {n.g} h: {n.h}')
        print()
        goal_node = n
        while goal_node.previousState:
            previousnode = goal_node
            path.append(previousnode.currentState)
            goal_node = previousnode.previousState
        path.reverse()
        for x in range (len(path)):
            print(f'Correct Path: {path[x]}')
        break
    # Visited Check
    children = n.childStates()
    if not children:
        break
    children = [node for node in children if tuple(map(tuple, node.currentState)) not in visited]
    for node in children:
        visited.add(tuple(map(tuple, node.currentState)))
    for child in children:
            open_list.put(child, child.g + child.h)
    