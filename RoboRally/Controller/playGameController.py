import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox
import random 
import time 

from View.playGameView import PlayGameView
from cardsAndRegisters import model
from cardsAndRegisters import view
from cardsAndRegisters.controller import DragAndDropController

from Controller.helperFunctions import generateRandomSquares, convertToRankAndFile
from Controller.botLogic import generateBotMoves

class PlayGameController:
    def __init__(self, root, canvas):
        self.mainMenuController = None
        self.root = root 
        self.canvas = canvas 

        # intialise undo stack 
        self.undoStack = [] 
    
        # view initilised here - self is the playGameController
        self.playGameView = PlayGameView(root, self.canvas, self)

        # grid controls 
        self._size = 10 
        self._cell = 50 

        # Game state variables 
        self.animationSpeed = 500

        self.moveHistory = []
        self.botMoveHistory = []

        self.cards = [] 
        self.registers = [] 

        self.currentTurn = 1

        self._obstacleCount = 5
        self._checkpointCount = 20

        self.obstacles = set()
        self.checkpoints = []
        self.checkpointsReached = 0

        self.playerHealth = 5
        self.botHealth = 5

        self.isMultiplayer = False
        self.totalPlayers = 4
        self.multiplayerPos = []
        self.currentPlayerIdx = 0
    
    def initialiseView(self, root):
        self.playGameView.showSelectBoardWindow() 
    
    def backToOptions(self):
        self.playGameView.showOptionWindow() 
    
    def onBoardSelect(self):
        self.playGameView.showOptionWindow() 
    
    def onSinglePlayerSelect(self):
        self.isMultiplayer = False 
        self.totalPlayers = 1 
        self.playGameView.showGameBoard(isSinglePlayer=True)
        self.singlePlayerAndBot()
    
    def onMultiplayerSelect(self):
        self.isMultiplayer = True
        self.totalPlayers = 4
        self.playGameView.showGameBoard(isSinglePlayer=False)
        self.createRobot(playerCount=self.totalPlayers)
        self.placeCheckpointsAndObstacles() 
    
    def singlePlayerAndBot(self):
        # Generate starting positions for player and bot
        exclude = set(self.checkpoints + list(self.obstacles))

        self.playerPos = generateRandomSquares(1, exclude, self._size)[0]
        exclude.add(self.playerPos)

        self.botPos = generateRandomSquares(1, exclude, self._size)[0]
        exclude.add(self.botPos)

        row, col = self.playerPos
        x1 = col * self._cell + self._cell / 4
        y1 = row * self._cell + self._cell / 4
        x2 = x1 + self._cell / 2
        y2 = y1 + self._cell / 2
        self.playerId = self.canvas.create_oval(x1, y1, x2, y2, fill='light blue')
        self.playerLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='P')

        # Drawing bot - I know this is so inefficinet but hey ho... 
        row, col = self.botPos
        x1 = col * self._cell + self._cell / 4
        y1 = row * self._cell + self._cell / 4
        x2 = x1 + self._cell / 2
        y2 = y1 + self._cell / 2
        self.botId = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
        self.botLabel = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='B')

        self.placeCheckpointsAndObstacles()
    
    def placeCheckpointsAndObstacles(self):
        # Start with positions already taken by checkpoints, obstacles, and players
        if self.isMultiplayer:
            exclude = set(self.multiplayerPos + list(self.obstacles))  # Multiplayer robots
        else:
            exclude = set([self.playerPos, self.botPos] + list(self.obstacles))  # Single-player positions

        # Generate obstacles
        obstacles = generateRandomSquares(self._obstacleCount, exclude, self._size)
        self.obstacles.update(obstacles)
        exclude.update(obstacles)

        # Generate checkpoints
        checkpoints = generateRandomSquares(self._checkpointCount, exclude, self._size)
        self.checkpoints.extend(checkpoints)

        # Place obstacles and checkpoints on the canvas
        self.placeObstacles(obstacles)
        self.placeCheckpoints(checkpoints)
    
    def placeObstacles(self, obstaclePos):
        for row, col in obstaclePos:
            x1 = col*self._cell 
            y1 = row*self._cell  
            x2 = x1 + self._cell  
            y2 = y1 + self._cell 

            # Draw/render the obstacle 
            self.canvas.create_rectangle(x1,y1,x2,y2,fill='gray', outline='black')
            self.obstacles.add((row, col))
    
    def placeCheckpoints(self, checkpointPos):
        self.checkpointIds = {} 

        for row, col in checkpointPos:
            x1 = col*self._cell 
            y1 = row*self._cell  
            x2 = x1+self._cell  
            y2 = y1+self._cell  

            checkpointId = self.canvas.create_polygon(
                x1+self._cell /2, y1+self._cell /4, 
                x1+self._cell /4, y1+3*self._cell /4, 
                x1+3*self._cell /4, y1+3*self._cell /4, 
                fill='green', 
                outline='black'
            )
            self.checkpointIds[(row, col)] = checkpointId
            self.checkpoints.append((row, col))
    
    #checking if the robot LANDS on the checkpoint 
    def checkForCheckpoint(self):
        if self.isMultiplayer: 
            position = self.multiplayerPos
        else: 
            position = self.playerPos

        if position in self.checkpoints:
            # remove checkpoint first 
            self.checkpoints.remove(position)

            # delete checkpoint 
            checkpointId = self.checkpointIds.pop(position, None)
            if checkpointId:
                self.canvas.delete(checkpointId)

            self.checkpointsReached +=1  
            
            # update progress bar in the view! 
            self.playGameView.updateProgressBar(self.checkpointsReached)
            messagebox.showinfo('Checkpoint reached!', f'Checkpoint reached at {convertToRankAndFile(*position)}') 
    
    def makeGrid(self):
        # draw the actual grid 
        for i in range(self._size):
            for j in range(self._size):
                x1 = (j+1) * self._cell 
                y1 = (i+1)  * self._cell 
                x2 = x1 + self._cell 
                y2 = y1 + self._cell 

                self.canvas.create_rectangle(x1, y1, x2, y2, fill='pink', outline='black')

        # letters 
        for col in range(self._size):
            x = (col+1) * self._cell + self._cell / 2 
            y = self._cell /2  
            file = chr(65+col) # convert 0-9 to letters 
            self.canvas.create_text(x,y,text=file) 
        
        # steps labels 
        for row in range(self._size):
            x = self._cell / 2 
            y = (row+1) * self._cell + self._cell / 2 
            rank = str(row+1)
            self.canvas.create_text(x,y,text=rank)
    
    def makeRegistersAndCards(self, canvas):
        self.makeRegisters(canvas) 
        self.createActionCards(canvas) 
    
    def makeRegisters(self, canvas):
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
    
    def createActionCards(self, canvas):
        self.cardsController = DragAndDropController(self.playGameView.cardsCanvas)

        directions = ['Forward', 'Backward', 'Left', 'Right', 'Forward', 'Backward']
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
    
    def resetCards(self): # THIS IS BUGGY 
        canvas = self.playGameView.cardsCanvas
        for cardPair in self.cards: 
            cardView = cardPair['view']
            cardView.resetPosition(canvas)
    
    def clearRegisterAndCards(self):
        canvas = self.playGameView.cardsCanvas

        for cardPair in self.cards: 
            cardView = cardPair['view']
            canvas.delete(cardView.cardId)
            canvas.delete(cardView.textId)
        self.cards =[]
        self.createActionCards(canvas) 

        for register in self.registers:
            register['model'].card = None 
        self.registers = [] 

        self.makeRegisters(canvas)   

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
            self.processCommands(commands, isBot=False, onComplete=self.endTurn)
        else:
            # Single-player: handle bot after player
            self.processCommands(commands, isBot=False, onComplete=self.handleBotTurn)  
    
    def handleBotTurn(self):
        if not self.isMultiplayer:
            botCommands = generateBotMoves() 
            self.processCommands(botCommands, isBot=True, onComplete=self.endTurn)
        
    def endTurn(self):
        if self.isMultiplayer:
            # Rotate to the next player
            self.currentPlayerIdx = (self.currentPlayerIdx + 1) % self.totalPlayers
            if self.currentPlayerIdx == 0:
                self.currentTurn += 1
            self.playGameView.updateTurnLabel(f"Player {self.currentPlayerIdx + 1}'s Turn")
            self.clearRegisterAndCards()
        else:
            self.currentTurn += 1
            self.playGameView.updateTurnLabel(self.currentTurn)
            self.clearRegisterAndCards()
        
        self.checkForCheckpoint()

    # CREATING AND MOVING THE ROBOT 
    # Robot logic stuff begins here 
    def createRobot(self, playerCount):
        self.multiplayerPos = [] 
        self.playerLabels = [] 
        self.playerIds = [] 

        colours = ['SpringGreen2', 'yellow', 'red2', 'purple']
        exclude = set(self.checkpoints + list(self.obstacles))  # Combine checkpoints and obstacles

        for i in range(playerCount):
            # Generate a random position for the player, ensuring no overlap
            startPos = generateRandomSquares(self.totalPlayers, exclude, self._size)[0]
            self.multiplayerPos.append(startPos)
            exclude.add(startPos)  # Immediately add to exclude set

            # Convert to canvas coordinates
            row, col = startPos
            x1 = col * self._cell + self._cell / 4
            y1 = row * self._cell + self._cell / 4
            x2 = x1 + self._cell / 2
            y2 = y1 + self._cell / 2

            # Draw player robot
            playerId = self.canvas.create_oval(x1, y1, x2, y2, fill=colours[i])
            self.playerIds.append(playerId)

            # Add label
            label = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f'P{i + 1}')
            self.playerLabels.append(label)
    
    # this is more like 'animateRobotMoving' but I can't be bothered to refactor... 
    def moveRobot(self, direction, steps, stepCount=0, onComplete=None, isBot=False):

        self.saveToUndoStack() 

        # First need to check which bot is moving 
        if isBot:
            robotPos = self.botPos
            health = self.botHealth
            history = self.botMoveHistory
            id = self.botId
            label = self.botLabel
            
        elif self.isMultiplayer:
            robotPos = self.multiplayerPos[self.currentPlayerIdx]
            id = self.playerIds[self.currentPlayerIdx]
            label = self.playerLabels[self.currentPlayerIdx]

        else:
            robotPos = self.playerPos
            health = self.playerHealth
            history = self.moveHistory
            id = self.playerId
            label = self.playerLabel

        # Current position
        row, col = robotPos

        # Calculate the next step position
        if direction == 'Forward':
            row -= 1
        elif direction == 'Backward':
            row += 1
        elif direction == 'Left':
            col -= 1
        elif direction == 'Right':
            col += 1

        # Constrain position within grid
        row = max(1, min(10, row))
        col = max(1, min(10, col))

        # check for obstacles 
        if not self.isMultiplayer:
            if (row, col) in self.obstacles:
                # Update health and move history for collision
                health -=1 
                history[-1]['end'] = convertToRankAndFile(row, col)
                history[-1]['collision'] = True
                self.playGameView.updateHealthLabel(health, isBot=isBot)

                messagebox.showinfo(
                    "Collision!",
                    f"{'Bot' if isBot else 'Player'} hit an obstacle!"
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
        x1 = (col) * self._cell + self._cell / 4
        y1 = (row) * self._cell + self._cell / 4
        x2 = x1 + self._cell / 2
        y2 = y1 + self._cell / 2

        # Update robot's position on the canvas
        self.canvas.coords(id, x1, y1, x2, y2)
        self.canvas.coords(label, (x1 + x2) / 2, (y1 + y2) / 2)

        # Continue animating steps if more remain
        if stepCount + 1 < steps:
            self.canvas.after(
                self.animationSpeed, 
                self.moveRobot, 
                direction, 
                steps, 
                stepCount + 1, 
                onComplete, 
                isBot)

        else: 
            if not self.isMultiplayer:
                # update move history 
                history[-1]['end'] = convertToRankAndFile(row,col)
                self.playGameView.updateMoveHistory(history, isBot=isBot)

                # calling onComplete 
            if onComplete: 
                onComplete() 
    
     # new method to process commands in an order because submitCards and Robot methods were not doing well... 
    def processCommands(self, commands, index=0, isBot=False, onComplete=None):
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

            self.moveRobot(
                direction, 
                steps, 
                stepCount=0, 
                isBot = isBot,
                onComplete=lambda: self.processCommands(commands,index+1, isBot, onComplete))
        else: 
            if onComplete:
                onComplete() 
    
    def saveToUndoStack(self):
        state = {
        "playerPos": self.playerPos,
        'playerLabel':self.playerLabel,
        "botPos": self.botPos,
        'botLabel':self.botLabel,
        "playerHealth": self.playerHealth,
        "botHealth": self.botHealth,
        "currentTurn": self.currentTurn,
        "currentPlayerIdx": self.currentPlayerIdx,
        "moveHistory": list(self.moveHistory),  # Create a copy
        "botMoveHistory": list(self.botMoveHistory),  # Create a copy
        "multiplayerPos": list(self.multiplayerPos),  # Create a copy
        "checkpointsReached": self.checkpointsReached,
    }
        self.undoStack.append(state)
    
    def undoLastAction(self):
        if not self.undoStack:
            messagebox.showinfo("Undo", "No actions to undo!")
            return
        state = self.undoStack.pop()

        self.playerPos = state["playerPos"]
        self.playerLabel = state['playerLabel']
        self.botPos = state["botPos"]
        self.botLabel = state['botLabel']
        self.playerHealth = state["playerHealth"]
        self.botHealth = state["botHealth"]
        self.currentTurn = state["currentTurn"]
        self.currentPlayerIdx = state["currentPlayerIdx"]
        self.moveHistory = state["moveHistory"]
        self.botMoveHistory = state["botMoveHistory"]
        self.multiplayerPos = state["multiplayerPos"]
        self.checkpointsReached = state["checkpointsReached"]

        self.redrawGameState() 

    def redrawGameState(self):
        row, col = self.playerPos
        x1 = col * self._cell + self._cell / 4
        y1 = row * self._cell + self._cell / 4
        x2 = x1 + self._cell / 2
        y2 = y1 + self._cell / 2
        self.canvas.coords(self.playerId, x1, y1, x2, y2)
        self.canvas.coords(self.playerLabel, (x1 + x2) / 2, (y1 + y2) / 2)

        row, col = self.botPos
        x1 = col * self._cell + self._cell / 4
        y1 = row * self._cell + self._cell / 4
        x2 = x1 + self._cell / 2
        y2 = y1 + self._cell / 2
        self.canvas.coords(self.botId, x1, y1, x2, y2)
        self.canvas.coords(self.botLabel, (x1 + x2) / 2, (y1 + y2) / 2)

        # Update health, turn labels, and other elements in the view
        self.playGameView.updateHealthLabel(self.playerHealth, isBot=False)
        self.playGameView.updateHealthLabel(self.botHealth, isBot=True)
        self.playGameView.updateTurnLabel(self.currentTurn)
        self.playGameView.updateProgressBar(self.checkpointsReached)
    

    