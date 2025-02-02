import random 
import heapq

def generateBotMoves(botPos, checkpoints, obstacles, grid_size):
    if not checkpoints:
        return [] 
    target = min(checkpoints, key=lambda cp: abs(botPos[0] - cp[0]) + abs(botPos[1] - cp[1])) 

    def astar(start, goal):
        directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        open_set = []
        heapq.heappush(open_set, (0, start, []))  
        g_score = {start: 0}
        f_score = {start: abs(start[0] - goal[0]) + abs(start[1] - goal[1])}  

        while open_set:
            _, current, path = heapq.heappop(open_set)

            if current == goal:
                return path  

            for direction, (dr, dc) in directions.items():
                new_pos = (current[0] + dr, current[1] + dc)
                if (0 <= new_pos[0] < grid_size and 0 <= new_pos[1] < grid_size and new_pos not in obstacles):
                    tentative_g = g_score[current] + 1 
                    if new_pos not in g_score or tentative_g < g_score[new_pos]:
                        g_score[new_pos] = tentative_g
                        f_score[new_pos] = tentative_g + abs(new_pos[0] - goal[0]) + abs(new_pos[1] - goal[1])
                        heapq.heappush(open_set, (f_score[new_pos], new_pos, path + [(direction, 1)]))

        return []  

    path = astar(botPos, target)

    if not path:
        return generateRandomBotMoves()  

    return [{'direction': direction, 'steps': steps} for direction, steps in path[:3]] 



def generateRandomBotMoves():
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        botCommands = [] 

        commands = random.randint(1,3)

        for _ in range(commands):
            direction = random.choice(directions)
            steps = random.randint(1,3)
            botCommands.append({'direction': direction, 'steps':steps})
        return botCommands