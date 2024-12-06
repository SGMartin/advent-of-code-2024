import copy

# Assume it can be looking at any direction
def find_guard_start_pos(maze: list) -> tuple:
    guard_pos = None

    for rid, row in enumerate(maze):
        if "^" in row:
            col = row.index("^")
            guard_pos = (rid, col)
        elif ">" in row:
            col = row.index(">")
        elif "v" in row:
            col = row.index("v")
        elif "<" in row:
            col = row.index("<")

    return guard_pos

# Get all of the ids of #
def get_row_obstacle_indices(row):
    return [i for i, c in enumerate(row) if c == "#"]




def find_next_position(maze: list, guard_position, new_direction) -> tuple:

    # First get the current guard direction
    current_direction = maze[guard_position[0]][guard_position[1]]
    current_direction = new_direction

    if current_direction == "up":
        for rid, row in enumerate(maze[::-1]):
            non_reversed_rid = maze_limits["bottom"] - 1 - rid
            if non_reversed_rid >= guard_position[0]:
                continue
            if row[guard_position[1]] == "#":
                return (non_reversed_rid + 1, guard_position[1])

        return (maze_limits["top"], guard_position[1])

    elif current_direction == "down":
        for rid, row in enumerate(maze):
            if rid <= guard_position[0]:
                continue
            if row[guard_position[1]] == "#":
                return (rid - 1, guard_position[1])

        return (maze_limits["bottom"], guard_position[1])

    elif current_direction == "right":
        row_left = maze[guard_position[0]]
        obstacles_id = get_row_obstacle_indices(row_left)
        obstacles_id = [n for n in obstacles_id if n >= guard_position[1]]

        if obstacles_id:
            return (guard_position[0], min(obstacles_id) - 1)
        else:
            return (guard_position[0], maze_limits["right"])

    else:
        row_left = maze[guard_position[0]]
        obstacles_id = get_row_obstacle_indices(row_left)
        obstacles_id = [n for n in obstacles_id if n <= guard_position[1]]

        if obstacles_id:
            return (guard_position[0], max(obstacles_id) + 1)
        else:
            return (guard_position[0], maze_limits["left"])


def get_visited_positions(current_pos: tuple, next_pos: tuple) -> set:
    x1, y1 = current_pos
    x2, y2 = next_pos

    if x1 == x2:  # Vertical line
        return {(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)}
    else:  # Horizontal line
        return {(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)}


with open("puzzle_input.txt", "r") as fil:
    raw_maze = fil.readlines()

maze = [row.rstrip() for row in raw_maze]

# Find the starting guard position
starting_guard_position = find_guard_start_pos(maze)

# Get maze limits, for reference
maze_limits = {
    "top": -1,
    "bottom": len(maze),
    "left": -1,
    "right": len(maze[0])
    }

# next directions. Always 90 clockwise
directions = {
    "up": "right",
    "right": "down",
    "down": "left",
    "left": "up"
}


print(f"Guard position start is {starting_guard_position}")
print(f"Maze limits are {maze_limits}")

# Part 1: start traversal
unique_positions = set()
unique_positions.add(starting_guard_position)

current_position = starting_guard_position

# Guard always start with "UP"
current_direction = "up"

while True:
    overlimit = False
    next_position = find_next_position(
        maze,
        current_position,
        current_direction
        )

    # Check if we went out of the maze
    if (next_position[0] not in range(0, maze_limits["bottom"])) or (next_position[1] not in range(0, maze_limits["right"])):
        # reset positition to be in range
        if next_position[0] >= maze_limits["bottom"]:
            next_position = (maze_limits["bottom"] - 1, next_position[1])
        elif next_position[0] <= maze_limits["top"]:
            next_position = (maze_limits["top"] + 1, next_position[1])
        elif next_position[1] > maze_limits["right"]:
            next_position = (next_position[0], maze_limits["right"] - 1)
        else:
            next_position = (next_position[0], maze_limits["left"] + 1)

        overlimit = True

    visited_positions = get_visited_positions(
        current_pos=current_position,
        next_pos=next_position
        )

    # Update the set of positions
    unique_positions.update(visited_positions)

    if overlimit:
        break

    # Set the new direction
    current_position = next_position
    current_direction = directions[current_direction]


print(f"Part 1 answer: {len(unique_positions)}")


# Now we have to get him stuck in a loop
def is_looping_maze(maze, new_obstruction):

    new_maze = copy.deepcopy(maze)
    maze_row = new_maze[new_obstruction[0]]

    new_maze_row = maze_row[:new_obstruction[1]] + "#" + maze_row[new_obstruction[1] + 1:]
    new_maze[new_obstruction[0]] = new_maze_row

    starting_guard_position = find_guard_start_pos(new_maze)
    current_position = starting_guard_position

    # Guard always start with "UP"
    current_direction = "up"

    visited_positions_history = set()

    while True:

        next_position = find_next_position(
            new_maze,
            current_position,
            current_direction
            )

        # Check if we went out of the maze
        if (next_position[0] not in range(0, maze_limits["bottom"])) or (next_position[1] not in range(0, maze_limits["right"])):
            # reset positition to be in range
            if next_position[0] >= maze_limits["bottom"]:
                next_position = (maze_limits["bottom"] - 1, next_position[1])
            elif next_position[0] <= maze_limits["top"]:
                next_position = (maze_limits["top"] + 1, next_position[1])
            elif next_position[1] > maze_limits["right"]:
                next_position = (next_position[0], maze_limits["right"] - 1)
            else:
                next_position = (next_position[0], maze_limits["left"] + 1)

            return False

        current_visited_positions = frozenset(get_visited_positions(
            current_pos=current_position,
            next_pos=next_position
        ))

        direction_and_positions = (current_direction, current_visited_positions)


        # Check if the tuple already exists in the set (indicating a loop)
        if direction_and_positions in visited_positions_history:
            return True  # Loop detected
        else:
            visited_positions_history.add(direction_and_positions)

        current_position = next_position
        current_direction = directions[current_direction]

# Remove the starting pos since we cannot put obstacle there
unique_positions.remove(starting_guard_position)

# Test if obstructing along any unique position makes a loop
loops = set()

for pid, pos in enumerate(unique_positions):
    if is_looping_maze(maze, pos):
        loops.add(pos)

print(f"Part 2 answer is {len(loops)}")
