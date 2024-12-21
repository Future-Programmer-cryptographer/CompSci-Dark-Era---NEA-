class CardView: 
    def __init__(self, canvas, x, y, width, height, colour='blue'):
        self.canvas = canvas
        self.cardId = self.canvas.create_rectangle(x,y, x+width, y+height, fill=colour)

    def move(self, dx,dy):
        self.canvas.move(self.cardId, dx, dy)

    def getPosition(self):
        coords = self.canvas.coords(self.cardId)
        return {

            'x' : coords[0], 
            'y' : coords[1]
        }    

    def snapTo(self, x, y, width, height):
        self.canvas.coords(self.cardId, x, y, x+width, y+height)
    