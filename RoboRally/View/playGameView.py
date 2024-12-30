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

        # creating game board frame with GRID layout 
        self.gameBoardFrame = tk.Frame(self.root, highlightbackground="black",highlightthickness=1)
        self.gameBoardFrame.pack(fill=tk.BOTH, expand=True)
        self.root.title('Single player' if isSinglePlayer else 'Multiplayer')

        # config grid layout 
        # left - move history 
        # center - game board 
        # right turn, health, progress, etc 
        self.gameBoardFrame.columnconfigure(0, weight=1)
        self.gameBoardFrame.columnconfigure(1, weight=3)
        self.gameBoardFrame.columnconfigure(2, weight=1)

        # move history 
        moveHistoryFrame = tk.Frame(self.gameBoardFrame, highlightbackground="black",highlightthickness=1)
        moveHistoryFrame.grid(
            row=0,
            column=0, 
            sticky='ns',
            padx=5, 
            pady=5
        )
        moveHistoryLabel = ttk.Label(
            moveHistoryFrame, 
            text='Move History'
        )
        moveHistoryLabel.grid(row=0, column=0, pady=5)
        self.moveHistoryTxt = tk.Text(moveHistoryFrame, width=60, height=10, state='disabled')
        self.moveHistoryTxt.grid(row=1, column=0, padx=5, pady=5)

        # Game board 
        canvasFrame = tk.Frame(self.gameBoardFrame, highlightbackground="blue",highlightthickness=3)
        canvasFrame.grid(
            row=0, 
            column=1, 
            sticky='news',
            padx=5, 
            pady=5
        )
        
        # adding a new canvas to frame cuz previous one was causing issues 
        self.canvas = tk.Canvas(canvasFrame, width=800, height=600, highlightthickness=1, highlightbackground="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Pass the new canvas to the controller
        self.playGameController.canvas = self.canvas

        # right controls 
        controlsFrame = tk.Frame(self.gameBoardFrame, highlightbackground="black",highlightthickness=1)
        controlsFrame.grid(
            row=0, 
            column=2, 
            sticky='ns',
            padx=5, 
            pady=5
        )
        controlsFrame.columnconfigure(0, weight=1)

        # turn counter - top right 
        self.turnLabel = ttk.Label(
            controlsFrame, 
            text=f'Turn: {self.playGameController.currentTurn}'
        )
        self.turnLabel.grid(row=0, column=2, pady=5)

        # health counter - middle right
        self.healthLabel = ttk.Label(
            controlsFrame, 
            text=f'Health: {self.playGameController.playerHealth}'
        )
        self.healthLabel.grid(row=1, column=0, pady=5)

        # progress bar - middle right 
        progressLabel = ttk.Label(
            controlsFrame, 
            text='Checkpoint Progress',
        )
        progressLabel.grid(row=2, column=0, pady=5)

        self.progressBar = ttk.Progressbar(
            controlsFrame, 
            orient='horizontal', 
            length=200, 
            mode='determinate'
        )
        self.progressBar.grid(row=3, column=0, pady=5) 
        self.progressBar['maximum'] = 3 # currently default for 3 checkpoints 
        self.progressBar['value'] = 0 

        # registers and cards - bottom right 
        registerLabel = ttk.Label(
            controlsFrame, 
            text='Registers and Cards', 
        )
        registerLabel.grid(row=4, column=0, pady=5)

        cardsFrame = tk.Frame(controlsFrame, highlightbackground="black",highlightthickness=1)
        cardsFrame.grid(row=5, column=0, pady=5)
        self.playGameController.makeRegistersAndCards() 

        # make the game grid + stuff 
        self.playGameController.makeGrid()
        self.playGameController.createRobot() # initialse robot on grid 
        self.playGameController.placeObstacles([(3,3), (4,5), (6,7)]) # gonan randomise placemnet, but this is just for a test 
        self.playGameController.placeCheckpoints([(1,1), (5,6), (3,8)])


        # submit button 
        submitBtn = ttk.Button(
            canvasFrame, 
            text='submit', 
            command=self.playGameController.submitCards
        )
        submitBtn.pack(pady=10)
    
        # Reset button 
        resetBtn = ttk.Button(
            canvasFrame, 
            text='Reset Cards', 
            command=self.playGameController.resetCards
        )
        resetBtn.pack(pady=10)

    def updateTurnLabel(self, turn):
        self.turnLabel.config(text=f'Turn: {turn}')
    
    def updateHealthLabel(self, health):
        self.healthLabel.config(text=f'Health: {health}')
    
    def updateProgressBar(self, checkpointsReached):
        self.progressBar['value'] = checkpointsReached

    def updateMoveHistory(self, history):
        self.moveHistoryTxt.configure(state='normal')
        self.moveHistoryTxt.delete(1.0, tk.END)

        # populate the text box 
        for move in history: 
            turn = move['turn']
            direction = move['direction']
            steps = move['steps']
            start = move['start']
            end = move['end']
            collision = move.get('collision', False)

            if collision: 
                self.moveHistoryTxt.insert(tk.END, 
                                       f'Obstacle hittt at {end}!! \n')

            else: 
                self.moveHistoryTxt.insert(tk.END, 
                                       f'{turn}: {steps} steps {direction} from {start} to {end} \n')
        
        self.moveHistoryTxt.configure(state='disabled')
