from tkinter import * 
from tkinter import ttk 
from tkinter.ttk import *  
from GameLogic.leaderboard import displayLeaderboard
from GameLogic.rules import RulesWindow
from GameLogic.playGame import PlayGame 

class MainMenuController: 
    def __init__(self, model, view):
        self.model = model 
        self.view = view 

    # so when the clicks, open a new window for each of these 
    def handleClick(self,action):
        if action == 'Tutorial':
            self.tutorialWindow() 
        elif action == 'PlayGame':
            self.playGame() 
        elif action == 'Multiplayer': 
            self.multiplayerWindow() 
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
    #    vsBotWindow = Toplevel(self.view.root)
    #    vsBotWindow.title('Single Player vs Bot')
    #    vsBotWindow.geometry('400x300')
    #    label = ttk.Label(vsBotWindow, text='Single Player vs Bot') 
    #    label.pack(pady=20)
        selectBoard = Toplevel(self.view.root)
        PlayGame(selectBoard)

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
        rulesWindow = Toplevel(self.view.root)
        RulesWindow(rulesWindow)
