from tkinter import * 
from PIL import Image, ImageTk 
import tkinter as tk 
from tkinter import ttk 
from View.registerHandling import Register
from Controller.dragAndDrop import DragAndDrop

# need a board selection screen with different difficulty 
# need to have three different boards - tkinter framing... 
# after they have selected the boards, we want them to select single player vs bot or multiplayer 

# set up a while loop... the when the user clicks on any option, we want to ask them if they want single player or multiplayer, just do it with one board..., then we want to have them play the game on that screen. 

class PlayGameView: 
    def __init__(self, root):
        self.root = root 
        self.root.title('Select game board')

        # creating another frame 
        self.selectBoardFrame = tk.Frame(self.root)
        self.selectBoardFrame.pack(fill=tk.BOTH)

        titleLabel = ttk.Label(self.selectBoardFrame, text='Select one of the three boards for single/multiplayer game')
        titleLabel.pack(pady=10)

        # importing an image - this is a board  
        boardImage = Image.open('Images/board1.png').resize((300,300))
        imageTk = ImageTk.PhotoImage(boardImage)

        # button widget 
        button = ttk.Button(self.selectBoardFrame, 
                            text='Example board', 
                            image=imageTk, 
                            command=self.optionWindow)
        button.pack() 
    
    def optionWindow(self): 
        self.selectBoardFrame.pack_forget() 

        # creating an options window frame
        self.optionWindowFrame = tk.Frame(self.root)
        self.optionWindowFrame.pack(fill=tk.BOTH)

        self.root.title('Choose Game option')

        singlePlayerBtn = ttk.Button(self.optionWindowFrame, 
                                     text='Single Player', 
                                     command=self.makeSingleplayerBoard)
        singlePlayerBtn.pack(pady=10)

        multiplayerBtn = ttk.Button(self.optionWindowFrame, 
                                     text='Multiplayer', 
                                     command=self.makeMultiplayerBoard)
        multiplayerBtn.pack(pady=10)

    # HOW DO I MAKE SURE I ONLY RUN THIS PART OF THE PROGRAM
    def makeGrid(self, window):
        # want to see rank-file style numbering 
        # size is 10 by 10 to start with
        # ask user to input a grid later

        size = 10
        cell = 20 
        # want the grid on the same canvas? 
        gridCanvas = tk.Canvas(window, width=cell*(size+1), height=cell*(size+1))
        gridCanvas.pack() 

        # drawing the actual grid 
        for i in range(size):
            for j in range(size): 
                x1 = (j+1) * cell 
                y1 = (i+1) * cell
                x2 = x1 + cell 
                y2 = y1 + cell

                gridCanvas.create_rectangle(x1,y1,x2,y2, fill='pink', outline='black')

        # letters 
        for col in range(size):
            x = (col+1) * cell + cell / 2 
            y = cell /2  
            file = chr(65+col) # convert 0-9 to letters 
            gridCanvas.create_text(x,y,text=file) 
        
        # number labels 
        for row in range(size):
            x = cell / 2 
            y = (row+1) * cell + cell / 2 
            rank = str(row+1)
            gridCanvas.create_text(x,y,text=rank)
        
        return gridCanvas
    
    def getCoordinates(self):
        # for the time being, user clicks on a square, I want to get the coordinates of that square 
        pass 

    def placeObstacles(self):
       pass  
    # takes in parameters to place obstacles 

    def createCheckpoints(self):
        pass 
    # randomsize it 

    def createRegister(self, window): 
        self.window = window
        # main register canvas 
        self.canvas = tk.Canvas(window, width=1000, height=1000, bg='light blue') 
        self.canvas.registers = [] 
        self.canvas.pack() 

        regWidth = 100 
        regHeight = 200 

        for i in range(3):
            Register(self.canvas, 
                     50+i*150, 50, 
                     regWidth, regHeight)
            
        # all possible cards here 
        self.cards = [
            DragAndDrop(self.canvas, 'Images/image1.png', 100,400, regWidth, regHeight),
            DragAndDrop(self.canvas, 'Images/image1.png', 350,400, regWidth, regHeight),
            DragAndDrop(self.canvas, 'Images/image3.png', 600,400, regWidth, regHeight)
        ]
        
    def startPoint(self):
        pass 

    def makeSingleplayerBoard(self):
        self.optionWindowFrame.pack_forget() 

        # single player board frame 
        self.singlePlayerFrame = tk.Frame(self.root)
        self.singlePlayerFrame.pack(fill=tk.BOTH)

        self.root.title('Single Player vs Bot')

        self.View.makeGrid(self.singlePlayerFrame) 
        self.createRegister(self.singlePlayerFrame) 

        # creating a back button - NEEDS TO BE IN THE CONTROLLER 
        backtoOptionsBtn = ttk.Button(self.singlePlayerFrame, 
                                    text='Back to Options menu',
                                    command=print('This needs to be in the controller')) 
        backtoOptionsBtn.pack(pady=10)

    def makeMultiplayerBoard(self): 
        pass 
        # multiplyer functionality 

    def checkWin(self): 
        pass 

    def moveHistory(self): 
        pass 
    
    def saveGame(self):
        pass 

