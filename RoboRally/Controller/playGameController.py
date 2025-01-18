import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox
import random 
from datetime import datetime
import re 
from tkinter.simpledialog import askstring

from View.playGameView import PlayGameView
from cardsAndRegisters import model
from cardsAndRegisters import view
from cardsAndRegisters.controller import DragAndDropController

from Controller.helperFunctions import generateRandomSquares, convertToRankAndFile
from Controller.botLogic import generateBotMoves

class PlayGameController:
    def __init__(self, root, canvas):

        # Public attributes 
        self.root = root
        self.canvas = canvas
        self.playGameView = PlayGameView(root, self.canvas, self)
        self.currentTurn = 1
        self.isMultiplayer = False
        self.totalPlayers = 4
        self.checkpointsReached = 0 
        self.currentPlayerIdx = 0 

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

        # private attributes 
        self.__cell = 50
        self.__size = 10
        self.__undoStack = []
        self.__obstacles = set()
        self.__checkpoints = []


    # Public methods 

    def parseGameState(self, contents):
        self.__size = int(self._getMdValue(contents, 'Size').split(' x ')[0])
        self.currentTurn = int(self._getMdValue(contents, 'Current Turn'))
        self.currentPlayerIdx = int(self._getMdValue(contents, 'Current Player Index'))
        self.isMultiplayer = self._getMdValue(contents, 'Is Multiplayer') 
        self.checkpointsReached = int(self._getMdValue(contents, 'Checkpoints Reached'))
        print('reached this point!')

        if not self.isMultiplayer: 
            self._playerHealth = int(self._getMdValue(contents, 'Health', section='Player'))
            self.playerPos = self.__parsePosition(self._getMdValue(contents, 'Position', section='Player'))
        else: 
            positions = self._getMdValue(contents, 'Positions', section='Multiplayer')
            self.multiplayerPos =  [self.__parsePosition(pos.strip()) for pos in positions.split('','')]
        
        self._botHealth = int(self._getMdValue(contents, 'Health', section='Bot'))
        self.botPos = self.__parsePosition(self._getMdValue(contents, 'Position', section='Bot'))

        checkpoints = self._getMdValue(contents, 'Positions', section='Checkpoints')
        self.__checkpoints = [self.__parsePosition(pos.strip()) for pos in checkpoints.split('','')]

        obstacles = self._getMdValue(contents, 'Positions', section='Obstacles')
        self.__obstacles = {self.__parsePosition(pos.strip()) for pos in obstacles.split('','')}


        self._redrawGameState() 

    def updateDifficulty(self, difficulty):
        if difficulty == 'EASY':
            self._obstacleCount = 5 
            self._checkpointCount = 20 
        elif difficulty == 'MEDIUM':
            self._checkpointCount = 10 
            self._obstacleCount = 5
        else:
            self._checkpointCount = 5 
            self._obstacleCount = 20  

    def initialiseView(self, root):
        self.playGameView.showSelectBoardWindow() 
    
    def onBoardSelect(self, difficulty=None):
        self.updateDifficulty(difficulty)
        self.playGameView.showOptionWindow() 
    
    def onSinglePlayerSelect(self):
        self.isMultiplayer = False 
        self.totalPlayers = 1 
        self.playGameView.showGameBoard(isSinglePlayer=True)
        self.__singlePlayerAndBot()
    
    def onMultiplayerSelect(self):
        self.isMultiplayer = True
        self.totalPlayers = 4
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

    def _getMdValue(self, contents, key, section=None):
        # Check if section-specific key exists
        if section:
            section_start = f"## {section}"
            section_lines = contents[contents.index(section_start):]
            line = next((l for l in section_lines if l.startswith(f"- **{key}:**")), None)
        else:
            line = next((l for l in contents if l.startswith(f"- **{key}:**")), None)
        if line:
            return line.split(": ", 1)[1].strip()
        return None  # Return None if key is not found


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
            f.write(f'- **Grid Size:** {self.__size} x {self.__size}\n')
            f.write(f'- **Current Turn:** {self.currentTurn}\n')
            f.write(f'- **Current Player:** {self.currentPlayerIdx}\n')
            f.write(f'- **Multiplayer Game?:** {self.isMultiplayer}\n')
            f.write(f'- **Checkpoints Reached:** {self.checkpointsReached}\n\n')

            # Player and multiplayer stuff 
            if not self.isMultiplayer: 
                f.write('## Player\n')
                f.write(f'- **Health:** {self._playerHealth}\n')
                f.write(f'- **Position:** ({self.playerPos[0]}, {self.playerPos[1]})\n\n')
            else: 
                f.write('## Multiplayer\n')
                positions = '', ''.join([f'({p[0]}, {p[1]})' for p in self.multiplayerPos])
                f.write(f'- **Positions:** {positions}\n')
                f.write(f'- **Current Player Index:** {self.currentPlayerIdx}\n\n')

            # need to initilaise isBot at some point 
            # Bot stuff
            f.write('## Bot\n')
            f.write(f'- **Health:** {self._botHealth}\n')
            f.write(f'- **Position:** ({self.botPos[0]}, {self.botPos[1]})\n\n')

            # Checkpoints Section
            f.write('## Checkpoints\n')
            f.write('- **Positions:** ' + '', ''.join([f'({p[0]}, {p[1]})' for p in self.__checkpoints]) + '\n\n')

            # Obstacles Section
            f.write('## Obstacles\n')
            f.write('- **Positions:** ' + '', ''.join([f'({p[0]}, {p[1]})' for p in self.__obstacles]) + '\n\n')


        messagebox.showinfo("Save Game", f"Game state saved to {file}")

    def _redrawGameState(self):
        print('reached redraw game state')

        self.canvas.delete("all")  # Clear all canvas elements

        # Redraw the grid
        self.makeGrid()

        # Redraw player robot
        if not self.isMultiplayer:
            row, col = self.playerPos
            x1 = col * self.__cell + self.__cell / 4
            y1 = row * self.__cell + self.__cell / 4
            x2 = x1 + self.__cell / 2
            y2 = y1 + self.__cell / 2
            self.playerId = self.canvas.create_oval(x1, y1, x2, y2, fill='light blue')
            self.playerLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='P')

        # Redraw multiplayer robots
        if self.isMultiplayer:
            self.playerIds = []
            self.playerLabels = []
            colours = ['SpringGreen2', 'yellow', 'firebrick1', 'DarkOrchid1']
            for i, (row, col) in enumerate(self.multiplayerPos):
                x1 = col * self.__cell + self.__cell / 4
                y1 = row * self.__cell + self.__cell / 4
                x2 = x1 + self.__cell / 2
                y2 = y1 + self.__cell / 2
                playerId = self.canvas.create_oval(x1, y1, x2, y2, fill=colours[i])
                self.playerIds.append(playerId)
                label = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f'P{i + 1}')
                self.playerLabels.append(label)

        # Redraw bot
        row, col = self.botPos
        x1 = col * self.__cell + self.__cell / 4
        y1 = row * self.__cell + self.__cell / 4
        x2 = x1 + self.__cell / 2
        y2 = y1 + self.__cell / 2
        self.botId = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
        self.botLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='B')

        # Redraw checkpoints
        self.checkpointIds = {}
        for row, col in self.__checkpoints:
            x1 = col * self.__cell
            y1 = row * self.__cell
            x2 = x1 + self.__cell
            y2 = y1 + self.__cell
            checkpointId = self.canvas.create_polygon(
                x1 + self.__cell / 2, y1 + self.__cell / 4,
                x1 + self.__cell / 4, y1 + 3 * self.__cell / 4,
                x1 + 3 * self.__cell / 4, y1 + 3 * self.__cell / 4,
                fill='green', outline='black'
            )
            self.checkpointIds[(row, col)] = checkpointId

        # Redraw obstacles
        for row, col in self.__obstacles:
            x1 = col * self.__cell
            y1 = row * self.__cell
            x2 = x1 + self.__cell
            y2 = y1 + self.__cell
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='gray', outline='black')

        # Update the UI components
        self.playGameView.updateHealthLabel(self._playerHealth, isBot=False)
        self.playGameView.updateHealthLabel(self._botHealth, isBot=True)
        self.playGameView.updateTurnLabel(self.currentTurn)
        self.playGameView.updateProgressBar(self.checkpointsReached)

        print('done redrwaing game state')

    # Private Methods 

    def __parsePosition(self, pos):
        if pos.startswith("(") and pos.endswith(")"):
            try:
                row, col = map(int, pos[1:-1].split(","))
                return (row, col)
            except ValueError:
                raise ValueError(f"Invalid position format: {pos}")
        raise ValueError(f"Invalid position string: {pos}")

    def __singlePlayerAndBot(self):
        # Generate starting positions for player and bot
        exclude = set(self.__checkpoints + list(self.__obstacles))

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
            exclude = set(self.multiplayerPos + list(self.__obstacles))  # Multiplayer robots
        else:
            exclude = set([self.playerPos, self.botPos] + list(self.__obstacles))  # Single-player positions

        # Generate obstacles
        obstacles = generateRandomSquares(self._obstacleCount, exclude, self.__size)
        self.__obstacles.update(obstacles)
        exclude.update(obstacles)

        # Generate checkpoints
        checkpoints = generateRandomSquares(self._checkpointCount, exclude, self.__size)
        self.__checkpoints.extend(checkpoints)

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
            self.__obstacles.add((row, col))
    
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
            self.__checkpoints.append((row, col))

    def __checkForCheckpoint(self):
        if self.isMultiplayer: 
            position = self.multiplayerPos
        else: 
            position = self.playerPos

        if position in self.__checkpoints:
            # remove checkpoint first 
            self.__checkpoints.remove(position)

            # delete checkpoint 
            checkpointId = self.checkpointIds.pop(position, None)
            if checkpointId:
                self.canvas.delete(checkpointId)

            self.checkpointsReached +=1  
            
            # update progress bar in the view! 
            self.playGameView.updateProgressBar(self.checkpointsReached)
            messagebox.showinfo('Checkpoint reached!', f'Checkpoint reached at {convertToRankAndFile(*position)}') 
    
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
        if direction == 'Up':
            row -= 1
        elif direction == 'Down':
            row += 1
        elif direction == 'Left':
            col -= 1
        elif direction == 'Right':
            col += 1

        # Constrain position within grid
        row = max(1, min(10, row))
        col = max(1, min(10, col))

        # check for obstacles and going off grid... 
        if not self.isMultiplayer:
            if (row, col) in self.__obstacles:
                # Update health and move history for collision
                health -=1 
                history[-1]['end'] = convertToRankAndFile(row, col)
                history[-1]['collision'] = True
                self.playGameView.updateHealthLabel(health, isBot=isBot)

                messagebox.showinfo(
                    'Collision!',
                    f"{'Bot' if isBot else 'Player'} hit an obstacle!"
                )
                if onComplete:
                    onComplete()
                return
            
            # logic here for if robot goes off grid 
            

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

    def __createActionCards(self, canvas):
        self.cardsController = DragAndDropController(self.playGameView.cardsCanvas)

        directions = ['Up', 'Down', 'Left', 'Right', 'Up', 'Down']
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

        colours = ['SpringGreen2', 'yellow', 'firebrick1', 'DarkOrchid1']
        exclude = set(self.__checkpoints + list(self.__obstacles))  # Combine checkpoints and obstacles

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


    