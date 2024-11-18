#!/usr/bin/env python
"""Provides functions for generating and manipulating a maze stored as an Adjacency List"""

#IMPORTS
from typing import Tuple

ARROWS = {'N':' ^ ','E':' > ','S':' v ', 'W':' < '}

def create_maze(width: int = 5, height: int = 5) -> dict:
    """Creates a Adjacency List with a connection between two nodes representing a wall in the maze"""
    maze = {'width':width, 'height':height}
    for i in range(height):
        for j in range(width):
            maze[f'{j}{i}'] = []
    return maze


def add_horizontal_wall(maze: dict, x_coordinate: int, horizontal_line: int) -> dict:
    """
    Parameters:
        - maze is the maze as returned by the create_maze function
        - x_coordinate is the coordinate of the column to place the wall
        - horizontal_line is the row number where the wall will go with the base of the maze being 0 
    """
    maze[f'{x_coordinate}{horizontal_line}'].append(f'{x_coordinate}{horizontal_line-1}')
    maze[f'{x_coordinate}{horizontal_line-1}'].append(f'{x_coordinate}{horizontal_line}')
    return maze

def add_vertical_wall(maze, y_coordinate, vertical_line) -> dict:
    maze[f'{vertical_line-1}{y_coordinate}'].append(f'{vertical_line}{y_coordinate}')
    maze[f'{vertical_line}{y_coordinate}'].append(f'{vertical_line-1}{y_coordinate}')
    return maze

def get_dimensions(maze: dict) -> Tuple[int, int]:
    """
    returns: [width, height]
    """
    return [maze['width'],maze['height']]

def get_walls(maze: dict, x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
    """
    
    Returns
        - N,E,S,W
    """
    n = False
    e = False
    s = False
    w = False
    walls = maze[f'{x_coordinate}{y_coordinate}']
    #expression after OR is to check if it is looking at the boundaries of the maze
    if f'{x_coordinate}{y_coordinate+1}' in walls  or (y_coordinate+1>=get_dimensions(maze)[1]):
        n = True
    if f'{x_coordinate}{y_coordinate-1}' in walls or (y_coordinate-1<0):
        s = True
    if f'{x_coordinate+1}{y_coordinate}' in walls or (x_coordinate+1>=get_dimensions(maze)[0]):
        e = True
    if f'{x_coordinate-1}{y_coordinate}' in walls or (x_coordinate-1<0):
        w = True
    return (n,e,s,w)

def print_maze(maze: dict, runner: dict = None, goal: Tuple[int, int] = None):
    width, height = get_dimensions(maze)
    if goal is None:
        goal = [width-1, height-1]
    for i in range(height, 0, -1):
        top_row = ""
        for j in range(width):
            top_row += "+"
            if i == height or (f'{j}{i}' in maze and f'{j}{i-1}' in maze[f'{j}{i}']):
                top_row += "---"
            else:
                top_row += "   "
        top_row+="+"
        print(top_row)

        side_row = ""
        for j in range(width):
            if j == 0 or j == width or (f'{j}{i-1}' in maze and f'{j-1}{i-1}' in maze[f'{j}{i-1}']):
                side_row += "|"
            else:
                side_row += " "
            if runner is not None:
                if runner['x'] == j and runner['y']+1 == i:
                    side_row += ARROWS[runner['orientation']]
                elif goal[0] == j and goal[1]+1 == i:
                    side_row += " X "
                else:
                    side_row+="   "
            else:
                side_row+="   "
        print(side_row + "|")
    bottom_row = ""
    for j in range(width):
        bottom_row += "+---"
    bottom_row+="+"
    print(bottom_row)

