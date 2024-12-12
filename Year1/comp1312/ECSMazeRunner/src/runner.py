"""
Provides functions to create a runner and manipulate its direction and position and explore a given maze.
"""

from typing import Tuple, Optional
from maze import *

# CONSTANTS
DIRECTIONS = ('N', 'E', 'S', 'W')

# Lists here are treated as movement vectors for each cardinal direction
MOVEMENT = {'N': [0, 1], 'E': [1, 0], 'S': [0, -1], 'W': [-1, 0]}
MOVEMENT_DIRECTION = {'[0, 1]': 'N', '[1, 0]': 'E', '[0, -1]': 'S', '[-1, 0]': 'W'}



def create_runner(x: int = 0, y: int = 0, orientation: str = 'N') -> dict:
    """
    parameters:
        - x is the runners starting x coordinate
        - y is the runners stating y coordinate
        - orientation should be either N, E, S or W
    returns:
        - dict: {x, y, orientation}
    """
    return {'x': x, 'y': y, 'orientation': orientation}


def get_x(runner: dict) -> int:
    return runner['x']


def get_y(runner: dict) -> int:
    return runner['y']


def get_orientation(runner: dict) -> str:
    return runner['orientation']


def get_position(runner: dict) -> str:
    """Returns runners position in format: 'x y' """
    return f"{runner['x']} {runner['y']}"


def turn(runner: dict, direction: str) -> dict:
    """
    Changes orientation of runner based on direction given

    parameters:
        - runner dict created by create_runner function
        - direction 'Left' or 'Right'
    
    returns:
        - updated runner

    raises:
        - ValueError if direction is not valid
    """

    # Treating DIRECTIONS as a circular queue by using % to wrap around
    # Left or Right moves the runners direction one 'place' backwards or forwards in the circular queue respectively
    if direction == "Left":
        runner['orientation'] = DIRECTIONS[(
            DIRECTIONS.index(runner['orientation']) - 1) % 4]
    elif direction == "Right":
        runner['orientation'] = DIRECTIONS[(
            DIRECTIONS.index(runner['orientation']) + 1) % 4]
    else:
        raise ValueError("direction must be either 'Left' or 'Right'")
    return runner


def forward(runner: dict) -> dict:
    """
    Returns runner moved one space forward in a direction dependant on its orientation
    """

    x, y = MOVEMENT[runner['orientation']]
    runner['x'] += x
    runner['y'] += y

    return runner


def sense_walls(runner: dict, maze: dict) -> Tuple[bool, bool, bool]:
    """
    Detects if there are walls right, forward or left of the runner in its current position and orientation.

    Returns walls in order [Left, Forward, Right]
    """

    walls = get_walls(maze, runner['x'], runner['y'])
    index = DIRECTIONS.index(runner['orientation'])

    # Treating walls as a circular queue by using % to wrap around
    return (walls[(index-1) % 4], walls[index], walls[(index+1) % 4])

def sense_to_node(runner, walls: list):
    """
    Turns sensed_walls to 
    """
    rx = get_x(runner)
    ry = get_y(runner)
    orientation = get_orientation(runner)
    node_list = []

    for i in range(len(walls)):
        if walls[i]:
            direction = DIRECTIONS[(DIRECTIONS.index(runner['orientation']) - 1 + i) % 4]
            x, y = MOVEMENT[direction]
            node_list.append(f"{rx+x} {ry+y}")
    return node_list




def go_straight(runner, maze) -> dict:
    """
    Moves runner forward one space in the direction they are facing if there are no walls ahed.

    returns:
        - Updated runner
    raises:
        - ValueError if there is a wall in the way
    """
    if sense_walls(runner, maze)[1]:
        raise ValueError("Can not move forward")
    else:
        return forward(runner)


def move(runner, maze) -> Tuple[dict, str]:
    """
    Determines next move using 'left-hug' algorithm

    returns:
        - (runner, movement encoded as L,F,R)
    """
    move = ""
    walls = sense_walls(runner, maze)
    if not walls[0]:
        turn(runner, 'Left')
        move = "LF"
    elif not walls[1]:
        move = "F"
    elif not walls[2]:
        turn(runner, 'Right')
        move = "RF"
    else:
        turn(runner, 'Left')
        turn(runner, 'Left')
        move = "RRF"
    go_straight(runner, maze)
    return runner, move


def explore(runner, maze, goal: Optional[Tuple[int, int]] = None, return_for_shortest_path=False, return_for_exploration=False) -> str:
    """
    Makes the runner move about the maze following the algorithm implemented in the 'move' function 
    till it reaches the goal.

    After each move a new maze is printed with the updated position of the runner

    returns:
        - By deafult: a string representing the list of moves taken by the runner
        - return_for_shortest_path: a dictionary of keys being visited nodes and values being unreachable adjacent nodes and a dictionary which can used to calculate the shortest path using the "dykstras" function in maze_runner.py
        - return_for_exploration: A list represenitng the moves taken by the runner and a list representing its position at each stage of its exploration


    """

    steps = []
    pos_list = [[get_x(runner), get_y(runner)]]
    table = {get_position(runner): [float('inf'), '']}
    seen_maze = {'width':maze['width'],'height':maze['height'],get_position(runner): sense_to_node(runner, sense_walls(runner, maze))}

    if goal is None:
        width, height = get_dimensions(maze)
        goal = [width-1, height-1]

    while (runner['x'] != goal[0] or runner['y'] != goal[1]):
        runner, movement = move(runner, maze)

        steps.append(movement)
        pos_list.append([get_x(runner), get_y(runner)])
        table[get_position(runner)] = [float('inf'), '']

        #if avoids re-writing if runner is revisitng nodes 
        if get_position(runner) not in seen_maze.keys():
            seen_maze[get_position(runner)] = sense_to_node(runner, sense_walls(runner, maze))

    if return_for_exploration:
        return steps, pos_list
    elif return_for_shortest_path:
        return seen_maze, table
    else:
        return " ".join(steps)


