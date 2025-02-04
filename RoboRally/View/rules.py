import tkinter as tk 
from tkinter import ttk 


class RulesWindow: 
    def __init__(self, root): 
        self.root = root 
        self.root.title('Robo Rally Rules')

        # creating rules frame 
        self.rulesFrame = tk.Frame(self.root)
        self.rulesFrame.pack(fill=tk.BOTH)

        titleLabel = ttk.Label(self.rulesFrame, text='Robo Rally Rules',  font=('fixedsys 20 bold'), foreground='red3')
        titleLabel.pack(pady=10)

        mainLabel = ttk.Label(self.rulesFrame, text='Objective: Program your robot to avoid obstacles and get to as many checkpoints as you can!', font=('verdana',15, 'bold'))
        mainLabel.pack(pady=5)

        rulesFrame = ttk.Frame(self.rulesFrame)
        rulesFrame.pack(pady=10)

        section1 = ttk.Label(rulesFrame, text='Rules about Program Cards and Slots', font=('verdana', 13, 'bold'), foreground='red3')
        text1 = ttk.Label(rulesFrame, text="- In both single player and multiplayer games modes, player/s will receive 5 random program cards each turn from which they must select either 1, 2 or 3 for that turn. \n - The player has to drag and drop cards into the empty card slots in the order they want their cards to be played (left to right) \n - The player will also have the option to undo a move by clicking on the 'Undo' button", font=('verdana', 12), wraplength=550, justify='left')

        section2 = ttk.Label(rulesFrame, text='Checkpoints and Obstacles', font=('verdana', 13, 'bold'), foreground='red3')
        text2 = ttk.Label(rulesFrame, text='- In this version of Robo Rally, there are only two special squares in the grid: obstacles and checkpoints. \n - Obstacles are grey squares and the checkpoints are shown as green triangles on the board (images shown below)', wraplength=550, font=('verdana', 12), justify='left')

        section3 = ttk.Label(rulesFrame, text='Health, Scoring, Winning, and Move History', font=('verdana', 13, 'bold'), foreground='red3')
        text3 = ttk.Label(rulesFrame, text="- In single player, both the player and bot will start with 5 lives each. \n - In multiplayer, the starting health will be 10 \n - You will lose a life if you go off grid or if you collide with any of the obstacles squares on the board. \n - You will gain a life for each checkpoint you reach. \n - In order to win in Single player, you must have more checkpoints reached than the BOT. \n - In multiplayer mode, your team needs to try and get to all the checkpoints in the shortest amount of time possible (there will be stopwatch on top right for you see your time). \n In single player vs bot mode, players will be able to view their move history, as well as the bot's move history on the left hand side.", wraplength=550, font=('verdana', 12), justify='left')

        section4 = ttk.Label(rulesFrame, text='Saving/Loading Games and Leaderboard', font=('verdana', 13, 'bold'), foreground='red3')
        text4 = ttk.Label(rulesFrame, text="- Users can save their game to a markdown (.md) file by clicking on the 'Save Game' button. You will be asked to enter a file name for your file so that your score/time can be showed on the leaderboard. \n LEADERBOARD - Players can view the leaderboard by clicking on the 'View Leaderboard' button on Main Menu. The leaderboard can be sorted by Date Played (most recent at the top), Checkpoints Reached, Difficulty, or Time Taken (avaibale for multiplayer game only) \n - Users can also load their game by clicking the 'Load From a Saved Game' button on the Menu Menu screen. The move histoyr will not be restored, but players can resume their game from where they saved it.", wraplength=550, font=('verdana', 12), justify='left')
        
        section1.grid(row=0, column=0, padx=20, pady=10)
        text1.grid(row=1, column=0, padx=20, pady=10)
        
        section2.grid(row=0, column=1, padx=20, pady=10)
        text2.grid(row=1, column=1, padx=20, pady=10)

        section3.grid(row=2, column=0, padx=20, pady=10)
        text3.grid(row=3, column=0, padx=20, pady=10)

        section4.grid(row=2, column=1, padx=20, pady=10)
        text4.grid(row=3, column=1, padx=20, pady=10)


        