"""
Provides functions for reading a maze from a file, calculating the shortest path of the maze and writing statistics and explorations path to files.
"""

from runner import *
import argparse 
from re import fullmatch
from typing import Tuple, Optional


def get_shortest_path(table: dict, goal) -> list[Tuple[int, int]]:
    """
    Retreives the shortest path from the start node to the goal node by tracing through the table 
    created by dijkstras.
    """
    shortest_path = []

    #Starting vertex is the one with no value 
    current_vertex = goal
    while current_vertex != '':
        shortest_path.append((int(current_vertex.split(" ")[0]), int(current_vertex.split(" ")[1])))
        current_vertex = table[current_vertex][1]
    return shortest_path[::-1]

def dijkstras(table:dict, maze, starting: Optional[Tuple[int, int]] = None, goal: Optional[Tuple[int, int]] = None) -> list[Tuple[int, int]]:
    """
    Uses dijkstras shortest path algorithm to find the shortest path from the starting node to all other nodes in the table.
    """

    if goal is None:
        goal = f"{maze['width']-1} {maze['height']-1}"
    else:
        goal = f"{goal[0]} {goal[1]}"
    
    if starting is None:
        starting = f"0 0"
    else:
        starting = f"{starting[0]} {starting[1]}"

    startingVertex = starting
    table[startingVertex] = [0, '']

    unvisited = list(table.keys())

    current_vertex = startingVertex
    
    while len(unvisited) != 0:
        current_vertex = min(unvisited, key=lambda vertex: table[vertex][0])

        neighbours = []
        
        for i in get_neighbors(maze, current_vertex): 
            if i in unvisited:
                neighbours.append(i)
        
        
        #Calculating min distance to neighbouring nodes and updating the value if the calculated distance is shorter than the current distance.
        min_distance = float('inf')
        closest_vertex = ''
        for neighbour in neighbours:
            distance = table[current_vertex][0] + 1
            if distance < min_distance:
                min_distance = distance
                closest_vertex = neighbour
            if distance < table[neighbour][0]:
                table[neighbour][0] = distance
                table[neighbour][1] = current_vertex
        unvisited.remove(current_vertex)

    shortest_path = get_shortest_path(table, goal)
    return shortest_path


def format_path_for_printing(shortest_path):
    """
    Formates the shortest path from [(x1, y1), (x2, y2), ... (xn, yn)] to ["x1 y1", "x2 y2", ... "xn yn"] format
     """
    formatted_path = []
    for node in shortest_path:
        formatted_path.append(f"{node[0]} {node[1]}")
    return formatted_path

def shortest_path(maze, starting: Optional[Tuple[int, int]] = None, goal: Optional[Tuple[int, int]] = None) -> list[Tuple[int, int]]:
    """
    Finds the shortest path between a start and goal node using Dijkstra's algorithm.
    """
    if goal is None:
        goal = [maze['width']-1, maze['height']-1]
    
    if starting is None:
        starting = [0, 0]

    runner = create_runner(starting[0], starting[1])
    seen_maze, table = explore(runner, maze, goal, return_for_shortest_path=True)
    shortest = dijkstras(table, seen_maze, starting, goal)
    return shortest

    

def calculate_score(shortest_path: list, exploration_steps: str):
    """
    Score calculated with formula: exploration_steps / 4 + length of shortest path
    """
    steps = len(exploration_steps.split(" "))
    return steps / 4 + len(shortest_path)

def write_to_stats_file(input_name, exploration_steps, shortest_path):
    """
    Write maze statistics to statistics.txt in order:
    1. Input File Name
    2. Score (which is exploration_steps / 4 + path_length)
    3. Number of steps in exploration
    4. Shortest path found
    5. Length of shortest path found
    """
    score = calculate_score(shortest_path, exploration_steps)

    with open('statistics.txt', 'w') as f:
        f.write(input_name + '\n')
        f.write(str(score) + '\n')
        f.write(str(len(exploration_steps.split(" "))) + '\n')
        f.write(str(shortest_path) + '\n')
        f.write(str(len(shortest_path)))
    #print("Written stats to statistics.txt")

def write_to_exploration_file(runner, maze, goal):
    steps, pos = explore(runner, maze, goal, return_for_exploration=True)
    with open('exploration.csv', 'w') as f:
        f.write("Step,x-coordinate,y-coordinate,Actions\n")
        for i in range(len(steps)):
            step = i+1
            x_coordinate = pos[i][0]
            y_coordinate = pos[i][1]
            action = steps[i]
            f.write(f"{step},{x_coordinate},{y_coordinate},{action}\n")
    #print("Written exploration to exploration.csv")


