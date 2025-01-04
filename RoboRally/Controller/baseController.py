class BaseController: 

    def __init__(self):
        self._currentTurn = 1 
        self._animationSpeed = 500 
    
    def incrementTurn(self):
        self._currentTurn +=1  
    
    def currentTurn(self):
        return self._currentTurn