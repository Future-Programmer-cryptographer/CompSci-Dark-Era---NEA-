from tkinter import * 
from tkinter import ttk 
from tkinter.ttk import *  
from View.rules import RulesWindow

from tkinter import messagebox
import os 

class MainMenuController: 
    def __init__(self, mainMenuView):
        self.mainMenuView = mainMenuView 
        self.playGameController = None
        self.leaderboardController = None
    
    # functions to hide and display the main menu frame - called mostly by the playGameController 
    def hideMain(self):
        self.mainMenuView.mainMenuFrame.pack_forget() 

    def displayMain(self):
        self.mainMenuView.mainMenuFrame.pack() 

    # main event handler for buttons clicks on the main menu 
    def handleClick(self,action):
        
        self.mainMenuView.mainMenuFrame.pack_forget() 

        # based on button clicked by user - most of the logic from here handled by playGameController 
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
        RulesWindow(self.mainMenuView.root)

    def ldSavedWindow(self):
        savedFiles = [f for f in os.listdir('.') if f.endswith('.md')]

        # inform user if no game files are found 
        if not savedFiles: 
            messagebox.showinfo('No Saved Games', "You haven't saved any games. Try again after saving games")
            return 
        
        # sort the saved files with most recent at the top 
        savedFiles.sort(key=os.path.getmtime, reverse=True)
        
        # Open a top level window for game selection 
        selectionWindow = Toplevel(self.mainMenuView.root)
        selectionWindow.title('Load Saved Game')
        selectionWindow.geometry('500x500')

        ttk.Label(selectionWindow, text='Select a saved game', font='fixedsys 20 bold').pack(pady=10)

        # create a button for each saved file 
        # display file name and date 
        for file in savedFiles: 
            with open(file, 'r') as f: 
                lines = f.readlines() 
                dateLine = next((line for line in lines if '**Date Played:**' in line), '').strip()

                # try and extract the date from the line 
                try:
                    date = dateLine.split('**Date Played:**', 1)[1].strip()
                except IndexError:
                    date = 'No games found :('
            
            # add a button for each file 
            # need to use lambda here as we need to pass each filename to the load game function 
            ttk.Button(selectionWindow, 
                       text=f'{file} (Played: {date})', 
                       command=lambda filename=file: self.__loadGameState(filename, selectionWindow)).pack(pady=5)
        
    def __loadGameState(self, filename, selectionWindow):
        try:
            with open(filename, 'r') as f:
                # Read the file content
                contents = f.readlines()
                # print(contents)

            # game state in the md file needs to parsed by playGameController 
            self.playGameController.parseGameState(contents)

            # close the window once game is loaded (easier to do with topLevel) 
            # inform user that game has been loaded 
            selectionWindow.destroy()
            messagebox.showinfo('Game Loading...', f'Loaded game from {filename}')

        except Exception as e:
            messagebox.showerror('ERrrr', f'Game cannot be loaded from {filename}: Please select another game')
            print(e)

                    
