import tkinter as tk 
from tkinter import ttk 


class LeaderboardView: 
    def __init__(self, root, leaderboardController):
        self.root = root 
        self.leaderboardController = leaderboardController
        self.root.title('Leaderboard')

        # creating the leaderboard frame 
        leaderboardFrame = tk.Frame(self.root)
        leaderboardFrame.pack(fill=tk.BOTH)