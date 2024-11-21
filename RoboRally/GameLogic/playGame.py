from tkinter import * 
from PIL import Image, ImageTk 
import tkinter as tk 
from tkinter import ttk 


# need a board selection screen with different difficulty 
# need to have three different boards - tkinter framing... 
# after they have selected the boards, we want them to select single player vs bot or multiplayer 

# set up a while loop... the when the user click son any option, we want to ask them if they want single player or multiplayer, just do it with one board..., then we want to have them play the game on that screen. 

class PlayGame: 
    def __init__(self, root):
        self.root = root 
        self.root.title('Select game board')
        self.root.geometry('600x400')

        titleLabel = ttk.Label(self.root, text='Select one of the three boards for single/multiplayer game')
        titleLabel.pack(pady=10)

        # importing an image 
        boardImage = Image.open('Images/board1.png').resize((300,300))
        imageTk = ImageTk.PhotoImage(boardImage)

        # button widget 
        button = ttk.Button(root, 
                            text='Example board', 
                            image=imageTk, 
                            command=self.optionWindow)
        button.pack() 

        root.mainloop() 
    
    def optionWindow(self): 
        newWindow = Toplevel(self.root) 
        newWindow.title('Choose Game option')
        newWindow.geometry('400x400')

        singlePlayerBtn = ttk.Button(newWindow, 
                                     text='Single Player', 
                                     command=self.makeSingleplayerBoard)
        singlePlayerBtn.pack(pady=10)

        multiplayerBtn = ttk.Button(newWindow, 
                                     text='Multiplayer', 
                                     command=self.makeMultiplayerBoard)
        multiplayerBtn.pack(pady=10)


    def makeGrid(self):
        pass    
    # want to see rank-file style numbering 
    # size is 10 by 10 

    def placeObstacles(self):
        pass 
    # takes in parameters to place obstacles 

    def createCheckpoints(self):
        pass 
    # randomsize it 

    def createRegister(self, window): 
        self.window = window
        self.canvas = tk.Canvas(window, width=800, height=400, bg='light blue') 
        self.canvas.registers = [] 
        self.canvas.pack() 

        regWidth = 100 
        regHeight = 200 
        for i in range(3):
            Register(self.canvas, 
                     50+i*150, 50, 
                     regWidth, regHeight)
        
        self.cards = [
            DragAndDrop(self.canvas, 100,500, regWidth, regHeight)
        ]
        
    def startPoint(self):
        pass 

    def makeSingleplayerBoard(self):
        singlePlayerWindow = Toplevel(self.root)
        singlePlayerWindow.title('Single Player vs Bot')
        singlePlayerWindow.geometry('700x500')
        self.makeGrid() 
        self.createRegister(singlePlayerWindow) 

    def makeMultiplayerBoard(self): 
        pass 
        # multiplyer functionality 

    def checkWin(self): 
        pass 

    def moveHistory(self): 
        pass 
    


class Register: 
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas 
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.id = self.canvas.create_rectangle(x, y, x + width, y + height, fill='white')
        self.canvas.registers.append(self)

class DragAndDrop: 
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(x,y, x+width, y+height, fill='red') 
        self.canvas.tag_bind(self.id, '<ButtonPress-1>', self.startDrag)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.continueDrag)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.endDrag)
        self.register = None
    
    def startDrag(self, event):
        self.start_x = event.x 
        self.start_y = event.y  

    def continueDrag(self, event):
        dx = event.x - self.start_x 
        dy = event.y - self.start_y 
        self.canvas.move(self.id, dx, dy)
        self.start_x = event.x 
        self.start_y = event.y  

    def endDrag(self, event):
        closestRegister = self.findClosestRegister(event.x, event.y)
        if closestRegister: 
            self.snapToRegister(closestRegister)

    def findClosestRegister(self, x, y):
        closestRegister = None  
        closestDistance = float('inf')
        snapDistance = 100 

        for register in self.canvas.registers: 
            distance = ((x - (register.x + register.width / 2)) ** 2 + (y-(register.y + register.height/2)) ** 2 ) ** 0.5
            if distance < closestDistance and distance < snapDistance: 
                closestDistance = distance
                closestRegister = register 
        
        return closestRegister

    def snapToRegister(self, register):
        self.canvas.coords(self.id, register.x, register.y, register.x + register.width, register.y + register.height)
        self.register = register  
