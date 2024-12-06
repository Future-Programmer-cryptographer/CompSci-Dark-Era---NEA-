from View.playGameView import PlayGameView
from Model.playGameModel import PlayGameModel

class PlayGameController: 
    def __init__(self):
        self.mainMenuController = None 
        self.playGameModel = None 
        self.playGameView = None 
    
    # self is the controller 
    def initialiseView(self, root):
        PlayGameView(root, self) 
    
    def submitCards(self, cards):
        pass 
    # basicaly, when the user clicks on the submit button, we want to send this msg of to the controller and return the cards that we submitted 