import sys

# Variables
file = None
num_lives = None
num_steps = None
num_gold = None
num_rows = None
num_col = None
grid = None
# Game Variables
destination_x = None
destination_y = None
current_x = None
current_y = None
current_lives = None
current_steps = None # Refers to the current remaining steps
current_gold = None # Refers to the amount of gold collected



def init_game(configFile):
    global file
    global num_lives
    global num_steps
    global num_gold
    global num_rows
    global num_col
    global grid

    global current_steps
    global current_lives
    global current_gold

    try:
        file = open(configFile, "r")
    except FileNotFoundError:
        print("File not found")
        return 1

    # read game varialbes
    num_lives, num_steps, num_gold, num_rows = file.readline().split(" ")
    num_lives = int(num_lives)
    num_steps = int(num_steps)
    num_gold = int(num_gold)
    num_rows = int(num_rows)
    #print(f"{num_lives}, {num_steps}, {num_gold}, {num_rows}")

    grid = []
    for i in range(num_rows):
        grid.append(file.readline())

    # find length of row
    lengths = []
    for i in range(num_rows):
        lengths.append(len(grid[i]) - 1)
    num_col = max(lengths)

    get_current_x()
    get_current_y()
    get_destination_x()
    get_destination_y()
    current_steps = num_steps
    current_lives = num_lives
    current_gold = 0

    file.close()

def get_destination_x():
    global destination_x
    for line in grid:
        if line.find("@") == -1:
            continue
        else:
            destination_x = line.find("@")
            return line.find("@")
    # if not found
    return -1

def get_destination_y():
    global destination_y
    for i in range(num_rows):
        if grid[i].find("@") != -1:
            destination_y = i
            return i
    # if not found
    return -1

def save_game(toFileName):
    file = open(toFileName, "w")
    file.write(f"{num_lives} {num_steps} {num_gold} {num_rows}\n")
    for line in grid:
        file.write(line)
    file.close()

def get_current_x():
    global current_x
    for line in grid:
        if line.find("&") == -1:
            continue
        else:
            current_x = line.find("&")
            return current_x
    # if not found
    return -1

def get_current_y():
    global current_y
    for i in range(num_rows):
        if grid[i].find("&") != -1:
            current_y = i
            return current_y
    # if not found
    return -1

def get_num_lives():
    return current_lives

def get_remaining_steps():
    return current_steps

def get_remaining_gold():
    return current_gold

def is_maze_completed():
    if (get_current_X() == dest_X and get_current_Y() == dest_Y):
        return True
    else:
        return False

def is_valid_coordinate(x, y):
    if (x < 0 or y < 0 or x > (num_col - 1) or y > (num_rows - 1)):
        return False
    else:
        return True

def can_move_to(x, y):
    return is_valid_coordinate(x, y)

def move_to(x, y):
    global current_steps
    global grid
    global current_lives
    global current_steps
    global current_gold

    old_x = get_current_x()
    old_y = get_current_y()

    gold = 0

    if (can_move_to(x, y)):
        current_steps -= 1
        print(f"Moved to ({x}, {y})")

        try:
            gold = int(grid[y][x])
            current_gold += gold
        except ValueError:
            pass

        # Move Character Piece
        grid[y] = replace_str_index(grid[y], x, "&")

        # Erase old Character Piece
        grid[old_y] = replace_str_index(grid[old_y], old_x, ".")

        get_current_x()
        get_current_y()
    else:
        current_lives -= 1
        current_steps -= 1
        print("Invalid move, One life lost.")

def replace_str_index(string, index, replacement):
    return "%s%s%s"%(string[:index], replacement, string[index + 1:])

def is_maze_completed():
    if(get_current_x() == destination_x and get_current_y() == destination_y):
        return True
    else:
        return False

def print_something():
    print(destination_x)

def is_game_end():
    if (is_maze_completed()):
        return 3
    elif(current_steps <= 0):
        return 2
    elif(current_lives <= 0):
        return 1

def print_help():
    print("Usage: You can type one of the following commands.")
    print("help         Print this help message.")
    print("board        Print the current board.")
    print("status       Print the current status.")
    print("left         Move the player 1 square to the left.")
    print("right        Move the player 1 square to the right.")
    print("up           Move the player 1 square up.")
    print("down         Move the player 1 square down.")
    print("save <file>  Save the current game configuration to the given file.")
    print("quit         Quits the game without saving")


def print_status():
    global current_lives
    global current_steps
    global current_gold
    print(f"Number of live(s): {current_lives}\nNumber of step(s) remaining: {current_steps}\nAmount of gold: {current_gold}\n")

def print_board():
    for line in grid:
        print(line[:num_col])

def perform_action(action):
    action = action.strip()
    params = action.split(" ")
    if(params[0] == "help"):
        print_help()
    elif (params[0] == "board"):
        print_board()
    elif (params[0] == "status"):
        print_status()
    elif (params[0] == "left"):
        move_to(get_current_x() - 1, get_current_y())
    elif (params[0] == "right"):
        move_to(get_current_x() + 1, get_current_y())
    elif (params[0] == "up"):
        move_to(get_current_x(), get_current_y() - 1)
    elif (params[0] == "down"):
        move_to(get_current_x(), get_current_y() + 1)
    elif (params[0] == "save" and len(params) == 2):
        try:
            save_game(params[1])
            print(f"Successfully saved current game to {params[1]}")
        except Exception as e:
            print(f"Could not save current game configuration to {params[1]}")
    else:
        print("Invalid argument")


def start_game(args):
    if (len(sys.argv) != 2):
        print("Expect 1 argument")
        return

    init_game(sys.argv[1])

    command = None
    command = input()
    while command != "quit":
        perform_action(command)
        if (is_game_end() == 3):
            print("Maze Completed")
        elif (is_game_end() == 2):
            print("Out of steps, feels bad")
        elif (is_game_end() == 1):
            print("Out of lives, feels bad")
        command = input()


if __name__ == '__main__':
    start_game(sys.argv)
