class CardModel: 
    def __init__(self, action, number):
        self.action = action # being forward, backward, left, right
        self.number = number # being 1,2,3 of each of the action 
    


class RegisterModel: 
    def __init__(self):
        self.card = None # Holds the card assinged to the register 
