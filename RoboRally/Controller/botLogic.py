import random 

# this is the function called by playGameController 
def generateBotMoves(botPos, checkpoints, obstacles, gridSize):

    path = aStar(botPos, checkpoints, obstacles, gridSize)

    # if a* doesn't work, resort to stupid bot moves
    if not path: 
        return generateRandomBotMoves()
    
    botCommands = [] 

    # this is so that the bot can make either 1,2 or 3 steps per turn (some element of randomness)
    num = random.randint(1,3)

    for direction, steps in path[:num]:
        botCommands.append({'direction': direction, 'steps':steps})
    return botCommands 

def generateRandomBotMoves():
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        botCommands = [] 

        commands = random.randint(1,3)

        # randomly make either 1, 2 or 3 moves, select a random directions and random number of steps between 1-3 inclusive 

        for _ in range(commands):
            direction = random.choice(directions)
            steps = random.randint(1,3)
            botCommands.append({'direction': direction, 'steps':steps})
        return botCommands


# class node to represent each grid pos 
class Node: 
    def __init__(self, x, y, isObstacle=False):
        self.x = x 
        self.y = y 
        self.isObstacle = isObstacle

        # g score = cost from start to a given node, 
        # f score = estimated total cost (g+h)
        self.gScore = float('inf')
        self.fScore = float('inf')

        # parent node to reconstrct the path 
        self.parent = None 
        
    # checks if two nodes have the same coords 
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y 

    # compares nodes based on f-score for sorting purposes 
    def __lt__(self, other):
         return self.fScore < other.fScore


# hScore = heuristic, in this case it's the absolute sum of distance between coords (Manhattan distance)
def hScore(node, goal):
     return abs(goal.x - node.x) + abs(goal.y - node.y)

# get all possible neighbours ofa given node 
def getNeighbours(node, gridSize, obstacles):
    directions =  {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
    neighbours = []

    for direction, (dx,dy) in directions.items():
        newX,newY = node.x+dx , node.y+dy

        # make sure new pos is within the grid and not an obstacle and add that pos as a valid neighbour 
        if 0 <=newX < gridSize and 0 <= newY < gridSize and (newX, newY) not in obstacles:
            neighbours.append((Node(newX, newY), direction))
    return neighbours    

def aStar(botPos, checkpoints, obstacles, gridSize):

    # check for cp's
    if not checkpoints: 
         return [] 

    # convert bot pos and nearest cp's to nodes 
    startNode = Node(botPos[0], botPos[1])
    goalNode = min(checkpoints, key=lambda cp:abs(botPos[0]-cp[0]) + abs(botPos[1] -cp[1]))
    goalNode = Node(goalNode[0], goalNode[1])

    # open set = nodes that need to be explored (implemented as a priority queue)
    # closed set = nodes that have already been explored 
    openSet = [startNode]
    closedSet = set() 
    startNode.gScore = 0 
    startNode.fScore = hScore(startNode, goalNode)

    while openSet: 
        # start by picking node with lowest fScore 
        current = min(openSet, key=lambda node: node.fScore)
        openSet.remove(current)
        closedSet.add((current.x, current.y))

        # if goal found, reconstruct path 
        if current == goalNode: 
            return reconstructPath(current) 
        
        # expore valid neighbour nodes (and ignore already explored nodes)
        for neighbour, direction in getNeighbours(current, gridSize, obstacles):
            if (neighbour.x, neighbour.y) in closedSet:
                continue 
        
            # movement cost for 1 
            tentative_g = current.gScore + 1 

            # add new nodes to explore 
            if neighbour not in openSet:
                openSet.append(neighbour)
            elif tentative_g >= neighbour.gScore: 
                continue 

            # update neighbour + scores 
            neighbour.parent = current 
            neighbour.gScore = tentative_g
            neighbour.fScore = neighbour.gScore + hScore(neighbour, goalNode)
    
    # return [] if no path is found          
    return [] 
         
# essentially backtracking from goal to start 
def reconstructPath(current):
    path = [] 
    while current.parent: 
        dx = current.x - current.parent.x 
        dy = current.y - current.parent.y 

        # direction is based on coordinate change 
        if dx == -1:
            direction = 'UP'
        elif dx == 1:
            direction = 'DOWN'
        elif dy == -1:
            direction = 'LEFT'
        else:
            direction = 'RIGHT'
        
        # currently storing movement 1 step at a time 
        path.append((direction, 1))
        current = current.parent 
    
    # reverse path from start to goal 
    return path[::-1]

