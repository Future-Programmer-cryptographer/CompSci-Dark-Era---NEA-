import tkinter as tk 
from tkinter import ttk 


class MainMenuView: 
    def __init__(self, root, controller):
        self.controller = controller  
        self.root = root 
        self.root.title('Main Menu')
        
        # setting width and height paramaters here 
        width = 1000 
        height = 750 

        self.root.geometry(f'{width}x{height}')
        self.root.minsize(width,height)


        # creating a main menu frame 
        self.mainMenuFrame = tk.Frame(self.root)
        self.mainMenuFrame.pack(fill=tk.BOTH)
        
        self.label = ttk.Label(self.mainMenuFrame, text='This is the Main Menu')
        self.label.pack(pady=20)
        
        self.buttons = []
        
        self.tutorialBtn = ttk.Button(self.mainMenuFrame, 
                                      text='Tutorial', 
                                      command=lambda: self.controller.handleClick('Tutorial'))
        
        self.playGameBtn = ttk.Button(self.mainMenuFrame, 
                                text='Play Game', 
                                command=lambda: self.controller.handleClick('PlayGame'))
        
        self.LeaderboardBtn = ttk.Button(self.mainMenuFrame, 
                                        text='View Leaderboard', 
                                        command=lambda: self.controller.handleClick('Leaderboard'))
        
        self.LdSavedBtn = ttk.Button(self.mainMenuFrame, 
                                  text='Load Saved', 
                                  command=lambda: self.controller.handleClick('LdSaved'))
        
        self.rulesBtn= ttk.Button(self.mainMenuFrame, 
                                text='View Robo Rally Rules', 
                                command=lambda: self.controller.handleClick('Rules'))

        self.buttons=[self.tutorialBtn, self.playGameBtn, self.LeaderboardBtn, self.LdSavedBtn, self.rulesBtn]

        for button in self.buttons: 
            button.pack(pady=10)
        
        
    def mainloop(self):
        self.root.mainloop() 
 
