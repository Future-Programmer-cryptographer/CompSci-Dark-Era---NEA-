import tkinter as tk 
from tkinter import ttk 
from View.leaderboardView import LeaderboardView

class LeaderboardController: 
    def __init__(self, root, canvas):

        self.root = root 
        self.canvas = canvas 
        self.leaderboardView = LeaderboardView(root, self)
    
    def initialiseLeaderboard(self, root):
        self.leaderboardView.showLeaderboard() 
    