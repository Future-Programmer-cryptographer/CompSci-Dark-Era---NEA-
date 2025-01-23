import tkinter as tk 
from tkinter import ttk 


class RulesWindow: 
    def __init__(self, root): 
        self.root = root 
        self.root.title('Robo Rally Rules')

        # creating rules frame 
        self.rulesFrame = tk.Frame(self.root)
        self.rulesFrame.pack(fill=tk.BOTH)

        titleLabel = ttk.Label(self.rulesFrame, text='Robo Rally Rules', font=('verdana', 15, 'bold'))
        titleLabel.pack(pady=10)

        mainLabel = ttk.Label(self.rulesFrame, text='Objective: Program robots to reach the checkpoints before your oppponents', font='verdana')
        mainLabel.pack(pady=5)

        rulesFrame = ttk.Frame(self.rulesFrame)
        rulesFrame.pack(pady=10)

        section1 = ttk.Label(rulesFrame, text='Rules about Instruction cards and register', font=('verdana', 10, 'bold'))
        text1 = ttk.Label(rulesFrame, text='-Each player will receive 5 instruction cards and will have to select 3 to play', wraplength=300, justify='left')

        section2 = ttk.Label(rulesFrame, text='How board elements work', font=('verdana', 10, 'bold'))
        text2 = ttk.Label(rulesFrame, text='-In this version of Robo Rally you will come across two board elememts: gears and pits \n -Pits are black, gears have a G on them', wraplength=300, justify='left')

        section3 = ttk.Label(rulesFrame, text='Health, scoring and winning criteria', font=('verdana', 10, 'bold'))
        text3 = ttk.Label(rulesFrame, text='-Every player starts of with 10 life \n -You lose a life if you fall into a pit or get hit by a laser', wraplength=300, justify='left')
        
        section1.grid(row=0, column=0, padx=20, pady=10)
        text1.grid(row=1, column=0, padx=20, pady=10)
        
        section2.grid(row=0, column=1, padx=20, pady=10)
        text2.grid(row=1, column=1, padx=20, pady=10)

        section3.grid(row=0, column=2, padx=20, pady=10)
        text3.grid(row=1, column=2, padx=20, pady=10)


        