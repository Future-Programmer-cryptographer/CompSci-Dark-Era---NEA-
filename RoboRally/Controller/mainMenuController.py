from tkinter import * 
from tkinter import ttk 
from tkinter.ttk import *  
from Controller.leaderboard import displayLeaderboard
from View.rules import RulesWindow

class MainMenuController: 
    def __init__(self, mainMenuView):
        self.mainMenuView = mainMenuView 
        self.playGameController = None

    # so when the clicks, open a new window for each of these 
    def handleClick(self,action):
        
        self.mainMenuView.mainMenuFrame.pack_forget() 

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
        tutorialWindow = Toplevel(self.mainMenuView.root)
        tutorialWindow.title('Tutorial')
        tutorialWindow.geometry('400x300')
        label = ttk.Label(tutorialWindow,text='Welcome to the Tutorial')
        label.pack(pady=20)

    def playGame(self):
        self.playGameController.initialiseView(self.mainMenuView.root) 

    def leaderboardWindow(self):
        leaderboardWindow = Toplevel(self.mainMenuView.root)
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
        RulesWindow(self.mainMenuView.root)
