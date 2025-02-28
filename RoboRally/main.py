import tkinter as tk
from Controller.mainMenuController import MainMenuController
from View.mainMenuView import MainMenuView
from Controller.playGameController import PlayGameController
from Controller.leaderboardController import LeaderboardController

def main():
    # Initialize root window
    root = tk.Tk()

    # Create a canvas for drawing
    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=1, highlightbackground="black")

    # initialise controllers and model
    mainMenuController = MainMenuController(None)
    playGameController = PlayGameController(root, canvas)
    leaderboardController = LeaderboardController(root, canvas)
    mainMenuView = MainMenuView(root, mainMenuController)

    # Subscribe 
    mainMenuController.mainMenuView = mainMenuView
    mainMenuController.playGameController = playGameController  
    playGameController.mainMenuController = mainMenuController
    leaderboardController.mainMenuController = mainMenuController
    mainMenuController.leaderboardController = leaderboardController
    
    # treating main.py as the 'master view' 
    root.mainloop()

main()
