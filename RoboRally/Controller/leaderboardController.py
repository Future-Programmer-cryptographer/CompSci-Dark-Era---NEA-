import tkinter as tk 
from tkinter import ttk 
from View.leaderboardView import LeaderboardView
from Controller.mainMenuController import MainMenuController
from View.mainMenuView import MainMenuView

class LeaderboardController: 
    def __init__(self, root, canvas):

        self.root = root 
        self.canvas = canvas 
        self.leaderboardView = LeaderboardView(root, self)
        self.mainMenuController = MainMenuController(MainMenuView)
    
    def initialiseLeaderboard(self, root):
        self.leaderboardView.showLeaderboard() 
    
    def backToMain(self):
        self.leaderboardView.leaderboardFrame.pack_forget() 
        self.mainMenuController.displayMain() 
    
    # merge sort algorithm for leaderboard 
    def mergeSort(self):
        pass 

    