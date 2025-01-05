from View.playGameView import PlayGameView

class DragAndDropController:

    def __init__(self, canvas):
        self.canvas = canvas 
        self.start_x = 0
        self.start_y = 0
    
    def startDrag(self, event, cardView):
        self.start_x = event.x
        self.start_y = event.y 
    
    def continueDrag(self, event, cardView):
        dx = event.x - self.start_x 
        dy = event.y - self.start_y 
        cardView.move(self.canvas, dx, dy)
        self.start_x = event.x 
        self.start_y = event.y 
    
    def endDrag(self, event, cardView, cards, registers):
        # Snap to the closest register
        closestRegister = self.findClosestRegister(event.x, event.y, registers)
        if closestRegister:
            register = closestRegister['view']
            # Move card to register
            dx = register.x - cardView.getPosition(self.canvas)[0]
            dy = register.y - cardView.getPosition(self.canvas)[1]
            cardView.move(self.canvas, dx, dy)
            # Find card model in self.cards 
            cardModel = None
            for card in cards: 
                if card['view'] == cardView: 
                    cardModel = card['model']
                    break 

            # assingn card model to register model 
            if cardModel: 
                closestRegister['model'].card = cardModel
    
    def findClosestRegister(self, x, y, registers):
        closestRegister = None
        minDistance = float('inf')

        for register in registers:
            centre_x, centre_y = register['view'].getCentre()
            distance = ((x - centre_x) ** 2 + (y - centre_y) ** 2) ** 0.5
            if distance < minDistance:
                minDistance = distance
                closestRegister = register

        return closestRegister