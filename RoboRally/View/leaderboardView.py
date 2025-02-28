import tkinter as tk 
from tkinter import ttk 

class LeaderboardView: 
    def __init__(self, root, leaderboardController):

        # View class to display leaderboard 

        self.root = root 
        self.leaderboardController = leaderboardController

        # button styling 
        style = ttk.Style() 

        # creating the leaderboard frame to pack different buttons and labels 
        self.leaderboardFrame = tk.Frame(self.root)
        
        # creating the buttons and options 
        label = ttk.Label(self.leaderboardFrame, text='Leaderboard', font=('fixedsys 20 bold'))
        label.pack(pady=5)

        # Creating an options frame for sorting buttons  
        self.sortOptionsFrame = tk.Frame(self.leaderboardFrame)
        self.sortOptionsFrame.pack(pady=5)

        sortByDateBtn = ttk.Button(
            self.sortOptionsFrame, 
            text='Sort by Date', 
            style='smallplay.TButton',
            command = lambda: self.leaderboardController.sortLeaderboard('date')
        )

        sortByDiffBtn = ttk.Button(
            self.sortOptionsFrame, 
            text='Sort by Difficulty',
            style='smallplay.TButton', 
            command = lambda: self.leaderboardController.sortLeaderboard('difficulty')
        )

        sortByScoreBtn = ttk.Button(
            self.sortOptionsFrame, 
            text='Sort by Checkpoints Reached',
            style='smallplay.TButton',
            command = lambda: self.leaderboardController.sortLeaderboard('checkpoints')
        )

        sortByTimeBtn = ttk.Button(
            self.sortOptionsFrame, 
            text='Sort by Time Taken (for multiplayer only)', 
            style='smallplay.TButton',
            command = lambda: self.leaderboardController.sortLeaderboard('time')
        )

        sortByDateBtn.pack(side=tk.LEFT, ipadx=5, ipady=10, padx=5)
        sortByScoreBtn.pack(side=tk.LEFT, ipadx=5, ipady=10, padx=5)
        sortByDiffBtn.pack(side=tk.LEFT, ipadx=5, ipady=10, padx=5)
        sortByTimeBtn.pack(side=tk.LEFT, ipadx=5, ipady=10, padx=5)

        # button styling (same as one from playGameView)
        style.configure('smallplay.TButton',font=('fixedsys', 17), foreground='red3')
        style.configure('play.TButton', font=('fixedsys 20 bold'), foreground='red3')

        # Tabel for leaderboard 
        self.table = ttk.Treeview(self.leaderboardFrame, columns=('filename', 'date', 'difficulty', 'checkpoints', 'time'), show='headings')
        self.table.heading('filename', text='File')
        self.table.heading('date', text='Date Played')
        self.table.heading('difficulty', text='Difficulty')
        self.table.heading('checkpoints', text='Checkpoints Reached')
        self.table.heading('time', text='Time Taken (seconds)')
        self.table.pack(pady=10, fill=tk.BOTH, expand=True)

        style2 = ttk.Style() 
        style2.configure('Treeview.Heading', font=('fixedsys', 12))
        style2.configure('Treeview', rowheight=30)

        # make a back button 
        quitBtn = ttk.Button(
            self.leaderboardFrame, 
            text='Back to Main Menu', 
            style='play.TButton',
            command=self.leaderboardController.backToMain)
        quitBtn.pack(pady=10)
    
    # method called by the leaderboardController to display the leaderboard to the user 
    def showLeaderboard(self, data):
        self.root.title('Leaderboard')
        self.leaderboardFrame.pack(fill=tk.BOTH)
        self.updateLeaderboard(data)
    
    # method to update the leaderboard with new entries 
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