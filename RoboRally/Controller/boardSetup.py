import random 

class BoardSetup: 
    def __init__(self, canvas, size=10, cell=50):
        self.canvas = canvas
        self.size = size
        self.cell = cell
        self.obstacles = set()
        self.checkpoints = []
    
    def createBoard(self, playerCount, isMultiplayer):
        self.placeObstacles(5)
        self.placeCheckpoints(10)
        