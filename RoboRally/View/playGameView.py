from tkinter import * 
from PIL import Image, ImageTk 
import tkinter as tk 
from tkinter import ttk 

# need a board selection screen with different difficulty 
# need to have three different boards - tkinter framing... 
# after they have selected the boards, we want them to select single player vs bot or multiplayer 

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
    
    def showSelectBoardWindow(self):
        self.selectBoardFrame.pack(fill=tk.BOTH)
    
    def updateMoveHistory(self, history):
        self.moveHistoryTxt.configure(state='normal')
        self.moveHistoryTxt.delete(1.0, tk.END)

        # populate the text box 
        for move in history: 
            direction = move['direction']
            steps = move['steps']
            start = move['start']
            end = move['end']
            self.moveHistoryTxt.insert(tk.END, f'{steps} steps {direction} from {start} to {end} \n')
        
        self.moveHistoryTxt.configure(state='disabled')
    
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

        # Move history text box
        self.moveHistoryTxt = tk.Text(self.gameBoardFrame, width=60, height=10, state='disabled')
        self.moveHistoryTxt.pack()

        # # creating another frame - left for grid and right for move history 
        # gridFrame = tk.Frame(self.gameBoardFrame)
        # gridFrame.grid(row=0, column=0, padx=10, pady=10)

        # historyFrame = tk.Frame(self.gameBoardFrame)
        # historyFrame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # # Move history label
        # historyLabel = ttk.Label(historyFrame, text='Move history')
        # historyLabel.pack(pady=5)

        # # Move history text box
        # self.moveHistoryTxt = tk.Text(historyFrame, width=30, height=20, state='disabled')
        # self.moveHistoryTxt.pack()

        # creating a back button 
        backBtn = ttk.Button(
            self.root, 
            text='Back to Options Menu', 
            command = self.playGameController.backToOptions
        )
        backBtn.pack(pady=10)

        # # pack the canvas 
        # self.canvas.pack(in_=gridFrame, fill=tk.BOTH, expand=True) 

        self.canvas.pack() 
    
        # make the game grid and registers/cards 
        self.playGameController.makeGrid()
        self.playGameController.makeRegistersAndCards()
    

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

