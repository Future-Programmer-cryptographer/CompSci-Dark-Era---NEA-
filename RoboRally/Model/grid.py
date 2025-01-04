class Grid: 

    def __init__(self, size, canvas, cell=50): 
        self.size = size 
        self.canvas = canvas 
        self.obstacles = set()
        self.checkpoints = [] 
        self.checkpointIds = {} 

        self.cell = cell 
    
    def placeObstacles(self, obstaclePos):
        for row, col in obstaclePos:
            x1 = col*self.cell 
            y1 = row*self.cell 
            x2 = x1 + self.cell 
            y2 = y1 +self.cell 

            # Draw/render the obstacle 
            self.canvas.create_rectangle(x1,y1,x2,y2,fill='gray', outline='black')
            self.obstacles.add((row, col))
        
    def placeCheckpoints(self, checkpointPos):

        for row, col in checkpointPos:
            x1 = col*self.cell 
            y1 = row*self.cell 
            x2 = x1+self.cell 
            y2 = y1+self.cell 

            checkpointId = self.canvas.create_polygon(
                x1+self.cell /2, y1+self.cell /4, 
                x1+self.cell /4, y1+3*self.cell /4, 
                x1+3*self.cell /4, y1+3*self.cell /4, 
                fill='green', 
                outline='black'
            )
            self.checkpointIds[(row, col)] = checkpointId
            self.checkpoints.append((row, col))
        