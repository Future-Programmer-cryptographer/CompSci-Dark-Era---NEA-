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



def getMdPos(contents, key):
    for line in contents:
        if key in line:
            # Extract the positions string after '**Positions:**'
            positions = line.split("**")[2].strip()
            try:
                # Convert each coordinate string '(x, y)' into a tuple (x, y)
                return [
                    tuple(map(int, pos.strip("()").split(", ")))
                    for pos in positions.split("), ")
                ]
            except ValueError as e:
                raise ValueError(f"Malformed positions in '{key}': {positions}") from e
    return []



def getMdValue(contents, key):
    for line in contents:
        if key in line:
            try:
                return line.split("**")[2].strip()
            except IndexError:
                raise ValueError(f"Key '{key}' not found in the file or is malformed.")