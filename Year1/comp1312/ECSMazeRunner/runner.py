# while (num := input("Number: ")) != "10":
#     print("Enter a valid number")

#CONSTANTS
DIRECTIONS = ('N','E','S','W')
MOVEMENT = {'N': [0,1], 'E':[1,0], 'S':[0,-1], 'W':[-1,0]} #Lists here are treated as movement vectors for each cardinal direction

def create_runner(x: int = 0, y: int = 0, orientation: str = 'N') -> dict:
    return {'x':x, 'y':y, 'orientation':orientation}

def get_x(runner: dict) -> int:
    return runner['x']

def get_y(runner: dict) -> int:
    return runner['y']

def get_orientation(runner: dict) -> str:
    return runner['orientation']

def turn(runner: dict, direction: str) -> dict:
    """
    Changes orientation of runner based on direction given
    
    Args
        - runner (dict) dict created by create_runner function
        - direction (str) Left or Right
    """
    
    #Treating DIRECTIONS as a circular queue by using % to wrap around
    #Left or Right moves the runners direction one 'place' backwards or forwards in the circular queue respectively
    if direction == "Left":
        runner['orientation'] = DIRECTIONS[(DIRECTIONS.index(runner['orientation']) - 1)%4]
    else:
        runner['orientation'] = DIRECTIONS[(DIRECTIONS.index(runner['orientation']) + 1)%4]
    return runner

def forward(runner: dict) -> dict:
    """
    Moves runner one space forward in a direction dependant on its orientation
    """

    x, y = MOVEMENT[runner['orientation']]
    runner['x'] += x
    runner['y'] += y

    return runner

