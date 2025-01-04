class Robot: 

    def __init__(self, name, colour, startPos):
        self.name = name 
        self.colour = colour 
        self.position = startPos 
        self.health = 5 
        self.moveHistory = [] 
    
    def updatePosition(self, newPos):
        self.position = newPos 
    
    def recordMove(self, moveDetails):
        self.moveHistory.append(moveDetails)