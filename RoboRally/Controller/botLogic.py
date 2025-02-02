import random 

# https://github.com/AaronHe7/pathfinder/blob/master/a_star.py


def generateBotMoves(botPos, checkpoints, obstacles, gridSize):

    path = aStar(botPos, checkpoints, obstacles, gridSize)

    # if a* doesn't work, resort to stupid bot moves
    if not path: 
        return generateRandomBotMoves()
    
    botCommands = [] 

    num = random.randint(2,3)

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


class Node: 
    def __init__(self, x, y, isObstacle=False):
        self.x = x 
        self.y = y 
        self.isObstacle = isObstacle

        # g score = cost from start to a given node, 
        # f score = estimated total cost (g+h)
        self.gScore = float('inf')
        self.fScore = float('inf')

        # in case we need to reconstrct the path 
        self.parent = None 
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y 

    def __lt__(self, other):
         return self.fScore < other.fScore


def hScore(node, goal):
     # Manhattan heuristic 
     return abs(goal.x - node.x) + abs(goal.y - node.y)

def getNeighbours(node, gridSize, obstacles):
    # return all possible neighbours 
    directions =  {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
    neighbours = []

    for direction, (dx,dy) in directions.items():
        newX,newY = node.x+dx , node.y+dy
        if 0 <=newX < gridSize and 0 <= newY < gridSize and (newX, newY) not in obstacles:
            # append neighbour + directions of neighbour 
            neighbours.append((Node(newX, newY), direction))
    return neighbours    

def aStar(botPos, checkpoints, obstacles, gridSize):
    if not checkpoints: 
         return [] 

    # convert to nodes 
    startNode = Node(botPos[0], botPos[1])
    goalNode = min(checkpoints, key=lambda cp:abs(botPos[0]-cp[0]) + abs(botPos[1] -cp[1]))
    goalNode = Node(goalNode[0], goalNode[1])

    # nodes to explore are gonna be in the open set 
    openSet = [startNode]
    closedSet = set() 
    startNode.gScore = 0 
    startNode.fScore = hScore(startNode, goalNode)

    while openSet: 
        current = min(openSet, key=lambda node: node.fScore)
        openSet.remove(current)
        closedSet.add((current.x, current.y))

        if current == goalNode: 
            return reconstructPath(current) 
        
        for neighbour, direction in getNeighbours(current, gridSize, obstacles):
            if (neighbour.x, neighbour.y) in closedSet:
                continue 
        
            # movemnet cost is 1 
            tentative_g = current.gScore + 1 

            if neighbour not in openSet:
                openSet.append(neighbour)
            
            elif tentative_g >= neighbour.gScore: 
                continue 

            # update neighbour 
            neighbour.parent = current 
            neighbour.gScore = tentative_g
            neighbour.fScore = neighbour.gScore + hScore(neighbour, goalNode)
    
    # if no path found         
    return [] 
         
def reconstructPath(current):
    path = [] 
    while current.parent: 
        dx = current.x - current.parent.x 
        dy = current.y - current.parent.y 
        if dx == -1:
            direction = 'UP'
        elif dx == 1:
            direction = 'DOWN'
        elif dy == -1:
            direction = 'LEFT'
        else:
            direction = 'RIGHT'
        path.append((direction, 1))
        current = current.parent 
    return path[::-1]

