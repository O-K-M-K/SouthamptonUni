from runner import *
import argparse 
from re import fullmatch

WALL_ADD = [[0,1],[1,0],[0,-1],[-1,0]]

def get_shortest_path(table, goal):
    shortest_path = []
    #link through previous vertex of goal till one with no previous vertex is reached
    current_vertex = goal
    #print(current_vertex)
    while current_vertex != '':
        shortest_path.append(current_vertex)
        current_vertex = table[current_vertex][1]
    return shortest_path

def dykstras(table, maze, starting: Optional[Tuple[int, int]] = None, goal: Optional[Tuple[int, int]] = None) -> list[Tuple[int, int]]:
    #TODO: ASK IF SENSING NEIGHBOURS IS OK IF ALL I HAVE IS A MAP OF NODES. TECHNICALLY I KNOW THE NEIGHBOURS BUT I AM NOT USING THE RUNNER HERE...
    #TODO: make choice of nodes, vertex and coordinates consistant
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


def shortest_path(maze, starting: Optional[Tuple[int, int]] = None, goal: Optional[Tuple[int, int]] = None) -> list[Tuple[int, int]]:
    if goal is None:
        goal = [maze['width']-1, maze['height']-1]
        node_goal = f"{maze['width']-1} {maze['height']-1}"
    else:
        node_goal = f"{goal[0]} {goal[1]}"
    
    if starting is None:
        starting = [0, 0]
        node_starting = f"0 0"
    else:
        node_starting = f"{starting[0]} {starting[1]}"

    runner = create_runner(starting[0], starting[1])
    exploration, table = explore(runner, maze, goal)
    shortest = dykstras(table, maze, starting, goal)
    return exploration, shortest
    

def calculate_score(shortest_path: list, exploration_steps: str):
    steps = len(exploration_steps.split(" "))
    return steps / 4 + len(shortest_path)

def write_to_stats_file(input_name, exploration_steps, shortest_path):
    score = calculate_score(shortest_path, exploration_steps)

    with open('statistics.txt', 'w') as f:
        f.write("Name: " + input_name + '\n')
        f.write("Score: " + str(score) + '\n')
        f.write("Exploration Steps: " + str(len(exploration_steps.split(" "))) + '\n')
        f.write("Shortest Path: " + str(shortest_path) + '\n')
        f.write("Length of shortest path: " + str(len(shortest_path)))




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
    Returns a adjacency list representation of the maze 
    """
    try:
        with open(maze_file) as f:
            file = []
            for line in f.readlines():
                file.append(line.strip())
    except:
        raise IOError("There was an error reading the file")
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
            raise ValueError(f'Invalid format for --starting argument. Expected format: "x, y" (e.g. "1, 2")')
    if args.goal:
        if not fullmatch(r"[0-9]+, [0-9]+", args.goal):
            raise ValueError(f'Invalid format for --goal argument. Expected format: "x, y" (e.g. "1, 2")')

def validate_values(maze, starting: Tuple[int, int]|None, goal: Tuple[int, int]|None):
    """Ensures the starting and goal values are within the bounds of the maze"""
    if starting:
        starting_x = starting[0]
        starting_y = starting[1]
        if not (0 <= starting_x <= maze['width']-1) or not (0 <= starting_y <= maze['height']-1):
            raise OutOfBoundsError(f"starting position out of bounds for maze provided.\n Starting position must be within bounds 0 <= x <= {maze['width']-1}, 0 <= y <= {maze['height']-1} ")
    if goal:
        goal_x = goal[0]
        goal_y = goal[1]
        if not (0 <= goal_x <= maze['width']-1) or not (0 <= goal_y <= maze['height']-1):
            raise OutOfBoundsError(f"Goal position out of bounds for maze provided.\n Goal position must be within bounds 0 <= x <= {maze['width']-1}, 0 <= y <= {maze['height']-1} ")
    
def validate_maze_format(maze: list):
    """
    Ensures given maze is of a valid format. Raises ValueError if not.
    """
    width = len(maze[0])

    if not all(len(row)==width for row in maze):
        raise ValueError("All rows must be the same width")
    if maze[0] != width * maze[0][0]:
        raise ValueError("The top or bottom rows are not all walls")
    if not all((row[0]=='#' and row[-1]=='#') for row in maze):
        raise ValueError("Maze is not fully enclosed by walls")
    for i in range(0,len(maze),2):
        for j in range(0,len(maze),2):
            if maze[i][j] != '#':
                raise ValueError("The intersections between a horizontal line and a vertical line must be a #")
    if not all(c in {'.', '#'} for row in maze for c in row):
        raise ValueError("Only '.' and '#' characters are allowed")
    



def main():
    parser = argparse.ArgumentParser(
        description="ECS Maze Runner",
        epilog='Example usage: python maze_runner.py maze1.mz --starting "2, 1" --goal "4, 5"'
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

    maze = maze_reader(args.maze)
    starting = list(map(int, args.starting.split(", "))) if args.starting else None
    goal = list(map(int, args.goal.split(", "))) if args.goal else None

    validate_syntax(args)
    validate_values(maze, starting, goal)


    exploration_steps, shortest = shortest_path(maze, starting, goal)
    write_maze = print_maze(maze, shortest_path=shortest)
    write_printed_maze_to_file(write_maze)
    write_to_stats_file(args.maze, exploration_steps, shortest)


if __name__ == "__main__":
    main()