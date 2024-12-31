import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox
import random 
import time 

from View.playGameView import PlayGameView
from cardsAndRegisters import model
from cardsAndRegisters import view

global cell
cell = 25 

global size 
size = 20 

class PlayGameController: 
    def __init__(self, root, canvas):
        self.mainMenuController = None 
        self.root = root 

        self.canvas = canvas 
        self.cards = [] 
        self.registers = [] 
        
        # coords display label 
        self.coordsLabel = ttk.Label(root, text='Coords: (0,0)')
        self.coordsLabel.pack() 

        # bind motion to show coords 
        self.canvas.bind('<Motion>', self.updateCoords)

        # animation speed 
        self.animationSpeed = 500

        # move history list - this needs to be displayed by THE VIEW 
        self.moveHistory = []
        self.botMoveHistory = [] # separate move histoyr for the bot? 

        # turn counter 
        self.currentTurn = 1 
        self.isBotTurn = False 

        # obstaclessss (pronouced obs-ta-cles - yes, like the greek heros)
        self.obstacles = set() 

        # robot health! 
        self.playerHealth=5 
        self.botHealth = 5 

        # checkpoint stuff 
        self.checkpoints = [] 
        self.checkpointsReached = 0 
        self.totalCheckpoints = 3 

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

    
    # method to place checkpoints 
    def placeCheckpoints(self, checkpointPos):

        for row, col in checkpointPos:
            pass 
            x1 = col*cell 
            y1 = row*cell 
            x2 = x1+cell 
            y2 = y1+cell 

            self.canvas.create_polygon(
                x1+cell/2, y1+cell/4, 
                x1+cell/4, y1+3*cell/4, 
                x1+3*cell/4, y1+3*cell/4, 
                fill='green', 
                outline='black'
            )
            self.checkpoints.append((row, col))
    
    # converting to rank and file to help with move histoyr 
    def convertToRankAndFile(self, row, col):
        rank = chr(64+col)
        file = row 
        return f'{rank}{file}'
    
    def updateCoords(self, event):
        x,y = event.x, event.y
        self.coordsLabel.config(text=f'Moues at :({x}, {y})')

    def initialiseView(self, root):
        self.playGameView.showSelectBoardWindow() 
    
    def onBoardSelect(self):
        self.playGameView.showOptionWindow() 
    
    def onSinglePlayerSelect(self):
        self.playGameView.showGameBoard(isSinglePlayer=True)
    
    def onMultiplayerSelect(self):
        self.playGameView.showGameBoard(isSinglePlayer=False)
    
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
        
        
    def createActionCards(self):
        directions = ['Forward', 'Backward', 'Left', 'Right', 'Forward', 'Backward']
        for i in range(5):
            direction = random.choice(directions)
            steps = random.randint(1,3) 

            # creating the model 
            cardModel = model.CardModel(direction, steps)

            # creating the card view 
            cardView = view.CardView(
                self.canvas, 
                x=100 + i * 150, 
                y=400, 
                width = 100, 
                height=50,
                text =f'{direction} {steps}'
            ) 

            # storing model and view in controller (as a dictionary)
            self.cards.append({'model':cardModel, 'view':cardView})

            # binding drag n drop stuff 
            self.canvas.tag_bind(cardView.cardId, '<ButtonPress-1>', lambda e, card=cardView: self.startDrag(e, card))
            self.canvas.tag_bind(cardView.cardId, '<B1-Motion>', lambda e, card=cardView: self.continueDrag(e, card))
            self.canvas.tag_bind(cardView.cardId, '<ButtonRelease-1>', lambda e, card=cardView: self.endDrag(e, card))

            # storing starting coords in case of a reset 
            cardView.start_x = 100+i*150
            cardView.start_y= 400 
    
    def resetCards(self):
        for cardPair in self.cards: 
            cardView = cardPair['view']
            current_x, current_y = cardView.getPosition() 
            dx = cardView.start_x - current_x
            dy = cardView.start_y - current_y
            cardView.move(dx,dy)
        
    def makeRegisters(self):
        for i in range(3):
            registerModel = model.RegisterModel() 
            registerView = view.RegisterView(
                self.canvas, 
                x= 50 + i * 150, 
                y=300, 
                width=100, 
                height=50
            )
            self.registers.append({'model':registerModel, 'view':registerView})


    # Logic for drag and drop here 

    def startDrag(self, event, cardView):
        self.start_x = event.x
        self.start_y = event.y 
    
    def continueDrag(self, event, cardView):
        dx = event.x - self.start_x 
        dy = event.y - self.start_y 
        cardView.move(dx, dy)
        self.start_x = event.x 
        self.start_y = event.y 
    
    def endDrag(self, event, cardView):
        # snap to closest register 
        closestRegister = self.findClosestRegister(event.x, event.y)
        if closestRegister: 
            register = closestRegister['view']
            # Move card to register 
            cardView.move(
                register.x - cardView.getPosition()[0], 
                register.y - cardView.getPosition()[1]
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
        
    
    # new method to process commands in an order because submitCards and Robot methods were not doing well... 
    def processCommands(self, commands, index=0):
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
            if not self.isBotTurn: 

                # end of turn logic 
                self.checkForCheckpoint()
                self.clearRegisterAndCards()

                # bot turn should start once the player turn finishes! 
                self.isBotTurn = True
                time.sleep(3)
                botCommands = self.generateBotMoves()
                self.processCommands(botCommands)

            else: 
                self.isBotTurn = False
                self.currentTurn +=1 
                self.playGameView.updateTurnLabel(self.currentTurn)

    #checking if the robot LANDS on the checkpoint 
    def checkForCheckpoint(self):
        if self.playerPos in self.checkpoints:
            # remove checkpoint first 
            self.checkpoints.remove(self.playerPos)
            self.checkpointsReached +=1  
            
            # update progress bar in the view! 
            self.playGameView.updateProgressBar(self.checkpointsReached)
            messagebox.showinfo('Checkpoint reached!', f'Checkpoint reached at {self.convertToRankAndFile(*self.playerPos)}') 

    def clearRegisterAndCards(self):
        for cardPair in self.cards: 
            cardView = cardPair['view']
            self.canvas.delete(cardView.cardId)
            self.canvas.delete(cardView.textId)
        self.cards =[]
        self.createActionCards() 

        for register in self.registers:
            register['model'].card = None 
        self.registers = [] 

        self.makeRegisters()         


    def makeRegistersAndCards(self):
        # create empty registers 
        self.makeRegisters() 
        self.createActionCards() 

    # Robot logic stuff begins here 
    def createRobot(self):
        # creating robot on grid, start with initial position
        self.playerPos = (5,5) 

        # calculat corners of the cell 
        x1 = (self.playerPos[1] * cell + cell/4)
        y1 = (self.playerPos[0] * cell + cell/4)
        x2 = x1 + cell /2
        y2 = y1 + cell /2

        # draw the robot 
        self.playerId = self.canvas.create_oval(x1, y1, x2, y2, fill='light blue')
        self.playerLabel = self.canvas.create_text(
            (x1+x2)/2, 
            (y1+y2)/2, 
            text='P'
        )

        # Bot robot 
        self.botPos = (8,8)
        x1 = (self.botPos[1] * cell + cell/4)
        y1 = (self.botPos[0] * cell + cell/4)
        x2 = x1 + cell /2
        y2 = y1 + cell /2

        self.botId = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
        self.botLabel = self.canvas.create_text(
            (x1+x2)/2, 
            (y1+y2)/2, 
            text='B'
        )
    
    # this is more like 'animateRobotMoving' but I can't be bothered to refactor... 
    def moveRobot(self, direction, steps, stepCount=0, onComplete=None):

        # First need to check which bot is moving 
        if self.isBotTurn:
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
            self.playGameView.updateHealthLabel(isBot=self.isBotTurn)

            messagebox.showinfo(
                "Collision!",
                f"{'Bot' if self.isBotTurn else 'Player'} hit an obstacle!"
            )
            if onComplete:
                onComplete()
            return

        # Update robot position
        if self.isBotTurn:
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
            self.playGameView.updateMoveHistory(history, isBot=self.isBotTurn)

            # calling onComplete 
            if onComplete: 
                onComplete() 




