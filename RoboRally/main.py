import tkinter as tk
from Controller.mainMenuController import MainMenuController
from View.mainMenuView import MainMenuView
from Controller.playGameController import PlayGameController
from Model.playGameModel import PlayGameModel

def main():
    # Initialize root window
    root = tk.Tk()

    # Create a canvas for drawing
    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=1, highlightbackground="black")
    # canvas.pack()

    # initialise PlayGameView
    # playGameView = PlayGameView(root, canvas, PlayGameController)

    # initialise controllers and model
    mainMenuController = MainMenuController(None)
    playGameController = PlayGameController(root, canvas)
    mainMenuView = MainMenuView(root, mainMenuController)
    playGameModel = PlayGameModel()

    # Subscribe 
    mainMenuController.mainMenuView = mainMenuView
    mainMenuController.playGameController = playGameController  
    playGameController.mainMenuController = mainMenuController
    playGameController.playGameModel = playGameModel

    # treating main.py as the 'master view' 
    root.mainloop()

main()
