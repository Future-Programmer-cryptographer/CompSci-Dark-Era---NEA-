from tkinter import * 
from tkinter import ttk 
from tkinter.ttk import *  
from Controller.leaderboard import displayLeaderboard
from View.rules import RulesWindow

from tkinter import messagebox
import os 

class MainMenuController: 
    def __init__(self, mainMenuView):
        self.mainMenuView = mainMenuView 
        self.playGameController = None
        self.leaderboardController = None
    
    def hideMain(self):
        self.mainMenuView.mainMenuFrame.pack_forget() 

    # so when the clicks, open a new window for each of these 
    def handleClick(self,action):
        
        self.mainMenuView.mainMenuFrame.pack_forget() 

        if action == 'PlayGame':
            self.playGame() 
        elif action == 'Leaderboard':
            self.leaderboardWindow() 
        elif action == 'LdSaved':
            self.ldSavedWindow()
            self.mainMenuView.mainMenuFrame.pack() 
        elif action == 'Rules':
            self.rulesWindow() 
    
    def playGame(self):
        self.playGameController.initialiseView(self.mainMenuView.root)

    def leaderboardWindow(self):
        self.leaderboardController.initialiseLeaderboard(self.mainMenuView.root)
    
    def rulesWindow(self):
        # I have no idea why I created another class for this... like it's pretty pointless, a frame would do but I can't be asked to refactor... 
        RulesWindow(self.mainMenuView.root)
    
    def displayMain(self):
        self.mainMenuView.mainMenuFrame.pack() 

    def ldSavedWindow(self):
        savedFiles = [f for f in os.listdir('.') if f.endswith('.md')]

        if not savedFiles: 
            messagebox.showinfo('No Saved Games')
            return 
        
        savedFiles.sort(key=os.path.getmtime, reverse=True)
        
        # Open a top level window 
        selectionWindow = Toplevel(self.mainMenuView.root)
        selectionWindow.title('Load Saved Game')
        selectionWindow.geometry('500x500')

        ttk.Label(selectionWindow, text='Select a saved game').pack(pady=10)

        for file in savedFiles: 
            with open(file, 'r') as f: 
                lines = f.readlines() 
                # dateLine 
                dateLine = next((line for line in lines if '**Date Played:**' in line), '').strip()
                try:
                    date = dateLine.split('**Date Played:**', 1)[1].strip()
                except IndexError:
                    date = 'No games found :('
            
            # add a button for each file so that user can click that 
            ttk.Button(selectionWindow, 
                       text=f'{file} (Played: {date})', 
                       command=lambda filename=file: self.__loadGameState(filename, selectionWindow)).pack(pady=5)
        
    def __loadGameState(self, filename, selectionWindow):
        try:
            with open(filename, 'r') as f:
                # Read the file content
                contents = f.readlines()
                # print(contents)

            # File stuff needs read by the controller 
            self.playGameController.parseGameState(contents)

            # close this window... 
            selectionWindow.destroy()

            # Tell user (messagebox is useful so why not...)
            messagebox.showinfo('Game Loading...', f'Loaded game from {filename}')

        except Exception as e:
            print(f'{e}')

                    
