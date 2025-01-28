import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox
import random 
from datetime import datetime
import re 
from tkinter import simpledialog
from tkinter.simpledialog import askstring

from View.playGameView import PlayGameView
from Controller.mainMenuController import MainMenuController
from View.mainMenuView import MainMenuView
from cardsAndRegisters import model
from cardsAndRegisters import view
from cardsAndRegisters.controller import DragAndDropController

from Controller.helperFunctions import generateRandomSquares, convertToRankAndFile, getMdPos, getMdValue
from Controller.botLogic import generateBotMoves

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

        # private attributes 
        self.__cell = 50
        self.__size = 10
        self.__undoStack = []



    # Public methods 

    def parseGameState(self, contents):
        try:
            # General section
            self.__size = int(getMdValue(contents, 'Grid Size'))
            self.currentTurn = int(getMdValue(contents, 'Current Turn'))
            self.currentPlayerIdx = int(getMdValue(contents, 'Current Player Index'))
            self.isMultiplayer = getMdValue(contents, 'Is Multiplayer') == 'True'
            self.checkpointsReached = int(getMdValue(contents, 'Checkpoints Reached'))

            # Player info
            self._playerHealth = int(getMdValue(contents, 'Player Health'))
            self.playerPos = tuple(map(int, getMdValue(contents, 'Player Position').strip("()").split(", ")))

            # Bot info
            self._botHealth = int(getMdValue(contents, 'Bot Health'))
            self.botPos = tuple(map(int, getMdValue(contents, 'Bot Position').strip("()").split(", ")))

            # Checkpoints and obs-ta-cles info 
            self._checkpoints = getMdPos(contents, 'Checkpoint Positions')
            self._obstacles = getMdPos(contents, "Obstacle Positions")

            # # debug prints 
            # print(f'Checkpoitn parse debug- {self._checkpoints}')
            # print(f'Obstacle prase debug- {self._obstacles}')

        except ValueError as e:
            messagebox.showerror("Errr", str(e))
        
        self._redrawGameState() 

    def initialiseView(self, root):
        self.playGameView.showSelectBoardWindow() 
    
    def onBoardSelect(self, difficulty=None):
        self.__updateDifficulty(difficulty)
        self.playGameView.showOptionWindow() 
    
    # generic button to take user back to main menu 
    def backToMain(self,token=None):
        if token: 
            self.playGameView.selectBoardFrame.pack_forget() 
        else: 
            self.playGameView.gameBoardFrame.pack_forget() 
        self.mainMenuController.displayMain() 
    
    def onSinglePlayerSelect(self):
        self.isMultiplayer = False 
        self.totalPlayers = 1 
        self.playGameView.showGameBoard(isSinglePlayer=True)
        self.__singlePlayerAndBot()
    
    def onMultiplayerSelect(self):
        self.isMultiplayer = True
        self.playGameView.showGameBoard(isSinglePlayer=False)
        self.__createRobot(playerCount=self.totalPlayers)
        self.__placeCheckpointsAndObstacles() 
    
    def submitCards(self):
        commands = [] 
        for i, register, in enumerate(self.registers): 
            card = register['model'].card
            if card: 
                commands.append({
                    'direction' : card.direction, 
                    'steps': card.steps
                })
            else: 
                print('Whoops! No cards')
        
        if self.isMultiplayer:
            # Process only the active player's commands
            self.__processCommands(commands, isBot=False, onComplete=self.__endTurn)
        else:
            # Single-player: handle bot after player
            self.__processCommands(commands, isBot=False, onComplete=self.__handleBotTurn)  
    
    def undoLastAction(self):
        if not self.__undoStack:
            messagebox.showinfo('Undo', "Can't undo anything!!") # Need to use double quotes for these!! 
            return
        state = self.__undoStack.pop()

        self.playerPos = state['playerPos']
        self.playerLabel = state['playerLabel']
        self.botPos = state['botPos']
        self.botLabel = state['botLabel']
        self._playerHealth = state['_playerHealth']
        self._botHealth = state['_botHealth']
        self.currentTurn = state['currentTurn']
        self.currentPlayerIdx = state['currentPlayerIdx']
        self.moveHistory = state['moveHistory']
        self.botMoveHistory = state['botMoveHistory']
        self.checkpointsReached = state['checkpointsReached']

        self._redrawGameState() 

    def makeRegistersAndCards(self, canvas):
        self.__makeRegisters(canvas) 
        self.__createActionCards(canvas) 

    def resetCards(self): 
        canvas = self.playGameView.cardsCanvas
        for cardPair in self.cards: 
            cardView = cardPair['view']
            cardView.resetPosition(canvas)
   
    def makeGrid(self):
        # draw the actual grid 
        for i in range(self.__size):
            for j in range(self.__size):
                x1 = (j+1) * self.__cell 
                y1 = (i+1)  * self.__cell 
                x2 = x1 + self.__cell 
                y2 = y1 + self.__cell 

                self.canvas.create_rectangle(x1, y1, x2, y2, fill='pink', outline='black')

        # letters 
        for col in range(self.__size):
            x = (col+1) * self.__cell + self.__cell / 2 
            y = self.__cell /2  
            file = chr(65+col) # convert 0-9 to letters 
            self.canvas.create_text(x,y,text=file) 
        
        # steps labels 
        for row in range(self.__size):
            x = self.__cell / 2 
            y = (row+1) * self.__cell + self.__cell / 2 
            rank = str(row+1)
            self.canvas.create_text(x,y,text=rank)

    # Protected Methods 


    def _saveGameState(self):
        filename = askstring('Save Game', 'Name your file (without extension!): ')
        if not filename: 
            messagebox.showinfo('Enter a file name you dummy')
            return 
        
        file = f'{filename}.md'

        # save it with current date n time- will could be useful to show on leaderboard later 
        now = datetime.now().strftime('%d-%m-%Y %H:%M')

        with open(file, 'w') as f: 
            f.write('# Robo Rally File\n')
            f.write(f"**Date Played:** {now}\n\n")

            # Start with summary!
            f.write('## Summary\n')
            f.write(f'- **Grid Size:** {self.__size}\n')
            f.write(f'- **Current Turn:** {self.currentTurn}\n')
            f.write(f'- **Current Player:** {self.currentPlayerIdx}\n')
            f.write(f'- **Difficulty:** {self.difficulty}\n')
            f.write(f'- **Is Multiplayer:** {self.isMultiplayer}\n')
            f.write(f'- **Checkpoints Reached:** {self.checkpointsReached}\n\n')

            # Player and multiplayer stuff 
            if not self.isMultiplayer: 
                f.write('## Player\n')
                f.write(f'- **Player Health:** {self._playerHealth}\n')
                f.write(f'- **Player Position:** ({self.playerPos[0]}, {self.playerPos[1]})\n\n')
            else: 
                f.write('## Multiplayer\n')
                positions = '', ''.join([f'({p[0]}, {p[1]})' for p in self.multiplayerPos])
                f.write(f'- **Positions:** {positions}\n')
                f.write(f'- **Current Player Index:** {self.currentPlayerIdx}\n\n')

            # need to initilaise isBot at some point 
            # Bot stuff
            f.write('## Bot\n')
            f.write(f'- **Bot Health:** {self._botHealth}\n')
            f.write(f'- **Bot Position:** ({self.botPos[0]}, {self.botPos[1]})\n\n')

            # Checkpoints Section
            checkpoints = ', '.join([f'({p[0]}, {p[1]})' for p in self._checkpoints])
            f.write('## Checkpoints\n')
            f.write(f'- **Checkpoint Positions:** {checkpoints}\n\n')

            # Obstacles Section
            obstacles = ', '.join([f'({p[0]}, {p[1]})' for p in self._obstacles])
            f.write('## Obstacles\n')
            f.write(f'- **Obstacle Positions:** {obstacles}\n\n')

        messagebox.showinfo('Game saved!!', f'Game saved to {file}')

    def _redrawGameState(self):
        self.playGameView.showGameBoard(isSinglePlayer=True)
        self.canvas.delete('all')
        self.makeGrid()  
        row, col = self.playerPos
        x1 = col * self.__cell + self.__cell / 4
        y1 = row * self.__cell + self.__cell / 4
        x2 = x1 + self.__cell / 2
        y2 = y1 + self.__cell / 2
        self.playerId = self.canvas.create_oval(x1, y1, x2, y2, fill='light blue')
        self.playerLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='P')

        # Redraw bot
        row, col = self.botPos
        x1 = col * self.__cell + self.__cell / 4
        y1 = row * self.__cell + self.__cell / 4
        x2 = x1 + self.__cell / 2
        y2 = y1 + self.__cell / 2
        self.botId = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
        self.botLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='B')
        
        self.__placeCheckpoints(self._checkpoints)

        # Redraw obstacles
        self.__placeObstacles(self._obstacles)
        
        # Update labels and progress
        self.playGameView.updateTurnLabel(self.currentTurn)
        self.playGameView.updateHealthLabel(self._playerHealth, isBot=False)
        self.playGameView.updateHealthLabel(self._botHealth, isBot=True)
        self.playGameView.updateProgressBar(self.checkpointsReached)

        self.mainMenuController.hideMain() 
        self.playGameView.moveHistoryFrame.pack_forget() 


    def _makeCustomBoard(self):

        players = simpledialog.askstring('Input', 'Enter number of players', parent=self.root)
        size = simpledialog.askstring('Input', 'Enter a grid size. Max size of 20', parent=self.root)
        obstacles = simpledialog.askstring('Input', 'Enter number of obstacles', parent=self.root)
        checkpoints = simpledialog.askstring('Input', 'Enter number of Checkpoints', parent=self.root)

        self.totalPlayers = int(players)
        self.__size = int(size) 
        # NEED SOME MATHS TO FIX THE CELL SIZE BELOW... 
        self.__cell = 25
        self._obstacleCount = int(obstacles)
        self._checkpointCount = int(checkpoints)

        self.onMultiplayerSelect() 

  
    # Private Methods 

    
    def __updateDifficulty(self, difficulty):
        if difficulty == 'EASY':
            self.difficulty = 'EASY'
            self._obstacleCount = 5 
            self._checkpointCount = 20 
        elif difficulty == 'MEDIUM':
            self.difficulty = 'MEDIUM'
            self._checkpointCount = 10 
            self._obstacleCount = 5
        elif difficulty == 'HARD':
            self.difficulty = 'HARD'
            self._checkpointCount = 5 
            self._obstacleCount = 20  
        else: 
            self._checkpointCount = 20
            self._obstacleCount = 5

    def __singlePlayerAndBot(self):
        # Generate starting positions for player and bot
        exclude = set(self._checkpoints + list(self._obstacles))

        self.playerPos = generateRandomSquares(1, exclude, self.__size)[0]
        exclude.add(self.playerPos)

        self.botPos = generateRandomSquares(1, exclude, self.__size)[0]
        exclude.add(self.botPos)

        row, col = self.playerPos
        x1 = col * self.__cell + self.__cell / 4
        y1 = row * self.__cell + self.__cell / 4
        x2 = x1 + self.__cell / 2
        y2 = y1 + self.__cell / 2
        self.playerId = self.canvas.create_oval(x1, y1, x2, y2, fill='light blue')
        self.playerLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='P')

        # Drawing bot - I know this is so inefficinet but hey ho... 
        row, col = self.botPos
        x1 = col * self.__cell + self.__cell / 4
        y1 = row * self.__cell + self.__cell / 4
        x2 = x1 + self.__cell / 2
        y2 = y1 + self.__cell / 2
        self.botId = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
        self.botLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='B')

        self.__placeCheckpointsAndObstacles()
    
    def __placeCheckpointsAndObstacles(self):
        # Start with positions already taken by checkpoints, obstacles, and players
        if self.isMultiplayer:
            exclude = set(self.multiplayerPos + list(self._obstacles))  # Multiplayer robots
        else:
            exclude = set([self.playerPos, self.botPos] + list(self._obstacles))  # Single-player positions

        # Generate obstacles
        obstacles = generateRandomSquares(self._obstacleCount, exclude, self.__size)
        self._obstacles.update(obstacles)
        exclude.update(obstacles)

        # Generate checkpoints
        checkpoints = generateRandomSquares(self._checkpointCount, exclude, self.__size)
        self._checkpoints.extend(checkpoints)

        # Place obstacles and checkpoints on the canvas
        self.__placeObstacles(obstacles)
        self.__placeCheckpoints(checkpoints)
    
    def __processCommands(self, commands, index=0, isBot=False, onComplete=None):
        if index < len(commands):
            command = commands[index]
            direction = command['direction']
            steps = command['steps']

            # check current robot status 
            if isBot:
                robotPos = self.botPos
                moveHistory = self.botMoveHistory
            elif self.isMultiplayer:
                robotPos = self.multiplayerPos[self.currentPlayerIdx]
                moveHistory = self.moveHistory
            else:
                robotPos = self.playerPos
                moveHistory = self.moveHistory

            # Add to move history start point
            startPos = convertToRankAndFile(*robotPos)
            if not self.isMultiplayer: 
                moveHistory.append({
                    'turn': self.currentTurn,
                    'player' : 'Bot' if isBot else 'Player',
                    'direction': direction,
                    'steps': steps,
                    'start': startPos,
                    'end': None,  # Will be updated later
                    'collision': False  # Will be updated if a collision happens
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
        for row, col in obstaclePos:
            x1 = col*self.__cell 
            y1 = row*self.__cell  
            x2 = x1 + self.__cell  
            y2 = y1 + self.__cell 

            # Draw/render the obstacle 
            self.canvas.create_rectangle(x1,y1,x2,y2,fill='gray', outline='black')
            #self._obstacles.add((row, col))
    
    def __placeCheckpoints(self, checkpointPos):
        self.checkpointIds = {} 

        for row, col in checkpointPos:
            x1 = col*self.__cell 
            y1 = row*self.__cell  
            x2 = x1+self.__cell  
            y2 = y1+self.__cell  

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

        # okay, this needs some debuggin... 
        # maybe... start with a flag for player and bot and then deal with multiplayer separately?
        playerReached = False 
        botReached = False 

        # first chek for player checkpoint, then bot checkpoint 
        if self.playerPos in self._checkpoints: 
            self._checkpoints.remove(self.playerPos)
            checkpointId = self.checkpointIds.pop(self.playerPos, None)
            playerReached = True 
            self.checkpointsReached += 1 

            if checkpointId:
                self.canvas.delete(checkpointId)
            self.playGameView.updateProgressBar(self.checkpointsReached)
            messagebox.showinfo('Checkpoint Reached!!', f'Player reached checkpoint at {convertToRankAndFile(*self.playerPos)}')
        
        if self.botPos in self._checkpoints:
            self._checkpoints.remove(self.botPos)
            checkpointId = self.checkpointIds.pop(self.botPos, None)
            botReached = True 
            self.botCheckpointsReached += 1 

            if checkpointId: 
                self.canvas.delete(checkpointId)
            self.playGameView.updateBotProgress(self.botCheckpointsReached)
            # don't need to show info for bot right? 
        
        # And NOW check for multiplayer! - need to check efor each player so use enumrate?
        if self.isMultiplayer: 
            for idx, pos in enumerate(self.multiplayerPos):
                if pos in self._checkpoints: 
                    self._checkpoints.remove(pos)
                    checkpointId = self.checkpointIds.pop(pos, None)
                    self.checkpointsReached += 1 
                    if checkpointId: 
                        self.canvas.delete(checkpointId)
                    self.playGameView.updateProgressBar(self.checkpointsReached)
                    messagebox.showinfo('Checkpoint Reached!!', f'Player {idx+1} reached checkpoint at {convertToRankAndFile(*pos)}')
    
    def __moveRobot(self, direction, steps, stepCount=0, onComplete=None, isBot=False):

        self.__saveToUndoStack() 

        # First need to check which bot is moving 
        if isBot:
            robotPos = self.botPos
            health = self._botHealth
            history = self.botMoveHistory
            id = self.botId
            label = self.botLabel
            
        elif self.isMultiplayer:
            robotPos = self.multiplayerPos[self.currentPlayerIdx]
            id = self.playerIds[self.currentPlayerIdx]
            label = self.playerLabels[self.currentPlayerIdx]

        else:
            robotPos = self.playerPos
            health = self._playerHealth
            history = self.moveHistory
            id = self.playerId
            label = self.playerLabel

        # Current position
        row, col = robotPos

        # Calculate the next step position
        if direction == 'UP':
            row -= 1
        elif direction == 'DOWN':
            row += 1
        elif direction == 'LEFT':
            col -= 1
        elif direction == 'RIGHT':
            col += 1

        # Constrain position within grid
        row = max(1, min(10, row))
        col = max(1, min(10, col))


        # check for obstacles and going off grid... 
        if not self.isMultiplayer:

            # self.__checkForBounds(row, col)

            if (row, col) in self._obstacles:
                # Update health and move history for collision
                health -=1 
                history[-1]['end'] = convertToRankAndFile(row, col)
                history[-1]['collision'] = True
                self.playGameView.updateHealthLabel(health, isBot=isBot)

                messagebox.showinfo(
                    'Collision!',
                    f"{'Bot' if isBot else 'Player'} has a collision!"
                )
                if onComplete:
                    onComplete()
                return

            # if self.__checkForBounds: 
            #     health -= 1 
            #     history[-1]['end'] = convertToRankAndFile(row, col)
            #     history[-1]['collision'] = True
            #     self.playGameView.updateHealthLabel(health, isBot=isBot)

            #     messagebox.showinfo(
            #         'Gone off grid!',
            #         f"{'Bot' if isBot else 'Player'} has gone off grid!"
            #     )
            #     if onComplete:
            #         onComplete()
            #     return

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

    def __checkForBounds(self,row, col):
                if row< 1 or row > self.__size or col <1 or col > self.__size: 
                    return True 
                else: 
                    return False 

    def __createActionCards(self, canvas):
        self.cardsController = DragAndDropController(self.playGameView.cardsCanvas)

        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for i in range(5):
            direction = random.choice(directions)
            steps = random.randint(1, 3)

            cardModel = model.CardModel(direction, steps)
            cardView = view.CardView(
                canvas,
                x=5 + i * 80,
                y=150,  # Adjust as needed
                width=75,
                height=50,
                text=f"{direction} {steps}"
            )

            # storing model and view in controller (as a dictionary)
            self.cards.append({'model':cardModel, 'view':cardView})

            # binding drag n drop stuff 
            canvas.tag_bind(cardView.cardId, '<ButtonPress-1>', lambda e, card=cardView: self.cardsController.startDrag(e, card))
            canvas.tag_bind(cardView.cardId, '<B1-Motion>', lambda e, card=cardView: self.cardsController.continueDrag(e, card))
            canvas.tag_bind(cardView.cardId, '<ButtonRelease-1>', lambda e, card=cardView: self.cardsController.endDrag(e, card, self.cards, self.registers))

            # # storing starting coords in case of a reset 
            # cardView.start_x = 100+i*150
            # cardView.start_y= 400 

    def __createRobot(self, playerCount):
        self.multiplayerPos = [] 
        self.playerLabels = [] 
        self.playerIds = [] 

        colours = ['SpringGreen2', 'yellow', 'firebrick1', 'DarkOrchid1', 'deep pink', 'cyan2', 'goldenrod1']
        exclude = set(self._checkpoints + list(self._obstacles))  # Combine checkpoints and obstacles

        for i in range(playerCount):
            # Generate a random position for the player, ensuring no overlap
            startPos = generateRandomSquares(self.totalPlayers, exclude, self.__size)[0]
            self.multiplayerPos.append(startPos)
            exclude.add(startPos)  # Immediately add to exclude set

            # Convert to canvas coordinates
            row, col = startPos
            x1 = col * self.__cell + self.__cell / 4
            y1 = row * self.__cell + self.__cell / 4
            x2 = x1 + self.__cell / 2
            y2 = y1 + self.__cell / 2

            # Draw player robot
            playerId = self.canvas.create_oval(x1, y1, x2, y2, fill=colours[i])
            self.playerIds.append(playerId)

            # Add label
            label = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f'P{i + 1}')
            self.playerLabels.append(label)
    
    def __makeRegisters(self, canvas):
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
        if not self.isMultiplayer:
            botCommands = generateBotMoves() 
            self.__processCommands(botCommands, isBot=True, onComplete=self.__endTurn)
        
    def __endTurn(self):
        if self.isMultiplayer:
            # Rotate to the next player
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
        state = {
        'playerPos': self.playerPos,
        'playerLabel':self.playerLabel,
        'botPos': self.botPos,
        'botLabel':self.botLabel,
        '_playerHealth': self._playerHealth,
        '_botHealth': self._botHealth,
        'currentTurn': self.currentTurn,
        'currentPlayerIdx': self.currentPlayerIdx,
        'moveHistory': list(self.moveHistory),  # Create a copy for them! 
        'botMoveHistory': list(self.botMoveHistory),  
        'checkpointsReached': self.checkpointsReached,
    }
        self.__undoStack.append(state)


