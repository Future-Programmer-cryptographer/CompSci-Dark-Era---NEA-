from tkinter import tk 
from tkinter import ttk 

def makeGrid(self, window):
        # want to see rank-file style numbering 
        # size is 10 by 10 to start with
        # ask user to input a grid later

        size = 10
        cell = 20 
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