import tkinter as tk 
from tkinter import ttk 
from datetime import datetime
import os 


class LeaderboardView: 
    def __init__(self, root, leaderboardController):
        self.root = root 
        self.leaderboardController = leaderboardController

        # creating the leaderboard frame - idk why I need self in this this... but it works and I'm not gonna question it... - problems with garbage collection or something... 
        self.leaderboardFrame = tk.Frame(self.root)
        
        # creating the buttons and options 
        label = ttk.Label(self.leaderboardFrame, text='Leaderboard', font=('fixedsys 20 bold'))
        label.pack(pady=5)

        # Sorting optoins 
        self.sortOptionsFrame = tk.Frame(self.leaderboardFrame)
        self.sortOptionsFrame.pack(pady=5)

        sortByDateBtn = ttk.Button(
            self.sortOptionsFrame, 
            text='Sort by Date', 
            command = lambda: self.leaderboardController.sortLeaderboard('date')
        )

        sortByDiffBtn = ttk.Button(
            self.sortOptionsFrame, 
            text='Sort by Difficulty', 
            command = lambda: self.leaderboardController.sortLeaderboard('difficulty')
        )

        sortByScoreBtn = ttk.Button(
            self.sortOptionsFrame, 
            text='Sort by Checkpoints Reached', 
            command = lambda: self.leaderboardController.sortLeaderboard('checkpoints')
        )

        sortByTimeBtn = ttk.Button(
            self.sortOptionsFrame, 
            text='Sort by Time Taken (for multiplayer only)', 
            command = lambda: self.leaderboardController.sortLeaderboard('time')
        )


        sortByDateBtn.pack(side=tk.LEFT, ipadx=5, ipady=10, padx=5)
        sortByScoreBtn.pack(side=tk.LEFT, ipadx=5, ipady=10, padx=5)
        sortByDiffBtn.pack(side=tk.LEFT, ipadx=5, ipady=10, padx=5)

        # Tabel for leaderboard 
        self.table = ttk.Treeview(self.leaderboardFrame, columns=('filename', 'date', 'difficulty', 'checkpoints', 'time'), show='headings')
        self.table.heading('filename', text='File')
        self.table.heading('date', text='Date Played')
        self.table.heading('difficulty', text='Difficulty')
        self.table.heading('checkpoints', text='Checkpoints Reached')
        self.table.heading('time', text='Time Taken')
        self.table.pack(pady=10, fill=tk.BOTH, expand=True)
    

        # make a back button 
        quitBtn = ttk.Button(self.leaderboardFrame, text='Back to Main Menu', command=self.leaderboardController.backToMain)
        quitBtn.pack(pady=5)
    
    def showLeaderboard(self, data):
        self.root.title('Leaderboard')
        self.leaderboardFrame.pack(fill=tk.BOTH)
        self.updateLeaderboard(data)
    
    def updateLeaderboard(self, data):
        for row in self.table.get_children():
            self.table.delete(row)

        for entry in data: 
            self.table.insert('', tk.END, values=(
                entry['filename'],
                entry['date'].strftime('%d-%m-%Y %H:%M'), 
                entry['difficulty'], 
                entry['checkpoints'], 
                entry['time']
            ))