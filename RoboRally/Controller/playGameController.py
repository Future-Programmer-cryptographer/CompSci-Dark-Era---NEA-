import tkinter as tk 
from tkinter import ttk 
import random 

from View.playGameView import PlayGameView
from Controller.cardController import CardController
from Model.cardModel import CardModel
from View.cardView import CardView 
from View.registerView import RegisterView


class PlayGameController: 
    def __init__(self, root, playGameview, canvas):
        self.mainMenuController = None 
        self.root = root 
        self.playGameView =  playGameview

        self.canvas = canvas 
        self.cards = [] 
        self.registers = [] 

        # initialise the view 
        # self.playGameView = PlayGameView(root, self)
    
    def initialiseView(self, root):
        PlayGameView(root, self)
    
    def onBoardSelect(self):
        self.playGameView.showOptionWindow() 
    
    def onSinglePlayerSelect(self):
        self.playGameView.showGameBoard(isSinglePlayer=True)
    
    def onMultiplayerSelect(self):
        self.playGameView.showGameBoard(isSinglePlayer=False)
    
    def backToOptions(self):
        self.playGameView.showOptionWindow() 
    
    def makeGrid(self, parentFrame):
        size = 10 
        cell = 20 

        gridCanvas = tk.Canvas(parentFrame, 
                               width=cell*(size+1), 
                               height=cell*(size+1))
        gridCanvas.pack() 

        # draw the actual grid 
        for i in range(size):
            for j in range(size):
                x1 = (j+1) * cell 
                y1 = (i+1)  * cell 
                x2 = x1 + cell 
                y2 = y1 + cell 

                gridCanvas.create_rectangle(x1, y1, x2, y2, fill='pink', outline='black')

        # letters 
        for col in range(size):
            x = (col+1) * cell + cell / 2 
            y = cell /2  
            file = chr(65+col) # convert 0-9 to letters 
            gridCanvas.create_text(x,y,text=file) 
        
        # number labels 
        for row in range(size):
            x = cell / 2 
            y = (row+1) * cell + cell / 2 
            rank = str(row+1)
            gridCanvas.create_text(x,y,text=rank)
        
        return gridCanvas
        
    def createActionCards(self):
        actions = ['Forward', 'Backward', 'Left', 'Right']
        for i in range(3):
            action = random.choice(actions)
            number = random.randint(1,3) 

            # create card model, view, controller 
            cardModel = CardModel(action, number)
            cardView = CardView(
                self.canvas, 
                x=100 + i * 150, 
                y=400, 
                width = 100, 
                height=50, 
                action=action, 
                number=number
            )
            cardController = CardController(self.canvas, cardModel, cardView)
            self.cards.append(cardController)

        
    def makeRegisters(self):
        for i in range(3):
            registerView = RegisterView(
                self.canvas, 
                x= 50 + i * 150, 
                y=300, 
                width=100, 
                height=50
            )
            self.registers.append(registerView)

    
    def submitCards(self):
        for register in self.registers:
            if register.card:
                card = register.card
                print(f"Register contains: Action = {card.action}, Number = {card.number}")
            else:
                print("Register is empty.")

    def makeRegistersAndCards(self, frame):
        # create empty registers 
        self.makeRegisters() 
        self.createActionCards() 

        # submit button 
        submitBtn = ttk.Button(
            frame, 
            text='submit', 
            command=self.submitCards
        )
        submitBtn.pack(pady=10)