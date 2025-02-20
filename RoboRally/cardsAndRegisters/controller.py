class DragAndDropController:
    def __init__(self, canvas):

        # initialises a controller which handles the movement of cards in the cards canvas 

        self.canvas = canvas 
        self.start_x = 0
        self.start_y = 0
    
    def startDrag(self, event, cardView):
        self.start_x = event.x
        self.start_y = event.y 
    
    def continueDrag(self, event, cardView):
        # calculate the displacement and move the card by that displacement 
        dx = event.x - self.start_x 
        dy = event.y - self.start_y 
        cardView.move(self.canvas, dx, dy)

        # update the start poitn for next move 
        self.start_x = event.x 
        self.start_y = event.y 
    
    def endDrag(self, event, cardView, cards, registers):

        # complete the drag and drop process by snapping the card to the nearest register 
        closestRegister = self.findClosestRegister(event.x, event.y, registers)
        if closestRegister:
            register = closestRegister['view']
            # move card to register
            dx = register.x - cardView.getPosition(self.canvas)[0]
            dy = register.y - cardView.getPosition(self.canvas)[1]
            cardView.move(self.canvas, dx, dy)
            # find card model in self.cards 
            cardModel = None
            for card in cards: 
                if card['view'] == cardView: 
                    cardModel = card['model']
                    break 

            # assingn card model to register model 
            if cardModel: 
                closestRegister['model'].card = cardModel
    
    def findClosestRegister(self, x, y, registers):
        # find the register whose centre is closest the card being dragged 
        closestRegister = None
        minDistance = float('inf')

        # itereate through each register to find the one with the least distance (using pythagoras)
        for register in registers:
            centre_x, centre_y = register['view'].getCentre()
            distance = ((x - centre_x) ** 2 + (y - centre_y) ** 2) ** 0.5
            if distance < minDistance:
                minDistance = distance
                closestRegister = register

        return closestRegister
    

