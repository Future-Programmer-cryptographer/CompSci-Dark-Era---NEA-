import tkinter as tk
from Controller.mainMenuController import MainMenuController
from View.mainMenuView import MainMenuView
from Controller.playGameController import PlayGameController
from Model.playGameModel import PlayGameModel
from View.playGameView import PlayGameView

def main():
    # Initialize root window
    root = tk.Tk()

    # Create a canvas for drawing
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()

    # initialise PlayGameView
    playGameView = PlayGameView(root, PlayGameController)

    # initialise controllers and model
    mainMenuController = MainMenuController(None)
    playGameController = PlayGameController(root, playGameView, canvas)
    mainMenuView = MainMenuView(mainMenuController)
    playGameModel = PlayGameModel()

    # Subscribe 
    mainMenuController.mainMenuView = mainMenuView
    mainMenuController.playGameController = playGameController  
    playGameController.mainMenuController = mainMenuController
    playGameController.playGameModel = playGameModel

    # Start the main application loop
    mainMenuView.mainloop()

main()
