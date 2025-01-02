import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox
import random 
import time 

from View.playGameView import PlayGameView
from cardsAndRegisters import model
from cardsAndRegisters import view

global cell
cell = 50

global size 
size = 10 

global checkpointCount 
checkpointCount = 20

global obstacleCount 
obstacleCount = 5 

class PlayGameController: 
    def __init__(self, root, canvas):
        self.mainMenuController = None 
        self.root = root 

        self.canvas = canvas 
        self.cards = [] 
        self.registers = [] 

        # animation speed 
        self.animationSpeed = 500

        # checkpoint 
        self.checkpointCount = checkpointCount

        # move history list - this needs to be displayed by THE VIEW 
        self.moveHistory = []
        self.botMoveHistory = [] # separate move histoyr for the bot? 

        # turn counter 
        self.currentTurn = 1 

        # obstaclessss (pronouced obs-ta-cles - yes, like the greek heros)
        self.obstacles = set() 

        # robot health! 
        self.playerHealth=5 
        self.botHealth = 5 

        # checkpoint stuff 
        self.checkpoints = [] 
        self.checkpointsReached = 0 
        self.totalCheckpoints = checkpointCount

        # multiplayer tracking stuff here 
        self.multiplayerPos = [] 
        self.currentPlayerIdx = 0 
        self.isMultiplayer = False 
        self.totalPlayers = 1 

        # view initilised here - self is the playGameController
        self.playGameView = PlayGameView(root, self.canvas, self)
    
    # bot moves - pretty random tbh... 
    def generateBotMoves(self):
        directions = ['Forward', 'Backward', 'Left', 'Right']
        botCommands = [] 

        for _ in range(3):
            direction = random.choice(directions)
            steps = random.randint(1,3)
            botCommands.append({'direction': direction, 'steps':steps})
        return botCommands

    # would be nice to be able to place random checkpoints and obstacles 
    def generateRandomSquares(self, count, exclude):
        exclude = set(exclude)
        positions = set() 
        while len(positions) < count: 
            row = random.randint(1, size-1)
            col = random.randint(1, size-1)
            if (row, col) not in exclude and (row,col) not in positions:
                positions.add((row, col))
        
        return list(positions)


    def placeCheckpointsAndObstacles(self):
        exclude = set(self.checkpoints + list(self.obstacles) + self.multiplayerPos)

        obstacles = self.generateRandomSquares(obstacleCount, exclude)
        self.obstacles.update(obstacles)
        exclude.update(obstacles) # haha, this is so that obstacles and checkpoints don't overlap!! 

        checkpoints = self.generateRandomSquares(checkpointCount, exclude)
        self.checkpoints.extend(checkpoints)

        self.placeObstacles(obstacles)
        self.placeCheckpoints(checkpoints)

    
    # method to place checkpoints 
    def placeCheckpoints(self, checkpointPos):
        self.checkpointIds = {} 

        for row, col in checkpointPos:
            pass 
            x1 = col*cell 
            y1 = row*cell 
            x2 = x1+cell 
            y2 = y1+cell 

            checkpointId = self.canvas.create_polygon(
                x1+cell/2, y1+cell/4, 
                x1+cell/4, y1+3*cell/4, 
                x1+3*cell/4, y1+3*cell/4, 
                fill='green', 
                outline='black'
            )
            self.checkpointIds[(row, col)] = checkpointId
            self.checkpoints.append((row, col))
    
    # converting to rank and file to help with move histoyr 
    def convertToRankAndFile(self, row, col):
        rank = chr(64+col)
        file = row 
        return f'{rank}{file}'

    def initialiseView(self, root):
        self.playGameView.showSelectBoardWindow() 
    
    def onBoardSelect(self):
        self.playGameView.showOptionWindow() 
    
    def onSinglePlayerSelect(self):
        self.totalPlayers = 1 
        self.playGameView.showGameBoard(isSinglePlayer=True)
        self.placeCheckpointsAndObstacles() 

    
    def onMultiplayerSelect(self):
        self.isMultiplayer = True
        self.totalPlayers = 4
        self.playGameView.showGameBoard(isSinglePlayer=False)
        self.createRobot(playerCount=self.totalPlayers)
        self.placeCheckpointsAndObstacles() 

    
    def backToOptions(self):
        self.playGameView.showOptionWindow() 
    
    def placeObstacles(self, obstaclePos):
        for row, col in obstaclePos:
            x1 = col*cell 
            y1 = row*cell 
            x2 = x1 + cell 
            y2 = y1 + cell

            # Draw/render the obstacle 
            self.canvas.create_rectangle(x1,y1,x2,y2,fill='gray', outline='black')
            self.obstacles.add((row, col))
    
    def makeGrid(self):

        # draw the actual grid 
        for i in range(size):
            for j in range(size):
                x1 = (j+1) * cell 
                y1 = (i+1)  * cell 
                x2 = x1 + cell 
                y2 = y1 + cell 

                self.canvas.create_rectangle(x1, y1, x2, y2, fill='pink', outline='black')

        # letters 
        for col in range(size):
            x = (col+1) * cell + cell / 2 
            y = cell /2  
            file = chr(65+col) # convert 0-9 to letters 
            self.canvas.create_text(x,y,text=file) 
        
        # steps labels 
        for row in range(size):
            x = cell / 2 
            y = (row+1) * cell + cell / 2 
            rank = str(row+1)
            self.canvas.create_text(x,y,text=rank)
        
        
    def createActionCards(self, canvas):
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
            canvas.tag_bind(cardView.cardId, '<ButtonPress-1>', lambda e, card=cardView: self.startDrag(e, card))
            canvas.tag_bind(cardView.cardId, '<B1-Motion>', lambda e, card=cardView: self.continueDrag(e, card))
            canvas.tag_bind(cardView.cardId, '<ButtonRelease-1>', lambda e, card=cardView: self.endDrag(e, card))

            # storing starting coords in case of a reset 
            cardView.start_x = 100+i*150
            cardView.start_y= 400 
    
    def resetCards(self):
        canvas = self.playGameView.cardsCanvas
        for cardPair in self.cards: 
            cardView = cardPair['view']
            current_x, current_y = cardView.getPosition(canvas) 
            dx = cardView.start_x - current_x
            dy = cardView.start_y - current_y
            cardView.move(canvas, dx,dy)
        
    def makeRegisters(self, canvas):
        for i in range(3):
            registerModel = model.RegisterModel()
            registerView = view.RegisterView(
                canvas,
                x=40 + i * 150,
                y=50,  # Adjust as needed
                width=75,
                height=50,
                colour='black'
            )
            self.registers.append({'model': registerModel, 'view': registerView})



    # Logic for drag and drop here 

    def startDrag(self, event, cardView):
        self.start_x = event.x
        self.start_y = event.y 
    
    def continueDrag(self, event, cardView):
        dx = event.x - self.start_x 
        dy = event.y - self.start_y 
        cardView.move(self.playGameView.cardsCanvas, dx, dy)
        self.start_x = event.x 
        self.start_y = event.y 
    
    def endDrag(self, event, cardView):
        canvas = self.playGameView.cardsCanvas
        # snap to closest register 
        closestRegister = self.findClosestRegister(event.x, event.y)
        if closestRegister: 
            register = closestRegister['view']
            # Move card to register 
            cardView.move(
                canvas,
                register.x - cardView.getPosition(canvas)[0], 
                register.y - cardView.getPosition(canvas)[1]
            )
            # Find card model in self.cards 
            cardModel = None
            for card in self.cards: 
                if card['view'] == cardView: 
                    cardModel = card['model']
                    break 

            # assingn card model to register model 
            if cardModel: 
                closestRegister['model'].card = cardModel
    
    def findClosestRegister(self, x, y):
        closestRegister = None 
        minDistance = float('inf')

        # go through register and calculate distance between card current pos and centre of each reg
        # pythag 

        for register in self.registers: 
            centre_x, centre_y = register['view'].getCentre()
            distance = ((x - centre_x) ** 2 + (y - centre_y) ** 2) ** 0.5
            if distance < minDistance: 
                minDistance = distance
                closestRegister = register
            
        return closestRegister

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
        
        self.processCommands(commands)

        # basially... we don't want robot existing (sorry mate) if it's multiplayer 
        if not self.isMultiplayer:
            botCommands = self.generateBotMoves() 
            self.processCommands(botCommands, isBot=True)
        
    
    # new method to process commands in an order because submitCards and Robot methods were not doing well... 
    def processCommands(self, commands, index=0, isBot=False):
        if index < len(commands):
            command = commands[index]
            direction = command['direction']
            steps = command['steps']

            # check current robot status 
            if self.isBotTurn:
                robotPos = self.botPos
                moveHistory = self.botMoveHistory
            else: 
                robotPos = self.playerPos
                moveHistory = self.moveHistory

            # Add to move history start point
            startPos = self.convertToRankAndFile(*robotPos)
            moveHistory.append({
                'turn': self.currentTurn,
                'player' : self.currentPlayerIdx + 1 if not isBot else 'Bot',
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
                onComplete=lambda: self.processCommands(commands,index+1))
        else: 
            if not isBot and self.isMultiplayer:
                self.currentPlayerIdx = (self.currentPlayerIdx+1) % self.totalPlayers
                # update end of turn label
                if self.currentPlayerIdx == 0:
                    self.currentTurn +=1 
                    self.playGameView.updateTurnLabel(self.currentTurn)

            elif not isBot and not self.isMultiplayer:
                botCommands = self.generateBotMoves()
                time.sleep(2)
                self.processCommands(botCommands, isBot=True)
            
            else: 
                # this is single player vs bot 
                self.currentTurn +=1  
                self.playGameView.updateTurnLabel(self.currentTurn)
                self.checkForCheckpoint()
                self.clearRegisterAndCards()

    #checking if the robot LANDS on the checkpoint 
    def checkForCheckpoint(self):
        if self.playerPos in self.checkpoints:
            # remove checkpoint first 
            self.checkpoints.remove(self.playerPos)

            # delete checkpoint 
            checkpointId = self.checkpointIds.pop(self.playerPos, None)
            if checkpointId:
                self.canvas.delete(checkpointId)

            self.checkpointsReached +=1  

            
            # update progress bar in the view! 
            self.playGameView.updateProgressBar(self.checkpointsReached)
            messagebox.showinfo('Checkpoint reached!', f'Checkpoint reached at {self.convertToRankAndFile(*self.playerPos)}') 

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


    def makeRegistersAndCards(self, canvas):
        # create empty registers 
        self.makeRegisters(canvas) 
        self.createActionCards(canvas) 

    # Robot logic stuff begins here 
    def createRobot(self, playerCount):
        # multiplayer tracking 
        self.multiplayerPos = [] 
        self.playerLabels = [] 
        self.playerIds = [] 

        colours = ['SpringGreen2', 'yellow', 'red2', 'purple']   

        # creating robots on grid, start with initial position
        exclude = self.checkpoints + list(self.obstacles)

        for i in range(playerCount):
            startPos= self.generateRandomSquares(1, exclude)[0]
            self.multiplayerPos.append(startPos)

            row,col = startPos 
            x1 = (col) * cell + cell/4
            y1 = (col) * cell + cell/4
            x2 = x1 + cell /2
            y2 = y1 + cell /2

            playerId = self.canvas.create_oval(x1, y1, x2, y2, fill=colours[i])
            self.playerIds.append(playerId)

            label = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f'P{i + 1}')
            self.playerLabels.append(label)

            exclude.append(startPos)

        # playerStart = self.generateRandomSquares(1, exclude)[0]
        # botStart = self.generateRandomSquares(1, exclude)[0]

        # # calculat corners of the cell 
        # self.playerPos = playerStart
        # x1 = (self.playerPos[1] * cell + cell/4)
        # y1 = (self.playerPos[0] * cell + cell/4)
        # x2 = x1 + cell /2
        # y2 = y1 + cell /2

        # # draw the robot 
        # self.playerId = self.canvas.create_oval(x1, y1, x2, y2, fill='light blue')
        # self.playerLabel = self.canvas.create_text(
        #     (x1+x2)/2, 
        #     (y1+y2)/2, 
        #     text='P'
        # )

        # # Bot robot 
        # self.botPos = botStart 
        # x1 = (self.botPos[1] * cell + cell/4)
        # y1 = (self.botPos[0] * cell + cell/4)
        # x2 = x1 + cell /2
        # y2 = y1 + cell /2

        # self.botId = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
        # self.botLabel = self.canvas.create_text(
        #     (x1+x2)/2, 
        #     (y1+y2)/2, 
        #     text='B'
        # )
    
    # this is more like 'animateRobotMoving' but I can't be bothered to refactor... 
    def moveRobot(self, direction, steps, stepCount=0, onComplete=None, isBot=False):

        # First need to check which bot is moving 
        if isBot:
            robotPos = self.botPos
            health = self.botHealth 
            history = self.botMoveHistory
            id = self.botId
            label = self.botLabel
        
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
        if (row, col) in self.obstacles:
            # Update health and move history for collision
            health -=1 
            history[-1]['end'] = self.convertToRankAndFile(row, col)
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
        else: 
            self.playerPos = (row, col)

        # Calculate new coordinates
        x1 = (col) * cell + cell / 4
        y1 = (row) * cell + cell / 4
        x2 = x1 + cell / 2
        y2 = y1 + cell / 2

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
                onComplete)

        else: 
            # update move history 
            history[-1]['end'] = self.convertToRankAndFile(row,col)
            self.playGameView.updateMoveHistory(history, isBot=isBot)

            # calling onComplete 
            if onComplete: 
                onComplete() 




