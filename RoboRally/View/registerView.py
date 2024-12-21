class RegisterView: 
    def __init__(self, canvas, x, y, width, height, colour='blue'):
        self.canvas = canvas 
        self.cardId = self.canvas.create_rectangle(x, y, x+width, y+height, outline=colour)
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
    
    def getCentre(self):
        return (self.x + self.width /2, self.y + self.height /2)
    
