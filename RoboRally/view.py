import tkinter as tk 
from tkinter import ttk 


class MainMenuView: 
    def __init__(self, controller):
        self.controller = controller  
        self.root = tk.Tk() 
        self.root.title('Main Menu')
        self.root.geometry('400x400')
        self.root.minsize(400,400)

        self.label = ttk.Label(self.root, text='This is the Main Menu')
        self.label.pack(pady=20)
        
        self.buttons = []
        
        self.tutorialBtn = ttk.Button(self.root, 
                                      text='Tutorial', 
                                      command=lambda: self.controller.handleClick('Tutorial'))
        self.vsBotBtn = ttk.Button(self.root, 
                                text='Single Player vs Bot', 
                                command=lambda: self.controller.handleClick('vsBot'))
        self.multiplayerBtn = ttk.Button(self.root, 
                                      text='Multiplayer', 
                                      command=lambda: self.controller.handleClick('Multiplayer'))
        self.LeaderboardBtn = ttk.Button(self.root, 
                                        text='View Leaderboard', 
                                        command=lambda: self.controller.handleClick('Leaderboard'))
        self.LdSavedBtn = ttk.Button(self.root, 
                                  text='Load Saved', 
                                  command=lambda: self.controller.handleClick('LdSaved'))
        self.rulesBtn= ttk.Button(self.root, 
                                text='View Robo Rally Rules', 
                                command=lambda: self.controller.handleClick('Rules'))

        self.buttons=[self.tutorialBtn, self.vsBotBtn, self.multiplayerBtn, self.LeaderboardBtn, self.LdSavedBtn, self.rulesBtn]

        for button in self.buttons: 
            button.pack(pady=10)
        
        
    def mainloop(self):
        self.root.mainloop() 
 
