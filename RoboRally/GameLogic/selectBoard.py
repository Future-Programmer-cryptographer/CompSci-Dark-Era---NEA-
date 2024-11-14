import tkinter as tk 
from tkinter import ttk 
from tkinter import PhotoImage
from tkinter import * 


# need a board selection screen with different difficulty 
# need to have three different boards - tkinter framing... 
# after they have selected the boards, we want them to select single player vs bot or multiplayer 

# set up a while loop... the when the user click son any option, we want to ask them if they want single player or multiplayer, just do it with one board..., then we want to have them play the game on that screen. 

class BoardDifficulty: 
    def __init__(self, root):
        self.root = root 
        self.root.title('Select game board')
        self.root.geometry('1000x1000')

        titleLabel = ttk.Label(self.root, text='Board difficulty')
        titleLabel.pack(pady=10)

        def stuffHappened():
            text.config(text='Button has been clicked')

        board1Btn = PhotoImage(file='Images/board1.png')
        imgLabel = ttk.Label(image=board1Btn)
        
        button = ttk.Button(root, image=board1Btn, command=stuffHappened, borderwidth=0).pack(pady=30)

        text = ttk.Label(root, text='').pack(pady=30)

        root.mainloop() 
    

