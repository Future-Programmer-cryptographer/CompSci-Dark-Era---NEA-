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

        # styling buttons 
        style = ttk.Style() 

        # creating a main menu frame 
        self.mainMenuFrame = tk.Frame(self.root)
        self.mainMenuFrame.pack(fill=tk.BOTH)
        
        label = ttk.Label(self.mainMenuFrame, text='Welcome to Robo Rally Pythonised!', font=('fixedsys 20 bold'))
        label2 = ttk.Label(self.mainMenuFrame, text='This is the Main Menu. Please select one of the options below', font=('Verdana bold', 15))
        label.pack(pady=20)
        label2.pack(pady=5)
        
        self.buttons = []
        
        self.playGameBtn = ttk.Button(self.mainMenuFrame, 
                                text='Play Game',
                                style='play.TButton', 
                                command=lambda: self.controller.handleClick('PlayGame'))
        
        self.LeaderboardBtn = ttk.Button(self.mainMenuFrame, 
                                        text='View Leaderboard', 
                                        style='play.TButton', 
                                        command=lambda: self.controller.handleClick('Leaderboard'))
        
        self.LdSavedBtn = ttk.Button(self.mainMenuFrame, 
                                  text='Load A Saved Game',
                                  style='play.TButton', 
                                  command=lambda: self.controller.handleClick('LdSaved'))
        
        self.rulesBtn= ttk.Button(self.mainMenuFrame, 
                                text='View Robo Rally Rules', 
                                style='play.TButton', 
                                command=lambda: self.controller.handleClick('Rules'))

        self.buttons=[self.playGameBtn, self.LeaderboardBtn, self.LdSavedBtn, self.rulesBtn]

        style.configure('play.TButton', font=('fixedsys 20 bold'), foreground='red3')

        for button in self.buttons: 
            button.pack(ipadx=20, ipady=10, pady=10)
        
        
    def mainloop(self):
        self.root.mainloop() 
 
