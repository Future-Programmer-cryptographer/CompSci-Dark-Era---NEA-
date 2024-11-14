import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox
from tkinter import * 

# Creating a drop down options menu 
class BoardDifficulty: 
    def __init__(self, root):
        self.root = root 
        self.root.title('Single Player vs Bot')
        self.root.geometry('500x500')

        titleLabel = ttk.Label(self.root, text='vs Bot')
        titleLabel.pack(pady=10)

        def getOption():
            label = ttk.Label(optionsFrame, text=clicked.get())
            label.grid(row=1, column=0, padx=20, pady=10)

        clicked = StringVar()
        clicked.set('Option Menu')

        options = OptionMenu(optionsFrame, clicked, 'Save Game', 'Quit', 'View Rules', 'Home')
        options.grid(row=0, column=0, padx=0, pady=0)

        optionButton = ttk.Button(optionsFrame, text='Go', command=getOption)
        optionButton.grid(row=2, column=0, padx=20, pady=10)

        root.mainloop() 
        optionsFrame = ttk.Frame(self.root)
        optionsFrame.pack(padx=0, pady=0)