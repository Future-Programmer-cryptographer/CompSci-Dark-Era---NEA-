import tkinter as tk 
from tkinter import ttk 


class LeaderboardView: 
    def __init__(self, root, leaderboardController):
        self.root = root 
        self.leaderboardController = leaderboardController

        # creating the leaderboard frame - idk why I need self in this this... but it works and I'm not gonna question it... - problems with garbage collection or something... 
        self.leaderboardFrame = tk.Frame(self.root)
        
        # creating the buttons and options 
        label = ttk.Label(self.leaderboardFrame, text='Leaderboard', font=('Arial',20))
        label.pack(pady=5)

        # make a back button 
    
    def showLeaderboard(self):
        self.root.title('Leaderboard')
        self.leaderboardFrame.pack(fill=tk.BOTH)