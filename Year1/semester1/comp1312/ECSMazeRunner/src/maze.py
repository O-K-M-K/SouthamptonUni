"""
Provides functions for generating and manipulating a maze stored as an Adjacency List.
All coordinates count from 0 and are in the (x,y) format.
"""

from typing import Tuple, Optional

# CONSTANTS
ARROWS = {'N': ' ^ ', 'E': ' > ', 'S': ' v ', 'W': ' < '}


def create_maze(width: int = 5, height: int = 5) -> dict:
    """
    Creates a width by height maze represented as an adjacency list.
    
    A connection between two nodes represents a wall in the maze.

    The width and height are stored as keys with their respective names.

    Each 'node' represents a cell in the maze and is represented in coordinate form without brackets or commas.
    
    eg: (1,2) is "1 2"
    """
    maze = {'width': width, 'height': height}
    for i in range(height):
        for j in range(width):
            maze[f'{j} {i}'] = []
    return maze


def add_horizontal_wall(maze: dict, x_coordinate: int, horizontal_line: int) -> dict:
    """
    parameters:
        - maze is the maze as returned by the create_maze function
        - x_coordinate is the coordinate of the column to place the wall
        - horizontal_line is the row number where the wall will go with the base of the maze being 0 #

    returns:
        - maze
    """
    maze[f'{x_coordinate} {horizontal_line}'].append(f'{x_coordinate} {horizontal_line-1}')
    maze[f'{x_coordinate} {horizontal_line - 1}'].append(f'{x_coordinate} {horizontal_line}')

    return maze


def add_vertical_wall(maze, y_coordinate, vertical_line) -> dict:
    """
    parameters:
        - maze is the maze as returned by the create_maze function
        - y_coordinate is the coordinate of the row to place the wall
        - horizontal_line is the column number where the wall will go with the left edge of the maze being 0

    returns:
        - maze
    """
    maze[f'{vertical_line - 1} {y_coordinate}'].append(f'{vertical_line} {y_coordinate}')
    maze[f'{vertical_line} {y_coordinate}'].append(f'{vertical_line-1} {y_coordinate}')

    return maze


def get_dimensions(maze: dict) -> Tuple[int, int]:
    """
    returns:
        - (width, height) of maze
    """
    return (maze['width'], maze['height'])


def get_neighbors(maze: dict, coordinate: str) -> Tuple[bool|str, bool|str, bool|str, bool|str]:
    """
    Gets the avaliable nodes surrounding a given coordinate. If the neighbor is not valid its value is false.

    returns:
        - Tuple in order (N,E,S,W)
    """
    x_coordinate = int(coordinate.split(" ")[0])
    y_coordinate = int(coordinate.split(" ")[1])

    n = False
    e = False
    s = False
    w = False
    walls = maze[coordinate]

    # expression after each OR is to check if it is looking at the boundaries of the maze
    if not(f'{x_coordinate} {y_coordinate+1}' in walls or (y_coordinate+1 >= get_dimensions(maze)[1])):
        n = f'{x_coordinate} {y_coordinate+1}'
    if not(f'{x_coordinate} {y_coordinate-1}' in walls or (y_coordinate-1 < 0)):
        s = f'{x_coordinate} {y_coordinate-1}'
    if not(f'{x_coordinate+1} {y_coordinate}' in walls or (x_coordinate+1 >= get_dimensions(maze)[0])):
        e = f'{x_coordinate+1} {y_coordinate}'
    if not(f'{x_coordinate-1} {y_coordinate}' in walls or (x_coordinate-1 < 0)):
        w = f'{x_coordinate-1} {y_coordinate}'
    return (n, e, s, w)


def get_walls(maze: dict, x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
    """
    Gets the walls surrounding a given coordinate. 

    Each element takes the value of True if there is a wall and False if there is not.

    returns:
        - Tuple in order (N,E,S,W)
    """
    n = False
    e = False
    s = False
    w = False
    walls = maze[f'{x_coordinate} {y_coordinate}']

    # expression after each OR is to check if it is looking at the boundaries of the maze
    if f'{x_coordinate} {y_coordinate+1}' in walls or (y_coordinate+1 >= get_dimensions(maze)[1]):
        n = True
    if f'{x_coordinate} {y_coordinate-1}' in walls or (y_coordinate-1 < 0):
        s = True
    if f'{x_coordinate+1} {y_coordinate}' in walls or (x_coordinate+1 >= get_dimensions(maze)[0]):
        e = True
    if f'{x_coordinate-1} {y_coordinate}' in walls or (x_coordinate-1 < 0):
        w = True
    return (n, e, s, w)


def print_maze(maze: dict, runner: dict = None, goal: Optional[Tuple[int, int]] = None, shortest_path = []) -> list:
    """
    Prints maze, runner (^) position, goal (X) and shortest path ((o)) to the terminal

    Goal is defaulted as the top right corner of the maze if none is given

    returns:
        - list with each element being one row in the maze as it would be printed to the terminal.
    """

    outputMaze = []

    width, height = get_dimensions(maze)
    if goal is None:
        goal = [width-1, height-1]
    
    for i in range(height, 0, -1):
        top_row = ""
        for j in range(width):
            top_row += "+"
            if i == height or (f'{j} {i}' in maze and f'{j} {i-1}' in maze[f'{j} {i}']):
                top_row += "---"
            else:
                top_row += "   "
        top_row += "+"
        print(top_row)
        outputMaze.append(top_row)

        side_row = ""
        for j in range(width):
            if j == 0 or j == width or (f'{j} {i-1}' in maze and f'{j-1} {i-1}' in maze[f'{j} {i-1}']):
                side_row += "|"
            else:
                side_row += " "
            if runner is not None:
                if runner['x'] == j and runner['y']+1 == i:
                    side_row += ARROWS[runner['orientation']]
                elif goal[0] == j and goal[1]+1 == i:
                    side_row += " X "
                else:
                    side_row += f"   "
            elif goal[0] == j and goal[1]+1 == i:
                    side_row += " X "
            elif f"{j} {i-1}" in shortest_path:
                    side_row += "(o)"
            else:
                side_row += "   "
        side_row += "|"
        print(side_row)
        outputMaze.append(side_row)
    bottom_row = ""
    for j in range(width):
        bottom_row += "+---"
    bottom_row += "+"
    print(bottom_row)
    outputMaze.append(bottom_row)

    return outputMaze


def write_printed_maze_to_file(maze: list, file_name: str):
    """
    Include .txt in the file name.

    Writes the printed maze to "filen_name" as sometimes terminal is too small to contain full maze

    parameters:
        - maze: list of printed maze lines as returned by the "print_maze" function
    
    """
    with open(file_name, 'w') as f:
        for row in maze:
            f.write(row + '\n')
    #print(f"Written maze to {file_name}")



    