def populate_maze(empty_maze: dict, read_maze:list) -> dict:
    """
    Populates maze with walls to match the maze given
    """
    maze_contents = read_maze[1:-1]
    maze_contents = maze_contents[::-1]
    for row in range(len(maze_contents)):
        row_contents = maze_contents[row][1:-1]
        for column in range(len(row_contents)):
            if row % 2 == 0 and column % 2 != 0 and row_contents[column] == '#':
                empty_maze = add_vertical_wall(empty_maze, row//2, (column+1)//2)
            elif row % 2 != 0 and column % 2 == 0 and row_contents[column] == '#':
                empty_maze = add_horizontal_wall(empty_maze, column//2, (row+1)//2)

    return empty_maze


def maze_reader(maze_file: str) -> dict:
    """
    Returns a adjacency list representation of the maze.

    Will validate the maze format before creating and populating the maze raising a ValueError if the format is invalid.

    """
    try:
        with open(maze_file) as f:
            file = []
            for line in f.readlines():
                file.append(line.strip())
    except:
        raise IOError(f"IOError: An error occured while reading maze file: {maze_file}")
    width = (len(file[0]) -1) // 2
    height = (len(file) -1) // 2 

    
    validate_maze_format(file)
   
    maze = create_maze(width, height)
    maze = populate_maze(maze, file)
    
    return maze

        


class OutOfBoundsError(ValueError):
    pass


def validate_syntax(args: argparse.Namespace):
    if args.starting:
        if not fullmatch(r"[0-9]+, [0-9]+", args.starting):
            raise ValueError(f'Argument Error: Invalid format for --starting argument. Expected format: "x, y" (e.g. "1, 2") Recieved format: "{args.starting}"')
    if args.goal:
        if not fullmatch(r"[0-9]+, [0-9]+", args.goal):
            raise ValueError(f'Argument Error: Invalid format for --goal argument. Expected format: "x, y" (e.g. "1, 2") Recieved format: "{args.goal}"')

def validate_values(maze, starting: Tuple[int, int]|None, goal: Tuple[int, int]|None):
    """Ensures the starting and goal values are within the bounds of the maze"""
    if starting:
        starting_x = starting[0]
        starting_y = starting[1]
        if not (0 <= starting_x <= maze['width']-1) or not (0 <= starting_y <= maze['height']-1):
            raise OutOfBoundsError(f"Argument Error: starting position out of bounds for maze provided.\nStarting position must be within bounds: 0 <= x <= {maze['width']-1}, 0 <= y <= {maze['height']-1}\n")
    if goal:
        goal_x = goal[0]
        goal_y = goal[1]
        if not (0 <= goal_x <= maze['width']-1) or not (0 <= goal_y <= maze['height']-1):
            raise OutOfBoundsError(f"Argument Error: Goal position out of bounds for maze provided.\nGoal position must be within bounds: 0 <= x <= {maze['width']-1}, 0 <= y <= {maze['height']-1} ")
    
def validate_maze_format(maze: list):
    """
    Ensures given maze is of a valid format. Raises ValueError if not.
    """
    width = len(maze[0])

    try:
        a = maze[0][0]
    except:
        raise ValueError("Invalid maze format: Unable to read maze correctly")

    if not all(c in {'.', '#'} for row in maze for c in row):
        raise ValueError("Invalid maze format: Only '.' and '#' characters are allowed")
    
    if not all(len(row)==width for row in maze):
        raise ValueError(f"Invalid maze format: All rows must be the same width")
    
    if maze[0] != width * maze[0][0] or maze[-1] != width * maze[0][0]:
        raise ValueError("Invalid maze format: Either top or bottom rows are not all walls '#'")
    
    if not all((row[0]=='#' and row[-1]=='#') for row in maze):
        raise ValueError("Invalid maze format: Maze is not fully enclosed by walls")
    
    for i in range(0,len(maze),2):
        for j in range(0,len(maze),2):
            if maze[i][j] != '#':
                raise ValueError("Invalid maze format: The intersections between a horizontal line and a vertical line must be a '#'")
            
    for i in range(1,len(maze)-1,2):
        for j in range(1,len(maze)-1,2):
            if maze[i][j] != ".":
                raise ValueError("Invalid maze format: A wall has been placed in a square rather than at a wall")
    
    



def main():
    parser = argparse.ArgumentParser(
        description="ECS Maze Runner",
        epilog='Example usage: python3 maze_runner.py maze1.mz --starting "2, 1" --goal "4, 5"'
    )
    
    parser.add_argument(
        "maze", 
        type=str, 
        help="The name of the maze file, e.g., maze1.mz"
    )
    parser.add_argument(
        "--starting", 
        type=str, 
        default=None, 
        help='The starting position, e.g., "2, 1"'
    )
    parser.add_argument(
        "--goal", 
        type=str, 
        default=None, 
        help='The goal position, e.g., "4, 5"'
    )

    args = parser.parse_args()

    try:
        validate_syntax(args)
        maze = maze_reader(args.maze)
    except Exception as e:
        print(e)
        return
    
    #formatting starting and goal values
    starting = list(map(int, args.starting.split(", "))) if args.starting else None
    goal = list(map(int, args.goal.split(", "))) if args.goal else None

    try:
        validate_values(maze, starting, goal)
    except Exception as e:
        print(e)
        return

    #Two runners are needed as for required outputs the maze has to be explored twice and the runners position does not reset once the goal is reached
    #Both runners explore exactly the same way one after tha other and are not sharing information in any way. 
    #It is only because the explore has 3 possible outputs depending on what is required

    if starting is None:
        runner = create_runner()
        runner2 = create_runner()
    else:
        runner = create_runner(starting[0],starting[1])
        runner2 = create_runner(starting[0],starting[1])

    

    exploration_steps = explore(runner, maze, goal)
    shortest = shortest_path(maze, starting, goal)

    #NOTE: Uncomment below line to print maze with shortest path to terminal
    printed_maze = print_maze(maze, shortest_path=format_path_for_printing(shortest), goal=goal)

    write_to_stats_file(args.maze, exploration_steps, shortest)
    write_to_exploration_file(runner2, maze, goal)

    #NOTE: Uncomment below line and above commented line to write the printed maze to outputMaze.txt
    write_printed_maze_to_file(printed_maze, "outputMaze.txt")


if __name__ == "__main__":
    main()