import random 

def generateRandomSquares(count, exclude, size):
    exclude = set(exclude)
    positions = set()
    while len(positions) < count:
        row = random.randint(1, size - 1)
        col = random.randint(1, size - 1)
        if (row, col) not in exclude:
            exclude.add((row, col))
            positions.add((row, col))
    return list(positions)

def convertToRankAndFile(row, col):
    rank = chr(64+col)
    file = row 
    return f'{rank}{file}'