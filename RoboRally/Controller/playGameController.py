import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox
import random 
from datetime import datetime
from tkinter import simpledialog
from tkinter.simpledialog import askstring

# importing the views and controllers from other files 
from View.playGameView import PlayGameView
from Controller.mainMenuController import MainMenuController
from View.mainMenuView import MainMenuView
from cardsAndRegisters import model
from cardsAndRegisters import view
from cardsAndRegisters.controller import DragAndDropController

from Controller.helperFunctions import generateRandomSquares, convertToRankAndFile, getMdPos, getMdValue
from Controller.botLogic import generateBotMoves, generateRandomBotMoves

class PlayGameController:
    def __init__(self, root, canvas):

        # Public attributes 
        self.root = root
        self.canvas = canvas
        self.playGameView = PlayGameView(root, self.canvas, self)
        self.mainMenuController = MainMenuController(MainMenuView)
        self.currentTurn = 1
        self.isMultiplayer = False
        self.totalPlayers = 4
        self.checkpointsReached = 0 
        self.botCheckpointsReached = 0 
        self.currentPlayerIdx = 0 

        # This is updated by the '__updateDifficulty' method when the users selects a board 
        self.difficulty = '' 

        self.cards = []
        self.registers = [] 

        self.moveHistory = []
        self.botMoveHistory = []

        self.playerPos = None
        self.botPos = None
        self.playerId = None
        self.playerLabel = None
        self.botId = None
        self.botLabel = None

        # protected attributes 
        self._playerHealth = 5
        self._botHealth = 5
        self._obstacleCount = 5
        self._checkpointCount = 10
        self._animationSpeed = 500
        self._obstacles = set()
        self._checkpoints = []
        self._size = 10

        # private attributes 
        self.__cell = 45
        self.__undoStack = []



    # Public methods 

    def parseGameState(self, contents):
        # parsing the contents from the md file to redraw game state 

        try:
            # General section
            self._size = int(getMdValue(contents, 'Grid Size'))
            self.currentTurn = int(getMdValue(contents, 'Current Turn'))
            self.currentPlayerIdx = int(getMdValue(contents, 'Current Player Index'))
            self.isMultiplayer = getMdValue(contents, 'Is Multiplayer') == 'True'
            self.checkpointsReached = int(getMdValue(contents, 'Player Checkpoints Reached'))
            self.botCheckpointsReached = int(getMdValue(contents, 'Bot Checkpoints Reached'))

            # Player info
            self._playerHealth = int(getMdValue(contents, 'Player Health'))
            self.playerPos = tuple(map(int, getMdValue(contents, 'Player Position').strip("()").split(", ")))

            # Bot info
            self._botHealth = int(getMdValue(contents, 'Bot Health'))
            self.botPos = tuple(map(int, getMdValue(contents, 'Bot Position').strip("()").split(", ")))

            # Checkpoints and obstacles info 
            self._obstacles = getMdPos(contents, "Obstacle Positions")
            self._checkpoints = getMdPos(contents, 'Checkpoint Positions')

        except ValueError as e:
            messagebox.showerror("Errr", str(e))
        
        # parameter is there to so that _redrawGameState knows it needs to recreate the entire game state instead of a move undo
        self._redrawGameState(1) 

    def initialiseView(self, root):
        self.playGameView.showSelectBoardWindow() 
    
    def onBoardSelect(self, difficulty=None):
        self.__updateDifficulty(difficulty)
        self.playGameView.showOptionWindow() 
    
    def backToMain(self,token=None):
        # token is there so that if this method is called BEFORE the game starts, we just need to hide the selectBoardFrame window 

        # message asking user to confirm exit 
        confirm = messagebox.askyesno('Quit To Main Menu', 'Are you SURE you want to quit? Unsaved game will be LOST')

        if confirm: 
            self.__resetState() 
            if token: 
                self.playGameView.selectBoardFrame.pack_forget() 
            else: 
                self.playGameView.gameBoardFrame.pack_forget() 
            self.mainMenuController.displayMain() 
            self.playGameView.stopTime() 
    
    def onSinglePlayerSelect(self):
        self.isMultiplayer = False 
        self.totalPlayers = 1 
        self.playGameView.showGameBoard(isSinglePlayer=True)
        self.__singlePlayerAndBot()
    
    def onMultiplayerSelect(self):
        self.isMultiplayer = True
        self._playerHealth = 10 
        self.playGameView.showGameBoard(isSinglePlayer=False)
        self.__createRobot(playerCount=self.totalPlayers)
        self.__placeCheckpointsAndObstacles() 

        # info screen before start of multiplaer game, as soon as player clicks on Ok, the multiplayer stopwatch starts counting 
        info = messagebox.askyesno('Welcome to MULTIPLAYER mode', 'Your goal is to work as a team to get to all the checkpoints as quickly as you can. As soon as this window closes, your stopwatch will start! Click Yes to continue. Good luck!')
        if info: 
            self.playGameView.startTime() 
        else: 
            self.backToMain()

    def submitCards(self):
        self.commands = [] 

        # creating an empty slot counter to keep track of how many cards the player has dragged n dropped into register slots 
        emptySlots = 0 

        for i, register, in enumerate(self.registers): 
            card = register['model'].card
            if card: 
                self.commands.append({
                    'direction' : card.direction, 
                    'steps': card.steps
                })
            else: 
                emptySlots += 1 

        # if the user has no selected any cards, inform user 
        if emptySlots == 3: 
            messagebox.showerror('No cards found', 'Please drag and drop at least one card into the empty register slot')
        else:
            if self.isMultiplayer:
                self.__processCommands(self.commands, isBot=False, onComplete=self.__endTurn)
            else:
                self.__processCommands(self.commands, isBot=False, onComplete=self.__handleBotTurn)   
    
    def undoLastAction(self):
        if not self.__undoStack:
            messagebox.showinfo('Undo', "Can't undo anything!!") # Need to use double quotes for these!! 
            return

        # only need player moves to be undone?  
        state = self.__undoStack.pop()

        self.playerPos = state['playerPos']
        self.botPos = state['botPos']
        self._playerHealth = state['_playerHealth']
        self._botHealth = state['_botHealth']
        self.currentTurn = state['currentTurn']
        self.currentPlayerIdx = state['currentPlayerIdx']
        self.checkpointsReached = state['checkpointsReached']
        self.botCheckpointsReached = state.get('botCheckpointsReached', 0) 


        if self.isMultiplayer:
            self.multiplayerPos = state.get('multiplayerPos', self.multiplayerPos)

        # Ensure move history updates correctly
        if not self.isMultiplayer:
            self.moveHistory.append({
                'undo': True,
                'turn': self.currentTurn,
                'direction': None,
                'steps': None,
                'start': None,
                'end': None,
                'collision': False
            })
            self.botMoveHistory.append({
                'undo': True,
                'turn': self.currentTurn,
                'direction': None,
                'steps': None,
                'start': None,
                'end': None,
                'collision': False
            })

        self._redrawGameState()

        # Update labels and stuff
        self.playGameView.updateHealthLabel(self._playerHealth, isBot=False)
        self.playGameView.updateHealthLabel(self._botHealth, isBot=True)
        self.playGameView.updateTurnLabel(self.currentTurn)
        self.playGameView.updateMoveHistory(self.moveHistory, isBot=False)
        self.playGameView.updateMoveHistory(self.botMoveHistory, isBot=True)

        messagebox.showinfo('Undo', 'Last move undone!')

    def makeRegistersAndCards(self, canvas):
        self.__makeRegisters(canvas) 
        self.__createActionCards(canvas) 

    def resetCards(self): 
        canvas = self.playGameView.cardsCanvas
        self.commands = [] 
        for cardPair in self.cards: 
            cardView = cardPair['view']
            cardView.resetPosition(canvas)
   
    def makeGrid(self):
        # drawing a square grid, based on size and cell 
        for i in range(self._size):
            for j in range(self._size):
                x1 = (j+1) * self.__cell 
                y1 = (i+1)  * self.__cell 
                x2 = x1 + self.__cell 
                y2 = y1 + self.__cell 

                self.canvas.create_rectangle(x1, y1, x2, y2, fill='pink', outline='black')

        # Rank and file style labelling system. So vertical columns on left hand side are numbers and bottom row will be letters  
        for col in range(self._size):
            x = (col+1) * self.__cell + self.__cell / 2 
            y = self.__cell /2  
            file = chr(65+col) # convert 0-9 to letters 
            self.canvas.create_text(x,y,text=file) 
        
        for row in range(self._size):
            x = self.__cell / 2 
            y = (row+1) * self.__cell + self.__cell / 2 
            rank = str(row+1)
            self.canvas.create_text(x,y,text=rank)

    # Protected Methods 

    def _saveGameState(self):

        # ask the user to enter a filename to save their game state 
        valid = False 

        while not valid: 
            try: 
                filename = askstring('Save Game', 'Name your file (without extension!): ')
                if not filename: 
                    raise ValueError('Enter a filename to save game state')
                else: 
                    valid = True 
            except ValueError as e: 
                messagebox.showerror('File not named', str(e))
        
        # save to a markdown file format 
        file = f'{filename}.md'
    
        # saving file with date and time - will be useful later to sort by date on the leaderboard  
        now = datetime.now().strftime('%d-%m-%Y %H:%M')

        with open(file, 'w') as f: 
            f.write('# Robo Rally File\n')
            f.write(f"**Date Played:** {now}\n\n")

            # Summary section - will be used for parsing game state and leaderboard standings 
            f.write('## Summary\n')
            f.write(f'- **Grid Size:** {self._size}\n')
            f.write(f'- **Current Turn:** {self.currentTurn}\n')
            f.write(f'- **Current Player Index:** {self.currentPlayerIdx}\n')
            f.write(f'- **Difficulty:** {self.difficulty}\n')
            f.write(f'- **Is Multiplayer:** {self.isMultiplayer}\n')
            f.write(f'- **Player Checkpoints Reached:** {self.checkpointsReached}\n')
            f.write(f'- **Bot Checkpoints Reached:** {self.botCheckpointsReached}\n\n')

            # Storing information if it's not single player vs bot 
            if not self.isMultiplayer: 
                f.write('## Player\n')
                f.write(f'- **Player Health:** {self._playerHealth}\n')
                f.write(f'- **Player Position:** ({self.playerPos[0]}, {self.playerPos[1]})\n')
                f.write(f'- **Time Taken:** 0.0 \n\n')

                f.write('## Bot\n')
                f.write(f'- **Bot Health:** {self._botHealth}\n')
                f.write(f'- **Bot Position:** ({self.botPos[0]}, {self.botPos[1]})\n\n')

            else: 
                f.write('## Multiplayer\n')
                f.write(f'- **Time Taken:** {self.playGameView.elapsedTime:.2f} \n\n')
                        

            # Checkpoints Section
            checkpoints = ', '.join([f'({p[0]}, {p[1]})' for p in self._checkpoints])
            f.write('## Checkpoints\n')
            f.write(f'- **Checkpoint Positions:** {checkpoints}\n\n')

            # Obstacles Section
            obstacles = ', '.join([f'({p[0]}, {p[1]})' for p in self._obstacles])
            f.write('## Obstacles\n')
            f.write(f'- **Obstacle Positions:** {obstacles}\n\n')

        messagebox.showinfo('Game saved!!', f'Game saved to {file}')

    def _redrawGameState(self, token=None):
        #  token is there if this method is called by the parseGameState instead of the Undo, we want to redraw the entire board from scratch 
        if token:
            self.playGameView.showGameBoard(isSinglePlayer=True)
        
        # first delete everything on the canvas then recreate the grid 
        self.canvas.delete('all')
        self.makeGrid()  
        
        # redraw player and bot positions on the grid 
        row, col = self.playerPos
        x1 = col * self.__cell + self.__cell / 4
        y1 = row * self.__cell + self.__cell / 4
        x2 = x1 + self.__cell / 2
        y2 = y1 + self.__cell / 2
        self.playerId = self.canvas.create_oval(x1, y1, x2, y2, fill='light blue')
        self.playerLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='P')

        if not self.isMultiplayer: 
            row, col = self.botPos
            x1 = col * self.__cell + self.__cell / 4
            y1 = row * self.__cell + self.__cell / 4
            x2 = x1 + self.__cell / 2
            y2 = y1 + self.__cell / 2
            self.botId = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
            self.botLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='B')

        # redraw cp's and obstacles   
        self.__placeCheckpoints(self._checkpoints)
        self.__placeObstacles(self._obstacles)
        
        # Update labels and progress bars in playGameView 
        self.playGameView.updateTurnLabel(self.currentTurn)
        self.playGameView.updateHealthLabel(self._playerHealth, isBot=False)
        self.playGameView.updateHealthLabel(self._botHealth, isBot=True)
        self.playGameView.updateProgressBar(self.checkpointsReached)
        self.playGameView.updateBotProgress(self.botCheckpointsReached)

        # if we are loading from a saved file, then hide the main menu and move history 
        if token: 
            self.mainMenuController.hideMain() 
            self.playGameView.moveHistoryFrame.grid_forget() 

    def _makeCustomBoard(self):

        # using exception handling to ensure user enters a sensible numbers for grid size and obstacles. 
        # eg - if the grid size is 10, the obstacles cannot be more than 100 

        valid = False 
        while not valid: 
            try: 
                players = simpledialog.askinteger('PLAYERS', 'Enter number of players', parent=self.root)
                size = simpledialog.askinteger('GRID SIZE', 'Enter a grid size. (Range is 5-20 inclusive)', parent=self.root)
                obstacles = simpledialog.askinteger('OBSTACLES', 'Enter number of obstacles', parent=self.root)
                checkpoints = simpledialog.askinteger('CHECKPOINTS', 'Enter number of Checkpoints', parent=self.root)
            except ValueError:
                print('nope!')
            else: 
                if size <5 or size > 20:
                    messagebox.showerror('Error', 'Enter grid size between 5 and 20')
                elif obstacles > int((size*size) - players ): 
                    messagebox.showerror('Error', 'Enter sensible number of obstacles')
                elif checkpoints > int((size*size) + obstacles): 
                    messagebox.showerror('Error', 'Enter sensible number of checkpoints')
                else: 
                    valid = True 

        self.difficulty = 'CUSTOM'

        self.totalPlayers = int(players)
        self._size = int(size) 
        
        self._obstacleCount = int(obstacles)
        self._checkpointCount = int(checkpoints)

        # NEED SOME MATHS TO FIX THE CELL SIZE BELOW... 

        # width and heigh infor from playgameview canvas 
        width = 600  
        height = 600  
        # don't go beyond 500 
        maxSize = min(width, height, 500)  
        # min size is 25 
        self.__cell = max(25, maxSize // self._size) 

        # print(f"Size: {self._size}, cell = {self.__cell}")

        self.onMultiplayerSelect() 

  
    # Private Methods 

    def __resetState(self):
        # this method is called whenever user going back to main, this resets the player count, move history, etc. so that if the player chooses a different option, the game renders properly 

        self.currentTurn = 1
        self.isMultiplayer = False
        self.totalPlayers = 4
        self.checkpointsReached = 0 
        self.botCheckpointsReached = 0 
        self.currentPlayerIdx = 0 

        self.difficulty = '' 

        self.cards = []
        self.registers = [] 

        self.moveHistory = []
        self.botMoveHistory = []

        self.playerPos = None
        self.botPos = None
        self.playerId = None
        self.playerLabel = None
        self.botId = None
        self.botLabel = None

        # protected attributes 
        self._playerHealth = 5
        self._botHealth = 5
        self._obstacleCount = 5
        self._checkpointCount = 10
        self._animationSpeed = 500
        self._obstacles = set()
        self._checkpoints = []
        self._size = 10

        # private attributes 
        self.__cell = 45
        self.__undoStack = [] 
    
    def __updateDifficulty(self, difficulty):
        # updates obstacles and checkpoints to reflect change in difficulty 
        if difficulty == 'EASY':
            self.difficulty = 'EASY'
            self._obstacleCount = 5 
            self._checkpointCount = 15
        elif difficulty == 'MEDIUM':
            self.difficulty = 'MEDIUM'
            self._checkpointCount = 10 
            self._obstacleCount = 10
        elif difficulty == 'HARD':
            self.difficulty = 'HARD'
            self._checkpointCount = 10 
            self._obstacleCount = 25  
        else: 
            self._checkpointCount = 10
            self._obstacleCount = 10

    def __singlePlayerAndBot(self):
        # Generate random starting positions for player and bot - making usre they don't overlap with obstacles or checkpoints 

        exclude = set(self._checkpoints + list(self._obstacles))

        self.playerPos = generateRandomSquares(1, exclude, self._size)[0]
        exclude.add(self.playerPos)

        self.botPos = generateRandomSquares(1, exclude, self._size)[0]
        exclude.add(self.botPos)

        row, col = self.playerPos
        x1 = col * self.__cell + self.__cell / 4
        y1 = row * self.__cell + self.__cell / 4
        x2 = x1 + self.__cell / 2
        y2 = y1 + self.__cell / 2
        self.playerId = self.canvas.create_oval(x1, y1, x2, y2, fill='light blue')
        self.playerLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='P')

        row, col = self.botPos
        x1 = col * self.__cell + self.__cell / 4
        y1 = row * self.__cell + self.__cell / 4
        x2 = x1 + self.__cell / 2
        y2 = y1 + self.__cell / 2
        self.botId = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
        self.botLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='B')

        self.__placeCheckpointsAndObstacles()
    
    def __placeCheckpointsAndObstacles(self):
        # Start with positions ALREADY taken by checkpoints/obstacles/players so that they don't overlap! 
        if self.isMultiplayer:
            exclude = set(self.multiplayerPos + list(self._obstacles))
        else:
            exclude = set([self.playerPos, self.botPos] + list(self._obstacles))  

        # generate random obstacles and checkpoints - again adding to exclude set so that they don't overlap 
        obstacles = generateRandomSquares(self._obstacleCount, exclude, self._size)
        self._obstacles.update(obstacles)
        exclude.update(obstacles)

        checkpoints = generateRandomSquares(self._checkpointCount, exclude, self._size)
        self._checkpoints.extend(checkpoints)

        # NOW place obstacles and checkpoints on canvas
        self.__placeObstacles(obstacles)
        self.__placeCheckpoints(checkpoints)
    
    def __processCommands(self, commands, index=0, isBot=False, onComplete=None):
        # print(isBot) # debug prints for bot... 
        if index < len(commands):
            command = commands[index]
            direction = command['direction']
            steps = command['steps']

            # checking robot type status 
            if isBot:
                robotPos = self.botPos
                moveHistory = self.botMoveHistory
            elif self.isMultiplayer:
                robotPos = self.multiplayerPos[self.currentPlayerIdx]
                moveHistory = self.moveHistory
            else:
                robotPos = self.playerPos
                moveHistory = self.moveHistory

            # Update move history in playGameView at the start of robot turn 
            startPos = convertToRankAndFile(*robotPos)
            if not self.isMultiplayer: 
                moveHistory.append({
                    'undo' : False,
                    'turn': self.currentTurn,
                    'player' : 'Bot' if isBot else 'Player',
                    'direction': direction,
                    'steps': steps,
                    'start': startPos,
                    'end': None,  
                    'collision': False  
                })

            self.__moveRobot(
                direction, 
                steps, 
                stepCount=0, 
                isBot = isBot,
                onComplete=lambda: self.__processCommands(commands,index+1, isBot, onComplete))
        else: 
            if onComplete:
                onComplete() 

    def __placeObstacles(self, obstaclePos):
        # get the obstacle position and draw the obstacle 
        for row, col in obstaclePos:
            x1 = col*self.__cell 
            y1 = row*self.__cell  
            x2 = x1 + self.__cell  
            y2 = y1 + self.__cell 

            self.canvas.create_rectangle(x1,y1,x2,y2,fill='gray', outline='black')
    
    def __placeCheckpoints(self, checkpointPos):
        self.checkpointIds = {} 

        for row, col in checkpointPos:
            x1 = col*self.__cell 
            y1 = row*self.__cell  
            x2 = x1+self.__cell  
            y2 = y1+self.__cell  

            # this is making green triangle 
            checkpointId = self.canvas.create_polygon(
                x1+self.__cell /2, y1+self.__cell /4, 
                x1+self.__cell /4, y1+3*self.__cell /4, 
                x1+3*self.__cell /4, y1+3*self.__cell /4, 
                fill='green', 
                outline='black'
            )
            self.checkpointIds[(row, col)] = checkpointId
            #self._checkpoints.append((row, col))

    def __checkForCheckpoint(self):

        # function to check if/when the user LANDS on the checkpoint (cp) only

        if self.isMultiplayer:
            for i, position in enumerate(self.multiplayerPos):
                if position in self._checkpoints:
                    self.__handleCheckpoint(i, position)
                
        else:
            if self.playerPos in self._checkpoints:
                self.__handleCheckpoint('P', self.playerPos)
            
            if self.botPos in self._checkpoints:
                self.__handleCheckpoint('B', self.botPos)

    def __handleCheckpoint(self, turn, position):

        # remove cp first 
        self._checkpoints.remove(position)

        # delete cp from canvas by matching with its id 
        checkpointId = self.checkpointIds.pop(position, None)
        if checkpointId:
            self.canvas.delete(checkpointId)
        
        # health +1 
        if turn == 'P':
            self._playerHealth = self._playerHealth +1
            self.playGameView.updateHealthLabel(self._playerHealth, isBot=False)
        
        elif turn == 'B':
            self._botHealth = self._botHealth +1 
            self.playGameView.updateHealthLabel(self._botHealth, isBot=True)
        
        # in case of multiplaer as self._playerHealth is used as player label for both single player vs bot and multiplaer 
        else: 
            self._playerHealth = self._playerHealth +1 
            self.playGameView.updateHealthLabel(self._playerHealth, isBot=False)
        
        # update cp progress 
        if turn == 'B':
            self.botCheckpointsReached += 1 
            self.playGameView.updateBotProgress(self.botCheckpointsReached)
        
        else: 
            self.checkpointsReached +=1 
            self.playGameView.updateProgressBar(self.checkpointsReached)
        
        # messagebox time!! 
        messagebox.showinfo('Checkpoint Reached!!', f"{'Bot' if turn=='B' else 'Player'} reached checkpoint and gained 1 health at {convertToRankAndFile(*position)}!!")
        if self.checkpointsReached + self.botCheckpointsReached >= self._checkpointCount:
            self.__gameOver() 

    def __moveRobot(self, direction, steps, stepCount=0, onComplete=None, isBot=False):

        # save the game state to a stack at the start in case of an undo
        self.__saveToUndoStack() 

        # First need to check which bot is moving 
        if isBot:
            robotPos = self.botPos
            health = self._botHealth
            history = self.botMoveHistory
            id = self.botId
            label = self.botLabel
            # print(f'Current pos: {robotPos}')
            
        elif self.isMultiplayer:
            robotPos = self.multiplayerPos[self.currentPlayerIdx]
            id = self.playerIds[self.currentPlayerIdx]
            label = self.playerLabels[self.currentPlayerIdx]
            health = self._playerHealth

        else:
            robotPos = self.playerPos
            health = self._playerHealth
            history = self.moveHistory
            id = self.playerId
            label = self.playerLabel

        # Current pos
        row, col = robotPos

        if direction == 'UP':
            row -= 1
        elif direction == 'DOWN':
            row += 1
        elif direction == 'LEFT':
            col -= 1
        elif direction == 'RIGHT':
            col += 1

        # now check for obstacles and going off grid and update -1 to health and update move history 
        if (row, col) in self._obstacles:
            if isBot: 
                self._botHealth -=1  
                health = self._botHealth
            else: 
                self._playerHealth -= 1 
                health = self._playerHealth

            if not self.isMultiplayer:
                history[-1]['end'] = convertToRankAndFile(row, col)
                history[-1]['collision'] = True

            # Update health 
            self.playGameView.updateHealthLabel(health, isBot=isBot)

            # Check for game over 
            if health <= 0: 
                self.__gameOver()
                return 

            messagebox.showinfo(
                'Collision!!',
                f"{'Bot' if isBot else 'Player'} has a collision!"
            )
            if onComplete:
                onComplete()
            return

        # checking for going off grid 
        if self.__checkForBounds(row, col): 
            if isBot: 
                self._botHealth -=1  
                health = self._botHealth
            else: 
                self._playerHealth -= 1 
                health = self._playerHealth

            if not self.isMultiplayer: 
                history[-1]['end'] = convertToRankAndFile(row, col)
                history[-1]['collision'] = True

            # Update health     
            self.playGameView.updateHealthLabel(health, isBot=isBot)

            # Check for game over 
            if health <= 0: 
                self.__gameOver()
                return 

            messagebox.showinfo(
                'Gone off grid!',
                f"{'Bot' if isBot else 'Player'} has gone off grid!"
            )
            if onComplete:
                onComplete()
            return

        # Update robot position
        if isBot:
            self.botPos = (row, col)
        elif self.isMultiplayer:
            self.multiplayerPos[self.currentPlayerIdx] = (row, col)
        else:
            self.playerPos = (row, col)


        # Calculate new coordinates
        x1 = (col) * self.__cell + self.__cell / 4
        y1 = (row) * self.__cell + self.__cell / 4
        x2 = x1 + self.__cell / 2
        y2 = y1 + self.__cell / 2

        # Update robot's position on the canvas
        self.canvas.coords(id, x1, y1, x2, y2)
        self.canvas.coords(label, (x1 + x2) / 2, (y1 + y2) / 2)


        # Continue animating steps if more remain
        if stepCount + 1 < steps:
            self.canvas.after(
                self._animationSpeed, 
                self.__moveRobot, 
                direction, 
                steps, 
                stepCount + 1, 
                onComplete, 
                isBot)

        else: 
            if not self.isMultiplayer:
                # update move history 
                history[-1]['end'] = convertToRankAndFile(row,col)
                self.playGameView.updateMoveHistory(history, isBot)

                # calling onComplete 
            if onComplete: 
                onComplete() 

    def __gameOver(self):
        # game can either finish if player/bot health dies or if all checkpoints have been reached!! 

        if self.checkpointsReached + self.botCheckpointsReached >= self._checkpointCount:
            if self.checkpointsReached > self.botCheckpointsReached: 
                winner = 'Player'
            elif self.botCheckpointsReached > self.checkpointsReached:
                winner= 'Bot'
            else: 
                winner = 'Tie'
            
            if winner == 'Tie':
                messagebox.showinfo('GAME OVER', f"It's a TIE! Player and Bot reached an equal number of checkpoints. Save Game or Return to Main Menu")
                save = messagebox.askyesno('SAVE GAME?', 'Would you like to save your Game?')
                if save: 
                    self._saveGameState()
                else: 
                    self.backToMain() 
                
            else: 
                messagebox.showinfo('GAME OVER', f'{winner} won! Save Game or Return to Main Menu')
                save = messagebox.askyesno('SAVE GAME?', 'Would you like to save your Game?')
                if save: 
                    self._saveGameState()
                else: 
                    self.backToMain() 

        if self._playerHealth > self._botHealth: 
            winner = 'Player'
            # Of course, very sensible variable names 
            notWinner  = 'Bot'
        
            messagebox.showinfo('GAME OVER', f'{notWinner} health is 0. {winner} wins! Save Game or Return to Main Menu')
            save = messagebox.askyesno('SAVE GAME?', 'Would you like to save your Game?')
            if save: 
                self._saveGameState()
            else: 
                self.backToMain() 

        else:
            messagebox.showinfo('GAME OVER', f'Overall health is 0! Save Game or Return to Main Menu')
            save = messagebox.askyesno('SAVE GAME?', 'Would you like to save your Game?')
            if save: 
                self._saveGameState()
            else: 
                self.backToMain() 

    def __checkForBounds(self,row, col):
        # method to see if the robot has gone off grid 
        if row< 1 or row > self._size or col <1 or col > self._size: 
            # print(row, col)
            return True 
        else: 
            # print(row,col)
            return False 

    def __createActionCards(self, canvas):
        # initialising the controller to handle drag and drop for cards into register slots 
        self.cardsController = DragAndDropController(self.playGameView.cardsCanvas)

        # create 5 random cards for user- choose 1 random directions and 1,2, or 3 steps for each direction
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for i in range(5):
            direction = random.choice(directions)
            steps = random.randint(1, 3)

            # initialising card model and view 
            cardModel = model.CardModel(direction, steps)
            cardView = view.CardView(
                canvas,
                x=5 + i * 80,
                y=150,  
                width=75,
                height=50,
                text=f"{direction} {steps}"
            )

            # storing model and view in controller (as a dictionary)
            self.cards.append({'model':cardModel, 'view':cardView})

            # binding drag n drop to cards so that user can drag and drop cards on the canvas  
            canvas.tag_bind(cardView.cardId, '<ButtonPress-1>', lambda e, card=cardView: self.cardsController.startDrag(e, card))
            canvas.tag_bind(cardView.cardId, '<B1-Motion>', lambda e, card=cardView: self.cardsController.continueDrag(e, card))
            canvas.tag_bind(cardView.cardId, '<ButtonRelease-1>', lambda e, card=cardView: self.cardsController.endDrag(e, card, self.cards, self.registers))

    def __createRobot(self, playerCount):
        # This method create robot for multiplayer/custom no.of players 

        self.multiplayerPos = [] 
        self.playerLabels = [] 
        self.playerIds = [] 

        colours = ['SpringGreen2', 'yellow', 'firebrick1', 'cyan2', 'deep pink', 'DarkOrchid1', 'goldenrod1']
        exclude = set(self._checkpoints + list(self._obstacles)) 

        for i in range(playerCount):
            # Generate a random position for the player, ensuring no overlap
            startPos = generateRandomSquares(self.totalPlayers, exclude, self._size)[0]
            self.multiplayerPos.append(startPos)
            exclude.add(startPos)  # Immediately add to exclude set

            # Convert to canvas coordinates
            row, col = startPos
            x1 = col * self.__cell + self.__cell / 4
            y1 = row * self.__cell + self.__cell / 4
            x2 = x1 + self.__cell / 2
            y2 = y1 + self.__cell / 2

            # Draw player bot 
            playerId = self.canvas.create_oval(x1, y1, x2, y2, fill=colours[i])
            self.playerIds.append(playerId)

            # Add label
            label = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f'P{i + 1}')
            self.playerLabels.append(label)
    
    def __makeRegisters(self, canvas):
        # initilise register model and view to store state and store them in the controller (similar to cards - as a dict)
        for i in range(3):
            registerModel = model.RegisterModel()
            registerView = view.RegisterView(
                canvas,
                x=40 + i * 150,
                y=50,  
                width=75,
                height=50,
                colour='black'
            )
            self.registers.append({'model': registerModel, 'view': registerView})
    
    def __clearRegisterAndCards(self):
        # clear the cards and registers from the canvas at the start of new turn 

        canvas = self.playGameView.cardsCanvas

        for cardPair in self.cards: 
            cardView = cardPair['view']
            canvas.delete(cardView.cardId)
            canvas.delete(cardView.textId)
        self.cards =[]
        self.__createActionCards(canvas) 

        for register in self.registers:
            register['model'].card = None 
        self.registers = [] 

        self.__makeRegisters(canvas)   
    
    def __handleBotTurn(self):
        # handles the bot turn, can be either random or using the A* pathfinding 
        if not self.isMultiplayer:
            botCommands = generateBotMoves(self.botPos, self._checkpoints, self._obstacles, self._size) 
            #botCommands = generateRandomBotMoves()
            self.__processCommands(botCommands, index=0, isBot=True, onComplete=self.__endTurn)
            # print('onto bot turn now!!')
        
    def __endTurn(self):
        # end of turn logic, if multiplayer, go onto next player and wrap around to player 1 at the end. 
        # for single player, just increment the turn counter 
        # clear registers and cards and check for checkpoint 

        if self.isMultiplayer:
            self.currentPlayerIdx = (self.currentPlayerIdx + 1) % self.totalPlayers
            if self.currentPlayerIdx == 0:
                self.currentTurn += 1
            self.playGameView.updateTurnLabel(f"Player {self.currentPlayerIdx + 1}'s Turn")
            self.__clearRegisterAndCards()
        else:
            self.currentTurn += 1
            self.playGameView.updateTurnLabel(self.currentTurn)
            self.__clearRegisterAndCards()
        
        self.__checkForCheckpoint()

    def __saveToUndoStack(self):
        # saving relevant info to a stack for undo 
        state = {
        'playerPos': self.playerPos,
        'playerLabel':self.playerLabel,
        'botPos': self.botPos,
        'botLabel':self.botLabel,
        '_playerHealth': self._playerHealth,
        '_botHealth': self._botHealth,
        'currentTurn': self.currentTurn,
        'currentPlayerIdx': self.currentPlayerIdx,
        'moveHistory': list(self.moveHistory),  
        'botMoveHistory': list(self.botMoveHistory),  
        'checkpointsReached': self.checkpointsReached,
    }
        self.__undoStack.append(state)


