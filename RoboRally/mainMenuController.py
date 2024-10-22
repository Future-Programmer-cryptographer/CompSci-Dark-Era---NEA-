import tkinter 
from tkinter import ttk 
import tkinter.messagebox

class MainMenuController: 
    def __init__(self, model, view):
        self.model = model 
        self.view = view 

    def handleClick(self,action):
        if action == 'Tutorial':
            self.Tutorial() 
        elif action == 'SpVBOT':
            self.spVsBot() 
        elif action == 'Leaderboard': 
            self.viewLeaderboard() 
    
    def Tutorial(self):
        print('tutorial button works!')

    def spVsBot(self):
        print('SpVS BOT works!')

    def viewLeaderboard(self):
        print('leaderboard works!')