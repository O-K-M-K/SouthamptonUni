#!/usr/bin/env python

"""Provides functions to create a runner and manipulate its direction and position"""


from typing import Tuple, Optional
from maze import *

#CONSTANTS
DIRECTIONS = ('N','E','S','W')

#Lists here are treated as movement vectors for each cardinal direction
MOVEMENT = {'N': [0,1], 'E':[1,0], 'S':[0,-1], 'W':[-1,0]} 



def create_runner(x: int = 0, y: int = 0, orientation: str = 'N') -> dict[int, int, str]:
    """Return dict: {x, y, orientation}"""
    return {'x':x, 'y':y, 'orientation':orientation}

def get_x(runner: dict[int, int, str]) -> int:
    return runner['x']

def get_y(runner: dict[int, int, str]) -> int:
    return runner['y']

def get_orientation(runner: dict[int, int, str]) -> str:
    return runner['orientation']

def turn(runner: dict[int, int, str], direction: str) -> dict[int, int, str]:
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

def forward(runner: dict[int, int, str]) -> dict[int, int, str]:
    """
    Moves runner one space forward in a direction dependant on its orientation
    """

    x, y = MOVEMENT[runner['orientation']]
    runner['x'] += x
    runner['y'] += y

    return runner


def sense_walls(runner: dict, maze: dict) -> Tuple[bool, bool, bool]:
    """
    Detects if there are walls right, forward or left of the runner in its current position and orientation.

    Returns in order [Left, Forward, Right]
    """
    walls = get_walls(maze, runner['x'], runner['y'])
    index = DIRECTIONS.index(runner['orientation'])

    #Treating walls as a circular queue by using % to wrap around
    return (walls[(index-1)%4], walls[index], walls[(index+1)%4])

def go_straight(runner, maze) -> dict:
    """
    Moves runner forward one space in the direction they are facing if there are no walls ahed.
    
    If there is a wall a ValueError is raised.
    """
    if sense_walls(runner,maze)[1]:
        raise ValueError("Can not move forward")
    else:
        return forward(runner)

def move(runner, maze) -> Tuple[dict, str]:
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
        move = "LLF"
    forward(runner)
    return runner, move

def explore(runner, maze, goal : Optional[Tuple[int,int]] = None):
    steps = []
    if goal is None:
        width, height = get_dimensions(maze)
        goal = [width-1, height-1]
    while (runner['x'] != goal[0] or runner['y'] != goal[1]):
        runner, mv = move(runner, maze)
        print_maze(maze, runner, goal)
        steps.append(mv)
    print("REACHED GOAL!")
    return steps


maze = create_maze(4,3)
maze = add_horizontal_wall(maze, 1, 1)
maze = add_horizontal_wall(maze, 2, 2)
maze = add_horizontal_wall(maze, 1, 2)
maze = add_vertical_wall(maze, 0,2)
maze = add_vertical_wall(maze, 1,1)
maze = add_horizontal_wall(maze,3,1)

runner = create_runner(1,0,'N')
print_maze(maze, runner)
print(explore(runner, maze, [1,1]))
