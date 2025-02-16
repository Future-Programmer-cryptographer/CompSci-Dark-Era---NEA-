import tkinter as tk 
from tkinter import ttk 
from View.leaderboardView import LeaderboardView
from Controller.mainMenuController import MainMenuController
from View.mainMenuView import MainMenuView
import os 
from datetime import datetime 
from tkinter import messagebox


from Controller.helperFunctions import getMdValue

class LeaderboardController: 
    def __init__(self, root, canvas):

        self.root = root 
        self.canvas = canvas 
        self.leaderboardView = LeaderboardView(root, self)
        self.mainMenuController = MainMenuController(MainMenuView)
    
        self.leaderboardData = []

    
    def initialiseLeaderboard(self, root):
        self.loadLeaderboardData() 
        self.leaderboardView.showLeaderboard(self.leaderboardData) 
    
    def loadLeaderboardData(self):
        savedFiles = [f for f in os.listdir('.') if f.endswith('.md')]

        for file in savedFiles: 
            try: 
                with open(file, 'r') as f: 
                    contents = f.readlines() 
                
                date= getMdValue(contents, 'Date Played')
                difficulty = getMdValue(contents, 'Difficulty')
                checkpoints = int(getMdValue(contents, 'Player Checkpoints Reached'))

                # Parsing for time - need to debug 
                time = getMdValue(contents, 'Time Taken')
                time = float(time) 

                self.leaderboardData.append({
                    'date' : datetime.strptime(date, '%d-%m-%Y %H:%M'), 
                    'difficulty' : difficulty, 
                    'checkpoints' : checkpoints, 
                    'filename' : file, 
                    'time' : time
                })
            
            except (ValueError, KeyError) as e: 
                messagebox.showerror('ERrrr', f'Error from {file}: {str(e)}')
    
    def backToMain(self):
        self.leaderboardView.leaderboardFrame.pack_forget() 
        self.mainMenuController.displayMain() 
    

    # Merge Sort algorithm to sort leaderboard 
    def mergeSort(self, data, key):

        # in case of list size = 1, already sorted 
        if len(data) <=1: 
            return data 
        
        # finding midpoint of list 
        mid = len(data) // 2

        # split and sort both halves (implemented recusively)
        left = self.mergeSort(data[:mid], key)
        right = self.mergeSort(data[mid:], key)

        # merge sorted halves 
        return self.merge(left, right, key)

    def merge(self, left, right, key):

        # final merge sorted list 
        sorted = [] 

        # compare elements from both halves and merge in order based on key (date/checkpoints/difficulty/etc.)
        while left and right: 
            if self.compare(left[0], right[0], key):
                sorted.append(left.pop(0))
            else: 
                sorted.append(right.pop(0))
        
        # if one list still has remaining elements, add them at then end 
        sorted.extend(left or right)

        return sorted 

    # method to compare items based on whether they are sorted by checkpoints/date/difficulty or time 
    def compare(self, i1, i2, key): 
        if key == 'checkpoints':
            # descending order - highest checkpoints at the top 
            return i1['checkpoints'] > i2['checkpoints']
        
        elif key == 'date':
            # descending order - most recently played games at the top 
            return i1['date'] > i2['date']
        
        elif key == 'difficulty':
            order = {'HARD':3, 'MEDIUM' :2, 'EASY':1, 'CUSTOM':0}
            # descending order - hardest games first (custom doesn't matter)
            return order[i1['difficulty']] > order[i2['difficulty']] 
        
        elif key == 'time':
            # ascending order - fastest times at the top 
            return i1['time'] < i2['time']

    # method to merge sort and update leaderboard after sorting in the view
    def sortLeaderboard(self, key):
        self.leaderboardData = self.mergeSort(self.leaderboardData, key)
        self.leaderboardView.updateLeaderboard(self.leaderboardData)



    