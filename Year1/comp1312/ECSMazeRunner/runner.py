# while (num := input("Number: ")) != "10":
#     print("Enter a valid number")

# print(num)
DIRECTIONS = ('N','E','S','W')
MOVEMENT = {'N': [0,1], 'E':[1,0], 'S':[0,-1], 'W':[-1,0]}

def create_runner(x: int = 0, y: int = 0, orientation: str = 'N'):
    return {'x':x, 'y':y, 'orientation':orientation}


def get_x(runner):
    return runner['x']

def get_y(runner):
    return runner['y']

def get_orientation(runner):
    return runner['orientation']

def turn(runner, direction: str):
    
    if direction == "Left":
        runner['orientation'] = DIRECTIONS[(DIRECTIONS.index(runner['orientation']) - 1)%4]
    else:
        runner['orientation'] = DIRECTIONS[(DIRECTIONS.index(runner['orientation']) + 1)%4]
    return runner

def forward(runner):
    x, y = MOVEMENT[runner['orientation']]
    runner['x'] += x
    runner['y'] += y

    return runner

