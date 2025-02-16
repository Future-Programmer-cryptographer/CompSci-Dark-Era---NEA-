import tkinter as tk 
from tkinter import ttk 


class MainMenuView: 

    # View class for creating and displaying the main menu  

    def __init__(self, root, controller):

        # initialise the main menu 
        # the controller passed in here is the 'MainMenuController' 
        
        self.controller = controller  
        self.root = root 
        self.root.title('Main Menu')
        
        # setting starting width and height paramaters here - but window is resizable 
        width = 1000 
        height = 750 

        self.root.geometry(f'{width}x{height}')
        self.root.minsize(width,height)

        # styling the buttons 
        style = ttk.Style() 
        style.configure('play.TButton', font=('fixedsys 20 bold'), foreground='red3')

        # creating the main menu frame that will contain the buttons and widgets 
        self.mainMenuFrame = tk.Frame(self.root)
        self.mainMenuFrame.pack(fill=tk.BOTH)
        
        label = ttk.Label(self.mainMenuFrame, text='Welcome to Robo Rally Pythonised!', font=('fixedsys 20 bold'))
        label2 = ttk.Label(self.mainMenuFrame, text='This is the Main Menu. Please select one of the options below', font=('Verdana bold', 15))
        label.pack(pady=20)
        label2.pack(pady=5)
        
        # creating an empty buttons list to then pack all the buttons on the main menu frame 
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

        for button in self.buttons: 
            button.pack(ipadx=20, ipady=10, pady=10)
        
    # start the main event here 
    def mainloop(self):
        self.root.mainloop() 
 
