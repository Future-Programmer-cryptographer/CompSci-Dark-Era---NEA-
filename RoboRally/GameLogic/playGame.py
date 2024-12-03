from tkinter import * 
from PIL import Image, ImageTk 
import tkinter as tk 
from tkinter import ttk 


# need a board selection screen with different difficulty 
# need to have three different boards - tkinter framing... 
# after they have selected the boards, we want them to select single player vs bot or multiplayer 

# set up a while loop... the when the user clicks on any option, we want to ask them if they want single player or multiplayer, just do it with one board..., then we want to have them play the game on that screen. 

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


    def makeGrid(self, window):
        size = 5
        cell = 10 
        # want the grid on the same canvas? 
        gridCanvas = tk.Canvas(window, width=cell*(size+1), height=cell*(size+1))
        gridCanvas.pack() 

        # drawing the actual grid 
        for i in range(size):
            for j in range(size): 
                x1 = (j+1) * cell 
                y1 = (i+1) * cell
                x2 = x1 + cell 
                y2 = y1 + cell

                gridCanvas.create_rectangle(x1,y1,x2,y2, fill='pink', outline='black')

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
        # main register canvas 
        self.canvas = tk.Canvas(window, width=1000, height=1000, bg='light blue') 
        self.canvas.registers = [] 
        self.canvas.pack() 

        regWidth = 100 
        regHeight = 200 

        for i in range(3):
            Register(self.canvas, 
                     50+i*150, 50, 
                     regWidth, regHeight)
            
        # all possible cards here 
        self.cards = [
            DragAndDrop(self.canvas, 'Images/image1.png', 100,400, regWidth, regHeight),
            DragAndDrop(self.canvas, 'Images/image1.png', 350,400, regWidth, regHeight),
            DragAndDrop(self.canvas, 'Images/image3.png', 600,400, regWidth, regHeight)
        ]
        
    def startPoint(self):
        pass 

    def makeSingleplayerBoard(self):
        singlePlayerWindow = Toplevel(self.root)
        singlePlayerWindow.title('Single Player vs Bot')
        singlePlayerWindow.geometry('1000x1000')
        self.makeGrid(singlePlayerWindow) 
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


# this is for dragging and dropping cards into register slots 
class DragAndDrop: 
    def __init__(self, canvas, imagePath, x, y, width, height):
        self.canvas = canvas

        # added these two for later 
        self.width = width 
        self.height = height 

        self.imagePath = imagePath
        self.image = Image.open(imagePath)
        self.imagePath= self.image.resize((width, height))
        self.photo = ImageTk.PhotoImage(self.image) # this was self.image before, which was not resized 

        # use create_image to render images (not rectangle)
        # create image only needs x and y 
        self.imageId = self.canvas.create_rectangle(x,y, x+width, y+height, fill='red')  

        self.canvas.tag_bind(self.imageId, '<ButtonPress-1>', self.startDrag)
        self.canvas.tag_bind(self.imageId, '<B1-Motion>', self.continueDrag)
        self.canvas.tag_bind(self.imageId, '<ButtonRelease-1>', self.endDrag)
        self.register = None
    
    def startDrag(self, event):
        self.start_x = event.x 
        self.start_y = event.y  

    def continueDrag(self, event):
        dx = event.x - self.start_x 
        dy = event.y - self.start_y 
        self.canvas.move(self.imageId, dx, dy)
        self.start_x = event.x 
        self.start_y = event.y  

    def endDrag(self, event):
        # iterate over all registers and calculate distance between card current pos and the centre of each reg 
        closestRegister = self.findClosestRegister(event.x, event.y)
        if closestRegister: 
            self.snapToRegister(closestRegister)

    def findClosestRegister(self, x, y):
        # pythag it 
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
        self.canvas.coords(self.imageId, register.x, register.y, register.x + register.width, register.y + register.height)
        self.register = register  

