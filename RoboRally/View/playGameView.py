from tkinter import * 
from PIL import Image, ImageTk 
import tkinter as tk 
from tkinter import ttk 
import time 
from tkinter import messagebox
import emoji

# need a board selection screen with different difficulty 
# need to have three different boards - tkinter framing... 
# after they have selected the boards, we want them to select single player vs bot or multiplayer 

class PlayGameView: 

    def __init__(self, root, canvas, playGameController):
        self.root = root 
        self.canvas = canvas 
        self.playGameController = playGameController 

        # creating another frame 
        self.selectBoardFrame = tk.Frame(self.root)

        titleLabel = ttk.Label(self.selectBoardFrame, text='Select one of the three boards for single player vs Bot OR Multiplayer \n Boards are sorted by difficulty, easy-medium-hard (left to right) \n You can also create a custom board for multiplayer gameplay \n (You can customise no. of players, grid size, no. of obstacles and checkpoints)', font=('Verdana',15))
        titleLabel.pack(pady=10)

        # note to my future self, the token was included here becuase there were some bugs when closing the frame, so adding a token solved that bug 
        backBtn = ttk.Button(self.selectBoardFrame, 
                        text='Back to Main Menu',
                        style='play.TButton',
                        command=lambda: self.playGameController.backToMain (1))
        backBtn.pack(side=BOTTOM, ipadx=25, ipady=25, expand=True)

        
        customBtn = ttk.Button(self.selectBoardFrame, 
                               text='Create Custom Board',
                               style='play.TButton',
                               command = self.onCustomBoard)
        customBtn.pack(side=BOTTOM, ipadx=25, ipady=25, expand=True)


        # need to use self.easyBoard instead of easyBoard due to 'garbage collection' 
        easyBoardImage = Image.open('Images/easy.png').resize((400,400))
        self.easyBoard = ImageTk.PhotoImage(easyBoardImage)

        mediumBoardImage = Image.open('Images/medium.png').resize((400,400))
        self.mediumBoard = ImageTk.PhotoImage(mediumBoardImage)

        hardBoardImage = Image.open('Images/hard.png').resize((400,400))
        self.hardBoard = ImageTk.PhotoImage(hardBoardImage)

        # button widget 
        easyBtn = ttk.Button(self.selectBoardFrame, 
                            text='EASY',
                            image = self.easyBoard,
                            command= lambda: self.playGameController.onBoardSelect('EASY'))
        easyBtn.pack(side=LEFT, expand=True) 

        mediumBtn = ttk.Button(self.selectBoardFrame, 
                            text = 'MEDIUM',
                            image = self.mediumBoard, 
                            command= lambda: self.playGameController.onBoardSelect('MEDIUM'))
        mediumBtn.pack(side=LEFT, expand=True) 

        hardBtn = ttk.Button(self.selectBoardFrame, 
                            text = 'HARD',
                            image = self.hardBoard,
                            command= lambda: self.playGameController.onBoardSelect('HARD'))
        hardBtn.pack(side=LEFT,expand=True)

        self.start = 0.0 
        self.elapsedTime = 0.0
        self.running = 0 
        self.timestr = StringVar()

    
    def showSelectBoardWindow(self):
        self.root.title('Choose Game Option')
        self.selectBoardFrame.pack(fill=tk.BOTH)
    
    def showOptionWindow(self): 

        self.selectBoardFrame.pack_forget() 

        style = ttk.Style() 

        # creating an options window frame
        self.optionWindowFrame = tk.Frame(self.root)
        self.optionWindowFrame.pack(fill=tk.BOTH)

        msg = ttk.Label(self.optionWindowFrame, text='Select one of the game options below\nA short summary of each game mode can be found below the buttons', font=('Verdana',20), justify='center')
        msg.pack(ipady=10, ipadx=10, pady=10)


        singlePlayerBtn = ttk.Button(self.optionWindowFrame, 
                                     text='Single Player vs Bot', 
                                     style='play.TButton',
                                     command=self.onOptionWindowSelectSinglePlayer)
        singlePlayerBtn.pack(ipady=10, ipadx=10, pady=10)

        multiplayerBtn = ttk.Button(self.optionWindowFrame, 
                                     text='Multiplayer', 
                                     style='play.TButton',
                                     command=self.onOptionWindowSelectMultiplayer)
        multiplayerBtn.pack(ipady=10, ipadx=10, pady=10)
        
        style.configure('play.TButton', font=('fixedsys 20 bold'), foreground='red3')

        self.rulesFrame = tk.Frame(self.optionWindowFrame)
        self.rulesFrame.pack(fill=tk.BOTH)

        rulesFrame = ttk.Frame(self.rulesFrame)
        rulesFrame.pack(pady=10)

        section1 = ttk.Label(rulesFrame, text='Single Player vs Bot', font=('fixedsys 20 bold'))
        text1 = ttk.Label(rulesFrame, text='You will play against a *very intelligent* bot. Try and get to all the checkpoints before the bot does!', font=('Verdana',15), wraplength=450)

        section2 = ttk.Label(rulesFrame, text='Multiplayer', font=('fixedsys 20 bold'))
        text2 = ttk.Label(rulesFrame, text='Work as a team of 4 to get to all the checkpoints as quickly as you can!', font=('Verdana',15), wraplength=450)
        
        section1.grid(row=0, column=0, padx=20, pady=10)
        text1.grid(row=1, column=0, padx=20, pady=10)
        
        section2.grid(row=0, column=1, padx=20, pady=10)
        text2.grid(row=1, column=1, padx=20, pady=10)

    
    def onCustomBoard(self):
        self.selectBoardFrame.pack_forget() 
        self.playGameController._makeCustomBoard() 
    
    def onOptionWindowSelectSinglePlayer(self):
        self.optionWindowFrame.pack_forget() 
        self.playGameController.onSinglePlayerSelect() 
    
    def onOptionWindowSelectMultiplayer(self):
        self.optionWindowFrame.pack_forget() 
        self.playGameController.onMultiplayerSelect()  
    
    def showGameBoard(self, isSinglePlayer=True):

        # creating game board frame with GRID layout 
        self.gameBoardFrame = tk.Frame(self.root, highlightbackground="black",highlightthickness=1)
        self.gameBoardFrame.pack(fill=tk.BOTH, expand=True)
        self.root.title('Single player' if isSinglePlayer else 'Multiplayer')

        
        # config grid layout 
        self.gameBoardFrame.columnconfigure(0, weight=1)
        self.gameBoardFrame.columnconfigure(1, weight=2)
        self.gameBoardFrame.columnconfigure(2, weight=2)

        # helpful info frame 
        infoFrame = tk.Frame(self.gameBoardFrame, highlightbackground="black",highlightthickness=2)
        infoFrame.grid(row=1, columnspan=3, sticky='news')

        infoLabel = ttk.Label(infoFrame, text='Helpful information:', font=('fixedsys 20 bold'))
        infoLabel.grid(row=0, column=0, pady=5, padx=5)

        self.summary = ttk.Label(infoFrame, 
                            text="AIM: drag and drop UP TO 3 OUT OF 5 CARDS into the EMPTY WHITE CARD SLOTS to move your robot and get to all the checkpoints before other ROBOT \n The robot you will be controlling is the blue token on the board with the label 'P' and you will be playign AGAINST a bot (label 'B'). \n GREEN TRIANGLES are CHECKPOINT. You MUST LAND on the checkpoint at the end of your turn to get the checkpoint \n DARK GREY SQUARES are OBSTACLES- collision with an obstacle will result in a loss of health, AVOID them if you can. \n Up = 1 square up \n Down = 1 square down  \n Left = one square to the left \n Right = one square to the right \n MOVE HISTORY: you can view your past moves (and the bot if playing against bot) in the move history text box on the left hand side of this screen.\n GOOD LUCK AND HAVE FUN!", font=('Arial', 12))
        self.summary.grid(row=0, column=1, pady=5)

        self.multiplayerSummary = ttk.Label(infoFrame, 
                                            text='AIM: Work as a team to get to all the checkpoints in the shortest time possible! \n Assign each player in your multiplayer team a number and drag and drop UP TO 3 OUT OF 5 CARDS in the EMPTY WHITE CARD SLOTS to move your numbered robot (numbered 1-4). \n GREEN TRIANGLES are CHECKPOINTS. You MUST LAND on the checkpoint at the end of your turn to get the checkpoint. \n DARK GREY SQUARES are OBSTACLES- collision with an obstacle will result in a loss of health, AVOID them if you can. \n Up = 1 square up \n Down = 1 square down  \n Left = one square to the left \n Right = one square to the right. \n GOOD LUCK AND HAVE FUN!', font=('Arial', 12))


        # move history 
        self.moveHistoryFrame = tk.Frame(self.gameBoardFrame, highlightbackground="black",highlightthickness=1)
        self.moveHistoryFrame.grid(
            row=0,
            column=0, 
            sticky='news',
            padx=5, 
            pady=5
        )
        moveHistoryLabel = ttk.Label(self.moveHistoryFrame, text='Player Move History', font=('fixedsys 20 bold'))
        moveHistoryLabel.grid(row=0, column=0, pady=5)
        self.moveHistoryTxt = tk.Text(self.moveHistoryFrame, width=40, height=15, state='disabled')
        self.moveHistoryTxt.grid(row=1, column=0, padx=5, pady=5)

        moveHistoryLabel2 = ttk.Label(self.moveHistoryFrame, text='Bot Move History', font=('fixedsys 20 bold'))
        moveHistoryLabel2.grid(row=2, column=0, pady=2)
        self.botMoveHistoryTxt = tk.Text(self.moveHistoryFrame, width=40, height=15, state='disabled')
        self.botMoveHistoryTxt.grid(row=3, column=0, padx=5, pady=5)

        # Game board canvas and frame
        canvasFrame = tk.Frame(self.gameBoardFrame, highlightbackground="black", highlightthickness=3)
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

        # frame to grid labels/turn coutners/etc. 
        stateFrame = tk.Frame(controlsFrame)
        stateFrame.grid(row=1, column=0)

        # turn counter - top right 
        self.turnLabel = ttk.Label(stateFrame, text=f'Turn: {self.playGameController.currentTurn}')
        if isSinglePlayer: 
            self.turnLabel.grid(row=0, column=1, pady=5)
        else: 
            self.turnLabel.grid(row=0, column=0, pady=5)

        # health counter - middle right
        self.healthLabel = ttk.Label(stateFrame, text=f'Player Health: {self.playGameController._playerHealth}')
        self.healthLabel.grid(row=1, column=0, pady=5)

        self.botHealthLabel = ttk.Label(stateFrame, text=f'Bot Health: {self.playGameController._botHealth}')
        self.botHealthLabel.grid(row=1, column=2, pady=5)

        # progress bar - middle right 
        progressLabel = ttk.Label(stateFrame, text='Player Checkpoint Progress')
        progressLabel.grid(row=3, column=0, pady=5)

        self.progressBar = ttk.Progressbar(stateFrame, orient='horizontal', length=150, mode='determinate')
        self.progressBar.grid(row=4, column=0, padx=5, pady=5) 
        self.progressBar['maximum'] = self.playGameController._checkpointCount 
        self.progressBar['value'] = 0 

        # Creating a bot progress bar 
        self.botProgressLabel = ttk.Label(stateFrame, text='Bot Checkpoint Progress')
        self.botProgressLabel.grid(row=3, column=2, pady=5)

        self.botProgressBar = ttk.Progressbar(stateFrame, orient='horizontal', length=150, mode='determinate')
        self.botProgressBar.grid(row=4, column=2, pady=5)
        self.botProgressBar['maximum'] = self.playGameController._checkpointCount 
        self.botProgressBar['value'] = 0 

        # stopwatch for multiplayer! 
        self.stopWatchFrame = tk.Frame(stateFrame)

        time = ttk.Label(self.stopWatchFrame, text='Time elapsed:', font=('fixedsys 20 bold'))
        time.grid(row=0, column=0)
        timeLabel = ttk.Label(self.stopWatchFrame, textvariable=self.timestr, font=('fixedsys 20 '), background='black', foreground='white')
        self.setTime(self.elapsedTime) 
        timeLabel.grid(row=1, column=0, rowspan=3, columnspan=3)
        
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

        # Quit to main menu button 
        quitBtn = ttk.Button(controlsFrame, text='Quit to Main Menu', command=self.playGameController.backToMain)
        quitBtn.grid(row=10, column=0, pady=5)

        # hiding unnecessary features in multiplayer 
        if not isSinglePlayer: 
            self.moveHistoryFrame.grid_forget() 
            self.botProgressLabel.grid_forget() 
            self.botProgressBar.grid_forget() 
            self.botHealthLabel.grid_forget() 
            self.summary.grid_forget() 
            # undoBtn.grid_forget() 
            self.multiplayerSummary.grid(row=0, column=1, pady=5) 
            self.stopWatchFrame.grid(row=0, column=1, columnspan=3, rowspan=3)
        
    def updateTime(self):
        self.elapsedTime = time.time() - self.start
        self.setTime(self.elapsedTime)
        self.timer = self.canvas.after(50, self.updateTime)
    
    def setTime(self, elapsed):
        mins = int(elapsed / 60)
        hrs = int(mins / 60)
        secs = int(elapsed - mins * 60.0)
        self.timestr.set('%02d:%02d:%02d' % (hrs, mins, secs))
    
    def startTime(self):
        if not self.running: 
            self.start = time.time() - self.elapsedTime
            self.updateTime() 
            self.running = 1 
        
    def stopTime(self):
        if self.running: 
            self.canvas.after_cancel(self.timer)
            self.elapsedTime = time.time() - self.start
            self.setTime(self.elapsedTime)
            self.running = 0 

            self.start = time.time() 
            self.elapsedTime = 0.0 
            self.setTime(self.elapsedTime)

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
    
    def updateBotProgress(self, botCheckpointsReached):
        self.botProgressBar['value'] = botCheckpointsReached 

    def updateMoveHistory(self, history, isBot=False):
        textBox = self.botMoveHistoryTxt if isBot else self.moveHistoryTxt
        textBox.configure(state='normal')
        textBox.delete(1.0, tk.END)

        # fill textbox with useful info
        for move in history: 
            undo = move.get('undo', False)
            turn = move['turn']
            direction = move['direction']
            steps = move['steps']
            start = move['start']
            end = move['end']
            collision = move.get('collision', False)

            if collision: 
                textBox.insert(tk.END, 
                                       f'{emoji.emojize(":collision:")}Lost health!!\n')
            if undo:
                textBox.insert(tk.END, 
                                       f'{emoji.emojize(":right_arrow_curving_left:")}Move undone\n')
            else: 
                textBox.insert(tk.END, 
                                       f'{turn}: {steps} steps {direction} from {start} to {end} \n')
        
        textBox.configure(state='disabled')
