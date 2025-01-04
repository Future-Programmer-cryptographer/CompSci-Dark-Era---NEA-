import random 

def generateBotMoves():
        directions = ['Forward', 'Backward', 'Left', 'Right']
        botCommands = [] 

        for _ in range(3):
            direction = random.choice(directions)
            steps = random.randint(1,3)
            botCommands.append({'direction': direction, 'steps':steps})
        return botCommands