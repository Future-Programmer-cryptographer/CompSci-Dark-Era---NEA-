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

        easyBoardImage = Image.open('Images/easy.png').resize((300,300))
        easyBoard = ImageTk.PhotoImage(easyBoardImage)

        # button widget 
        easyBtn = ttk.Button(self.selectBoardFrame, 
                            text='EASY',
                            image = easyBoard,
                            command=self.playGameController.onBoardSelect)
        easyBtn.pack(pady=5) 

        mediumBtn = ttk.Button(self.selectBoardFrame, 
                            text = 'MEDIUM',
                            command=self.playGameController.onBoardSelect)
        mediumBtn.pack(pady=5) 

        hardBtn = ttk.Button(self.selectBoardFrame, 
                            text = 'HARD',
                            command=self.playGameController.onBoardSelect)
        hardBtn.pack(pady=5)
    
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
        self.gameBoardFrame.columnconfigure(0, weight=1)
        self.gameBoardFrame.columnconfigure(1, weight=2)
        self.gameBoardFrame.columnconfigure(2, weight=2)

        # helpful informations frame 
        infoFrame = tk.Frame(self.gameBoardFrame, highlightbackground="black",highlightthickness=5)
        infoFrame.grid(row=1, columnspan=3, sticky='news')

        infoLabel = ttk.Label(infoFrame, text='Helpful information: ')
        infoLabel.grid(row=0, column=0, pady=5)

        directionsImg = Image.open('Images/checkpoint.png').resize((100,100))
        print('image created?')
        img = ImageTk.PhotoImage(directionsImg)
        stuff = ttk.Label(infoFrame, image=img)
        stuff.grid(row=0, column=1, pady=5)

        # move history 
        moveHistoryFrame = tk.Frame(self.gameBoardFrame, highlightbackground="black",highlightthickness=1)
        moveHistoryFrame.grid(
            row=0,
            column=0, 
            sticky='news',
            padx=5, 
            pady=5
        )
        moveHistoryLabel = ttk.Label(moveHistoryFrame, text='Move History')
        moveHistoryLabel.grid(row=0, column=0, pady=5)
        self.moveHistoryTxt = tk.Text(moveHistoryFrame, width=40, height=15, state='disabled')
        self.moveHistoryTxt.grid(row=1, column=0, padx=5, pady=5)

        self.botMoveHistoryTxt = tk.Text(moveHistoryFrame, width=40, height=15, state='disabled')
        self.botMoveHistoryTxt.grid(row=2, column=0, padx=5, pady=5)


        # Game board canvas and frame
        canvasFrame = tk.Frame(self.gameBoardFrame, highlightbackground="blue", highlightthickness=3)
        canvasFrame.grid(
            row=0, column=1, sticky="nsew", padx=5, pady=5
        )
        self.canvas = tk.Canvas(canvasFrame, width=500, height=600, highlightthickness=1, highlightbackground="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.playGameController.canvas = self.canvas

        # right controls 
        controlsFrame = tk.Frame(self.gameBoardFrame, highlightbackground="black",highlightthickness=1)
        controlsFrame.grid(
            row=0, 
            column=2, 
            sticky='news',
            padx=5, 
            pady=5
        )
        controlsFrame.columnconfigure(0, weight=2)

        # Register and Cards Frame
        cardsAndRegistersFrame = tk.Frame(controlsFrame, highlightbackground="black", highlightthickness=2)
        cardsAndRegistersFrame.grid(
            row=5, column=0, sticky="nsew", padx=5, pady=5
        )
        cardsAndRegistersFrame.columnconfigure(0, weight=1)

        # Create a canvas inside the registers and cards frame
        self.cardsCanvas = tk.Canvas(cardsAndRegistersFrame, width=400, height=300, bg="white", highlightthickness=1)
        self.cardsCanvas.pack(fill=tk.BOTH, expand=False)

        # Call makeRegistersAndCards
        self.playGameController.makeRegistersAndCards(self.cardsCanvas)
        # turn counter - top right 
        self.turnLabel = ttk.Label(controlsFrame, text=f'Turn: {self.playGameController.currentTurn}')
        self.turnLabel.grid(row=0, column=0, pady=5)

        # health counter - middle right
        self.healthLabel = ttk.Label(controlsFrame, text=f'Player Health: {self.playGameController._playerHealth}')
        self.healthLabel.grid(row=1, column=0, pady=5)

        self.botHealthLabel = ttk.Label(controlsFrame, text=f'Bot Health: {self.playGameController._botHealth}')
        self.botHealthLabel.grid(row=2, column=0, pady=5)

        # progress bar - middle right 
        progressLabel = ttk.Label(controlsFrame, text='Checkpoint Progress',)
        progressLabel.grid(row=3, column=0, pady=5)

        self.progressBar = ttk.Progressbar(controlsFrame, orient='horizontal', length=150, mode='determinate')
        self.progressBar.grid(row=4, column=0, padx=5, pady=5) 
        self.progressBar['maximum'] = self.playGameController._checkpointCount 
        self.progressBar['value'] = 0 

        # make the game grid + stuff 
        self.playGameController.makeGrid()

        # submit button 
        submitBtn = ttk.Button(controlsFrame, text='submit', command=self.playGameController.submitCards)
        submitBtn.grid(row=6, column=0, pady=5)
    
        # Reset button 
        resetBtn = ttk.Button(controlsFrame, text='Reset Cards', command=self.playGameController.resetCards)
        resetBtn.grid(row=7, column=0, pady=5)

        # Undo button 
        undoBtn = ttk.Button(controlsFrame, text='Undo', command=self.playGameController.undoLastAction)
        undoBtn.grid(row=8, column=0, pady=5)

        # Save button 
        saveBtn = ttk.Button(controlsFrame, text='Save', command=self.playGameController._saveGameState)
        saveBtn.grid(row=9, column=0, pady=5)

    def updateTurnLabel(self, turn):
        self.turnLabel.config(text=f'Turn: {turn}')
    
    def updateHealthLabel(self, health, isBot=False):
        if isBot:
            self.botHealthLabel.config(
                text=f"Bot Health: {health}")
        else:
            self.healthLabel.config(
                text=f"Player Health: {health}")

    
    def updateProgressBar(self, checkpointsReached):
        self.progressBar['value'] = checkpointsReached

    def updateMoveHistory(self, history, isBot=False):
        textBox = self.botMoveHistoryTxt if isBot else self.moveHistoryTxt
        textBox.configure(state='normal')
        textBox.delete(1.0, tk.END)

        # populate the text box 
        for move in history: 
            turn = move['turn']
            direction = move['direction']
            steps = move['steps']
            start = move['start']
            end = move['end']
            collision = move.get('collision', False)

            if collision: 
                textBox.insert(tk.END, 
                                       f'Obstacle hittt at {end}!! \n')

            else: 
                textBox.insert(tk.END, 
                                       f'{turn}: {steps} steps {direction} from {start} to {end} \n')
        
        textBox.configure(state='disabled')
