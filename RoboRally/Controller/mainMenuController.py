from tkinter import * 
from tkinter import ttk 
from tkinter.ttk import *  
from Controller.leaderboard import displayLeaderboard
from View.rules import RulesWindow
from View.playGameView import PlayGameView

class MainMenuController: 
    def __init__(self, view):
        self.view = view 

    # so when the clicks, open a new window for each of these 
    def handleClick(self,action):
        
        self.view.mainMenuFrame.pack_forget() 

        if action == 'Tutorial':
            self.tutorialWindow() 
        elif action == 'PlayGame':
            self.playGame() 
        elif action == 'Leaderboard':
            self.leaderboardWindow() 
        elif action == 'LdSaved':
            self.ldSavedWindow()
        elif action == 'Rules':
            self.rulesWindow() 
    
    def tutorialWindow(self):
        tutorialWindow = Toplevel(self.view.root)
        tutorialWindow.title('Tutorial')
        tutorialWindow.geometry('400x300')
        label = ttk.Label(tutorialWindow,text='Welcome to the Tutorial')
        label.pack(pady=20)

    def playGame(self):
        PlayGameView(self.view.root)

    def leaderboardWindow(self):
        leaderboardWindow = Toplevel(self.view.root)
        leaderboardWindow.title('Leaderboard')
        leaderboardWindow.geometry('400x300')
        data = displayLeaderboard() 
        leaderboardLabel = ttk.Label(leaderboardWindow, text=data)
        leaderboardLabel.pack(pady=20)

    def ldSavedWindow(self):
        # include some logic for saving game and maybe a message like 'sure you wanna save this thing' 
        pass 
        print('saving game button works!')

    def rulesWindow(self):
        RulesWindow(self.view.root)
