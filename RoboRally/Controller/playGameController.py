from View.playGameView import PlayGameView
from Model.playGameModel import PlayGameModel

class PlayGameController: 
    def __init__(self, playGameModel, playGameView):
        self.playGameView = playGameView
        self.playGameModel = playGameModel