import random 

def generateRandomSquares(count, exclude, size):
    # function to generate random squares for a given grid size 
    # useful for randomising start positions and obstacles/checkpoints 
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


# function to extract the markdown position as tuples 
def getMdPos(contents, key):
    # search through files lines for the line containing key (eg: 'Player Checkpoints')
    for line in contents:
        if key in line:
            # Extract the position from that line and convert each coordinate string into a tuple (x,y)
            positions = line.split("**")[2].strip()
            try:
                return [
                    tuple(map(int, pos.strip("()").split(", ")))
                    for pos in positions.split("), ")
                ]
            except ValueError as e:
                raise ValueError(f"Error getting pos in '{key}': {positions}") from e
    return []


# function to extract a SINGLE value 
def getMdValue(contents, key):
    for line in contents:
        if key in line:
            try:
                return line.split("**")[2].strip()
            except IndexError:
                raise ValueError(f"key '{key}' not found in the file")