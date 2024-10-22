import tkinter as tk 
from tkinter import ttk 


class MainMenuView: 
    def __init__(self, controller):
        self.controller = controller  
        self.root = tk.Tk() 
        self.root.title('Main Menu')
        self.root.geometry('300x300')
        self.root.minsize(300,300)

        self.label = ttk.Label(self.root, text='This is the Main Menu')
        self.label.pack(pady=20)
        
        self.buttons = []
        self.tutorialBtn = ttk.Button(self.root, 
                                      text='Tutorial', 
                                      command=lambda: self.controller.handleClick('Tutorial'))
        self.vsBot = ttk.Button(self.root, 
                                text='SP vs Bot', 
                                command=lambda: self.controller.handleClick('SpVBOT'))
        self.LeaderboardBtn = ttk.Button(self.root, 
                                        text='Leaderboard', 
                                        command=lambda: self.controller.handleClick('Leaderboard'))
        
        self.buttons=[self.tutorialBtn, self.vsBot, self.LeaderboardBtn]

        for button in self.buttons: 
            button.pack(pady=10)
        
        
    def mainloop(self):
        self.root.mainloop() 
 
