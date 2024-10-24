from tkinter import * 
from tkinter import ttk 
from tkinter.ttk import * 

class MainMenuController: 
    def __init__(self, model, view):
        self.model = model 
        self.view = view 

    # so wehn user clicks, open a new window for each of these 
    def handleClick(self,action):
        if action == 'Tutorial':
            self.tutorialWindow() 
        elif action == 'vsBot':
            self.vsBotWindow() 
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

    def vsBotWindow(self):
       vsBotWindow = Toplevel(self.view.root)
       vsBotWindow.title('Single Player vs Bot')
       vsBotWindow.geometry('400x300')
       label = ttk.Label(vsBotWindow, text='Single Player vs Bot') 
       label.pack(pady=20)

    def multiplayerWindow(self):
        multiplayerWindow = Toplevel(self.view.root)
        multiplayerWindow.title('Multiplayer Mode')
        multiplayerWindow.geometry('400x300')
        label=ttk.Label(multiplayerWindow, text='Welcome to multiplayer game')
        label.pack(pad=20)

    def leaderboardWindow(self):
        leaderboardWindow = Toplevel(self.view.root)
        leaderboardWindow.title('Leaderboard')
        leaderboardWindow.geometry('400x300')
        # insert some leaderboard logic including sorting of leaderboard, read from an external file 

    def ldSavedWindow(self):
        # include some logic for saving game and maybe a message like 'sure you wanna save this thing' 
        pass 
        print('saving game button works!')

    def rulesWindow(self):
        rulesWindow = Toplevel(self.view.root)
        rulesWindow.title('Robo Rally Rules')
        rulesWindow.geometry('400x300')
        label1 = ttk.Label(rulesWindow, text='Rules here...')
        label1.pack(pady=20)