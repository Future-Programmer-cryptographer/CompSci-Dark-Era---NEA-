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

        # Creating a select board frame when the user wants to select a board 
        self.selectBoardFrame = tk.Frame(self.root)

        titleLabel = ttk.Label(self.selectBoardFrame, text='Select one of the three boards for single player vs Bot OR 4-Player Multiplayer \n Boards are sorted by difficulty, easy-medium-hard (left to right) \n You can also create a custom board for multiplayer gameplay \n (You can customise no. of players, grid size, no. of obstacles and checkpoints)', font=('Verdana',15))
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

        # Creating difficulty option buttons 
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

        msg = ttk.Label(self.optionWindowFrame, text='Select one of the game options below\n A short summary of each game mode can be found below the buttons', font=('Verdana',20), justify='center')
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

        # rules frame implementation to one in Rules class (View rules from Main Menu) - provides a short useful summary of the game modes for user 
        self.rulesFrame = tk.Frame(self.optionWindowFrame)
        self.rulesFrame.pack(fill=tk.BOTH)

        rulesFrame = ttk.Frame(self.rulesFrame)
        rulesFrame.pack(pady=10)

        section1 = ttk.Label(rulesFrame, text='Single Player vs Bot', font=('fixedsys 20 bold'))
        text1 = ttk.Label(rulesFrame, text='You will play against a *very intelligent* bot. Try and get to all the checkpoints before the bot does!', font=('Verdana',15), wraplength=450)

        section2 = ttk.Label(rulesFrame, text='4-player Multiplayer', font=('fixedsys 20 bold'))
        text2 = ttk.Label(rulesFrame, text='Work as a team of 4 to get to all the checkpoints as quickly as you can!', font=('Verdana',15), wraplength=450)
        
        section1.grid(row=0, column=0, padx=20, pady=10)
        text1.grid(row=1, column=0, padx=20, pady=10)
        
        section2.grid(row=0, column=1, padx=20, pady=10)
        text2.grid(row=1, column=1, padx=20, pady=10)

    # if the user selects a custom board, then call the _makeCustomBoard method in the playGameController, else in all cases, hide the frame 
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
                            text=" AIM: drag and drop UP TO 1, 2 OR 3 OUT OF 5 CARD into the EMPTY CARD SLOTS to move your robot and get to all the checkpoints before the BOT \n The robot you will be controlling is the blue token on the board with the label 'P' and you will be playing AGAINST a bot (label 'B'). \n RESET Cards: if you have accidently dragged a card into a wrong slot, then click 'Reset Cards' to start again. \n GREEN TRIANGLES are CHECKPOINT. You MUST LAND on the checkpoint at the end of your turn to get the checkpoint \n DARK GREY SQUARES are OBSTACLES- collision with an obstacle will result in a loss of health, AVOID them if you can. \n HEALTH: you will start with 5 health points. You will lose a health for every obstacle collision AND if you go off the grid at any point during the game. You will regain 1 health for every checkpoint you reach. \n MOVE HISTORY: you can view your past moves (and the bot if playing against bot) in the move history text box on the left hand side of this screen.\n GOOD LUCK AND HAVE FUN!", font=('Verdana', 11), wraplength=1000)
        self.summary.grid(row=0, column=1, pady=5)

        self.multiplayerSummary = ttk.Label(infoFrame, 
                                            text=" AIM: Work as a team to get to all the checkpoints in the shortest time possible! \n Assign each player in your multiplayer team a number anddrag and drop UP TO 1, 2 OR 3 OUT OF 5 CARD into the EMPTY CARD SLOTS to move your numbered robot. \n RESET Cards: if you have accidently dragged a card into a wrong slot, then click 'Reset Cards' to start again. \n GREEN TRIANGLES are CHECKPOINTS. You MUST LAND on the checkpoint at the end of your turn to get the checkpoint. \n DARK GREY SQUARES are OBSTACLES- collision with an obstacle will result in a loss of health, AVOID them if you can. \n HEALTH: you will start with 10 health points. You will lose a health for every obstacle collision AND if you go off the grid at any point during the game. You will regain 1 health for every checkpoint you reach. \n GOOD LUCK AND HAVE FUN!", font=('Verdana', 11), wraplength=1000)

        # Creating a move history with labels and text boxes to be populated later for single player vs bot game mode 
        self.moveHistoryFrame = tk.Frame(self.gameBoardFrame, highlightbackground="black",highlightthickness=1)
        self.moveHistoryFrame.grid(
            row=0,
            column=0, 
            sticky='news',
            padx=5, 
            pady=5
        )
        moveHistoryLabel = ttk.Label(self.moveHistoryFrame, text='Player Move History', font=('fixedsys 20 bold'), foreground='blue2')
        moveHistoryLabel.grid(row=0, column=0, pady=5)
        self.moveHistoryTxt = tk.Text(self.moveHistoryFrame, width=40, height=15, state='disabled')
        self.moveHistoryTxt.grid(row=1, column=0, padx=5, pady=5)

        moveHistoryLabel2 = ttk.Label(self.moveHistoryFrame, text='Bot Move History', font=('fixedsys 20 bold'), foreground='red3')
        moveHistoryLabel2.grid(row=2, column=0, pady=2)
        self.botMoveHistoryTxt = tk.Text(self.moveHistoryFrame, width=40, height=15, state='disabled')
        self.botMoveHistoryTxt.grid(row=3, column=0, padx=5, pady=5)

        # Game board canvas frame - this is where the grid will be created 
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
        
        # Register and Cards Frame - the registers and cards canvas will be created in here 
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

        # Frid to grid labels/turn counters/etc (things above the card and register slot canvas)
        stateFrame = tk.Frame(controlsFrame)
        stateFrame.grid(row=1, column=0)

        # turn labels for player and bot - top right hand side 
        self.turnLabel = ttk.Label(stateFrame, text=f'Turn: {self.playGameController.currentTurn}', font=('fixedsys 20 bold'))
        if isSinglePlayer: 
            self.turnLabel.grid(row=0, column=1, pady=5)
        else: 
            self.turnLabel.grid(row=0, column=0, pady=5)

        # health labels for player and bot - these will be updated by methods later 
        self.healthLabel = ttk.Label(stateFrame, text=f'Player Health: {self.playGameController._playerHealth}', font=('fixedsys', 15), foreground='blue2')
        self.healthLabel.grid(row=1, column=0, pady=5)

        self.botHealthLabel = ttk.Label(stateFrame, text=f'Bot Health: {self.playGameController._botHealth}', font=('fixedsys', 15), foreground='red2')
        self.botHealthLabel.grid(row=1, column=2, pady=5)

        # progress label and bar - the max value of progress bar is the total checkpoint count. 
        progressLabel = ttk.Label(stateFrame, text='Player Checkpoint Progress',font=('fixedsys'), foreground='blue2')
        progressLabel.grid(row=3, column=0, pady=5)

        self.progressBar = ttk.Progressbar(stateFrame, orient='horizontal', length=150, mode='determinate')
        self.progressBar.grid(row=4, column=0, padx=5, pady=5) 
        self.progressBar['maximum'] = self.playGameController._checkpointCount 
        self.progressBar['value'] = 0 

        # separate progress label and bar for bot 
        self.botProgressLabel = ttk.Label(stateFrame, text='Bot Checkpoint Progress', font=('fixedsys'), foreground='red2')
        self.botProgressLabel.grid(row=3, column=2, pady=5)

        self.botProgressBar = ttk.Progressbar(stateFrame, orient='horizontal', length=150, mode='determinate')
        self.botProgressBar.grid(row=4, column=2, pady=5)
        self.botProgressBar['maximum'] = self.playGameController._checkpointCount 
        self.botProgressBar['value'] = 0 

        # stopwatch frame for multiplayer game mode  
        self.stopWatchFrame = tk.Frame(stateFrame)

        time = ttk.Label(self.stopWatchFrame, text='Time elapsed:', font=('fixedsys 20 bold'))
        time.grid(row=1, column=1)
        timeLabel = ttk.Label(self.stopWatchFrame, textvariable=self.timestr, font=('fixedsys 20 '), background='black', foreground='white')
        self.setTime(self.elapsedTime) 
        timeLabel.grid(row=2, column=1, rowspan=3, columnspan=3)
        
        # make the game grid
        self.playGameController.makeGrid()

        # frame to grid subtmit, reset, undo, save, quit buttons 
        buttonsFrame = tk.Frame(controlsFrame)
        buttonsFrame.grid(row=7, column=0)

        btnStyle = ttk.Style()

        # submit button 
        submitBtn = ttk.Button(buttonsFrame, text='SUBMIT', style='btn.TButton', command=self.playGameController.submitCards)
        submitBtn.grid(row=1, column=0, pady=5)
    
        # Reset button 
        resetBtn = ttk.Button(buttonsFrame, text='RESET Cards', style='btn.TButton', command=self.playGameController.resetCards)
        resetBtn.grid(row=1, column=2, pady=5)

        # Undo button 
        undoBtn = ttk.Button(buttonsFrame, text='UNDO', style='btn.TButton', command=self.playGameController.undoLastAction)
        undoBtn.grid(row=2, column=0, pady=5)

        # Save button 
        saveBtn = ttk.Button(buttonsFrame, text='SAVE', style='btn.TButton', command=self.playGameController._saveGameState)
        saveBtn.grid(row=2, column=2, pady=5)

        # Quit to main menu button 
        quitBtn = ttk.Button(buttonsFrame, text='QUIT to Main Menu', style='btn.TButton', command=self.playGameController.backToMain)
        quitBtn.grid(row=3, column=0, pady=5)

        btnStyle.configure('btn.TButton', font='fixedsys 20 bold')

        # hiding unnecessary features in multiplayer 
        if not isSinglePlayer: 
            self.moveHistoryFrame.grid_forget() 
            self.botProgressLabel.grid_forget() 
            self.botProgressBar.grid_forget() 
            self.botHealthLabel.grid_forget() 
            self.summary.grid_forget() 
            self.multiplayerSummary.grid(row=0, column=1, pady=5) 
            self.stopWatchFrame.grid(row=1, column=1, columnspan=3, rowspan=3)
    
    # method to update time on the canvas 
    def updateTime(self):
        self.elapsedTime = time.time() - self.start
        self.setTime(self.elapsedTime)
        self.timer = self.canvas.after(50, self.updateTime)
    
    # setting the time 
    def setTime(self, elapsed):
        mins = int(elapsed / 60)
        hrs = int(mins / 60)
        secs = int(elapsed - mins * 60.0)
        self.timestr.set('%02d:%02d:%02d' % (hrs, mins, secs))
    
    # starting the time - this method is called by the playGameController as soon as the user closes the info messagebox in multiplayer game mode
    def startTime(self):
        if not self.running: 
            self.start = time.time() - self.elapsedTime
            self.updateTime() 
            self.running = 1 
    
    # stop the time when the user clicks on save gmae 
    def stopTime(self):
        if self.running: 
            self.canvas.after_cancel(self.timer)
            self.elapsedTime = time.time() - self.start
            self.setTime(self.elapsedTime)
            self.running = 0 

            self.start = time.time() 
            self.elapsedTime = 0.0 
            self.setTime(self.elapsedTime)

    # method to update turn between player/s and bot  
    def updateTurnLabel(self, turn):
        self.turnLabel.config(text=f'Turn: {turn}')
    
    # method to update health label for player/bot 
    def updateHealthLabel(self, health, isBot=False):
        if isBot:
            self.botHealthLabel.config(
                text=f"Bot Health: {health}")
        else:
            self.healthLabel.config(
                text=f"Player Health: {health}")

    # updating player progress bar 
    def updateProgressBar(self, checkpointsReached):
        self.progressBar['value'] = checkpointsReached

    # updating bot progrses bar 
    def updateBotProgress(self, botCheckpointsReached):
        self.botProgressBar['value'] = botCheckpointsReached 

    # updating player/bot move history for single player vs bot game mode 
    def updateMoveHistory(self, history, isBot=False):
        textBox = self.botMoveHistoryTxt if isBot else self.moveHistoryTxt
        textBox.configure(state='normal')
        textBox.delete(1.0, tk.END)

        # populating the move history textbox with either a collision, undo move, or in most cases, the move played by the user 
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
