class CardView: 
    def __init__(self, canvas, x, y, width, height, text, colour='light blue'):
        self.canvas = canvas
        self.cardId = self.canvas.create_rectangle(x,
                                                   y, 
                                                   x+width, 
                                                   y+height, 
                                                   fill=colour)
        self.textId = self.canvas.create_text(x+width//2, 
                                              y+height //2,
                                              text=text,
                                              anchor='center')

    def move(self, canvas, dx,dy):
        canvas.move(self.cardId, dx, dy)
        canvas.move(self.textId, dx, dy)
    
    def getPosition(self, canvas):
        coords = canvas.coords(self.cardId) # this will return [x1, y1, x2,y2]
        x,y = coords[0], coords[1]
        return x,y 
    
class RegisterView: 
    def __init__(self, canvas, x, y, width, height, colour='black'):
        self.canvas = canvas 
        self.cardId = self.canvas.create_rectangle(x, y, x+width, y+height, outline=colour)
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
    
    def getCentre(self):
        return (self.x + self.width /2, self.y + self.height /2)
    
