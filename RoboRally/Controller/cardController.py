class CardController: 
    def __init__(self, canvas, cardModel, cardView):
        self.model = cardModel
        self.view = cardView 
        self.canvas = canvas 

        # binding drag n drop stuff 
        self.canvas.tag_bind(self.view.cardId, '<ButtonPress-1>', self.startDrag)
        self.canvas.tag_bind(self.view.cardId, '<B1-Motion>', self.continueDrag)
        self.canvas.tag_bind(self.view.cardId, '<ButtonRelease-1>', self.endDrag)
    
        self.start_x = 0 
        self.start_y = 0 
    
    def startDrag(self, event):
        self.start_x = event.x
        self.start_y = event.y 
    
    def continueDrag(self, event):
        dx = event.x - self.start_x 
        dy = event.y - self.start_y 
        self.view.move(dx, dy)
        self.start_x = event.x 
        self.start_y = event.y 
    
    def endDrag(self, event):
        # snap to closest register 
        closestRegister = self.findClosestRegister(event.x, event.y)
        if closestRegister: 
            self.view.snapTo(
                closestRegister.x, 
                closestRegister.y, 
                closestRegister.width, 
                closestRegister.height,
            )
    
    def findClosestRegister(self, x, y):
        closestRegister = None 
        minDistance = float('inf')

        # go through register and calculate distance between card current pos and centre of each reg
        # pythag 

        for register in self.registers: 
            centre_x, centre_y = register.getCentre()
            distance = ((x - centre_x) ** 2) + ((y-centre_y) **2) ** 0.5 
            if distance < minDistance: 
                minDistance = distance
                closestRegister = register
            
        return closestRegister
