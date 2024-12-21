class CardModel: 
    def __init__(self, action, number):
        self.action = action # being forward, backward, left, right
        self.number = number # being 1,2,3 of each of the action 
    
    def __str__(self):
        return f'{self.number} {self.action}'