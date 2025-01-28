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
                checkpoints = int(getMdValue(contents, 'Checkpoints Reached'))

                self.leaderboardData.append({
                    'date' : datetime.strptime(date, '%d-%m-%Y %H:%M'), 
                    'difficulty' : difficulty, 
                    'checkpoints' : checkpoints, 
                    'filename' : file
                })
            
            except (ValueError, KeyError) as e: 
                messagebox.showerror('Error', f'Failed to load {file}: {str(e)}')
    
    def backToMain(self):
        self.leaderboardView.leaderboardFrame.pack_forget() 
        self.mainMenuController.displayMain() 
    
    # merge sort algorithm for leaderboard - comment this pls, I know geeksforgeeks was useful but for the love of god please comment this section!! 
    def mergeSort(self, data, key):
        if len(data) <=1: 
            return data 
        
        mid = len(data) // 2
        left = self.mergeSort(data[:mid], key)
        right = self.mergeSort(data[mid:], key)

        return self.merge(left, right, key)

    def merge(self, left, right, key):
        sorted = [] 
        while left and right: 
            if self.compare(left[0], right[0], key):
                sorted.append(left.pop(0))
            else: 
                sorted.append(right.pop(0))
        
        sorted.extend(left or right)
        return sorted 

    def compare(self, i1, i2, key): 
        if key == 'checkpoints':
            return i1['checkpoints'] > i2['checkpoints']
        elif key == 'date':
            return i1['date'] > i2['date']
        elif key == 'difficulty':
            order = {'HARD':3, 'MEDIUM' :2, 'EASY':1}
            return order[i1['difficulty']] > order[i2['difficulty']] 

    def sortLeaderboard(self, key):
        self.leaderboardData = self.mergeSort(self.leaderboardData, key)
        self.leaderboardView.updateLeaderboard(self.leaderboardData)



    