from tkinter import * 
from PIL import Image, ImageTk 
import tkinter as tk 
from tkinter import ttk 

# need a board selection screen with different difficulty 
# need to have three different boards - tkinter framing... 
# after they have selected the boards, we want them to select single player vs bot or multiplayer 

# set up a while loop... the when the user clicks on any option, we want to ask them if they want single player or multiplayer, just do it with one board..., then we want to have them play the game on that screen. 

class PlayGameView: 

    def __init__(self, root, canvas, playGameController):
        self.root = root 
        self.canvas = canvas 
        self.playGameController = playGameController 
        self.root.title('Select game board')

        # creating another frame 
        self.selectBoardFrame = tk.Frame(self.root)

        titleLabel = ttk.Label(self.selectBoardFrame, text='Select one of the three boards for single/multiplayer')
        titleLabel.pack(pady=10)

        # importing an image - this is a board  
        # boardImage = Image.open('Images/board1.png').resize((300,300))
        # imageTk = ImageTk.PhotoImage(boardImage)

        # button widget 
        button = ttk.Button(self.selectBoardFrame, 
                            text='Example board', 
                            command=self.playGameController.onBoardSelect)
        button.pack() 

        # self.optionWindowFrame.pack_forget() 
    
    def showSelectBoardWindow(self):
        self.selectBoardFrame.pack(fill=tk.BOTH)
    
    def showOptionWindow(self): 

        self.selectBoardFrame.pack_forget() 

        # creating an options window frame
        self.optionWindowFrame = tk.Frame(self.root)
        self.optionWindowFrame.pack(fill=tk.BOTH)

        self.root.title('Choose Game option')

        singlePlayerBtn = ttk.Button(self.optionWindowFrame, 
                                     text='Single Player', 
                                     command=self.playGameController.onSinglePlayerSelect)
        singlePlayerBtn.pack(pady=10)

        multiplayerBtn = ttk.Button(self.optionWindowFrame, 
                                     text='Multiplayer', 
                                     command=self.playGameController.onMultiplayerSelect)
        multiplayerBtn.pack(pady=10)
    
    def showGameBoard(self, isSinglePlayer=True):

        self.optionWindowFrame.pack_forget() 

        # creating game board frame
        self.gameBoardFrame = tk.Frame(self.root)
        self.gameBoardFrame.pack(fill=tk.BOTH)

        self.root.title('Single player' if isSinglePlayer else 'Multiplayer')

        # creating a back button 
        backBtn = ttk.Button(
            self.gameBoardFrame, 
            text='Back to Options Menu', 
            command = self.playGameController.backToOptions
        )
        backBtn.pack(pady=10)

        # pack the canvas 
        self.canvas.pack() 
    
        # make the game grid and registers/cards 
        self.playGameController.makeGrid(self.gameBoardFrame)
        self.playGameController.makeRegistersAndCards(self.gameBoardFrame)
    

    def getCoordinates(self):
        # for the time being, user clicks on a square, I want to get the coordinates of that square 
        pass 

    def placeObstacles(self):
       pass  
    # takes in parameters to place obstacles 

    def createCheckpoints(self):
        pass 
    # randomsise it 
        
    def startPoint(self):
        pass 

    def checkWin(self): 
        pass 

    def moveHistory(self): 
        pass 
    
    def saveGame(self):
        pass 

