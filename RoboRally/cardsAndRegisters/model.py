class CardModel: 
    def __init__(self, direction, steps):
        self.direction = direction # being forward, backward, left, right
        self.steps = steps # being 1,2,3 of each of the action 
    


class RegisterModel: 
    def __init__(self):
        self.card = None # Holds the card assinged to the register 
