
from Controller.mainMenuController import MainMenuController 
from View.mainMenuView import MainMenuView
from Controller.playGameController import PlayGameController
from Model.playGameModel import PlayGameModel

def main():     
    mainMenuController = MainMenuController(None) 
    playGameController = PlayGameController()
    mainMenuView = MainMenuView(mainMenuController) 
    playGameModel = PlayGameModel() 

    # view is set in the controller 
    mainMenuController.mainMenuView = mainMenuView 

    # subscribing to playGameController  
    mainMenuController.playGameController = playGameController

    # playGameController subscribing to mainMenuController  
    playGameController.mainMenuController = mainMenuController

    # playgameController to subscribe to model 
    playGameController.playGameModel = playGameModel 

    mainMenuView.mainloop() 

main() 
