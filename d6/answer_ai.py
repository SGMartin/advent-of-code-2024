import copy

# Assume it can be looking at any direction
def find_guard_start_pos(maze: list) -> tuple:
    for rid, row in enumerate(maze):
        for direction in "^v><":
            if direction in row:
                return rid, row.index(direction)
    return None

# Get all of the ids of #
def get_row_obstacle_indices(row):
    return [i for i, c in enumerate(row) if c == "#"]

def find_next_position(maze: list, guard_position, new_direction) -> tuple:
    current_direction = new_direction  # Ignore maze direction; use the new direction directly

    if current_direction == "up":
        for rid, row in enumerate(maze[::-1]):
            non_reversed_rid = len(maze) - 1 - rid
            if non_reversed_rid >= guard_position[0]:
                continue
            if row[guard_position[1]] == "#":
                return non_reversed_rid + 1, guard_position[1]
        return -1, guard_position[1]

    elif current_direction == "down":
        for rid, row in enumerate(maze):
            if rid <= guard_position[0]:
                continue
            if row[guard_position[1]] == "#":
                return rid - 1, guard_position[1]
        return len(maze), guard_position[1]

    elif current_direction == "right":
        obstacles = get_row_obstacle_indices(maze[guard_position[0]])
        obstacles = [n for n in obstacles if n >= guard_position[1]]
        return (guard_position[0], min(obstacles) - 1) if obstacles else (guard_position[0], len(maze[0]))

    else:  # left
        obstacles = get_row_obstacle_indices(maze[guard_position[0]])
        obstacles = [n for n in obstacles if n <= guard_position[1]]
        return (guard_position[0], max(obstacles) + 1) if obstacles else (guard_position[0], -1)

def get_visited_positions(current_pos: tuple, next_pos: tuple) -> set:
    x1, y1 = current_pos
    x2, y2 = next_pos
    if x1 == x2:  # Vertical line
        return {(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)}
    return {(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)}

def adjust_position_to_limits(position, limits):
    x, y = position
    x = max(min(x, limits["bottom"] - 1), limits["top"])
    y = max(min(y, limits["right"] - 1), limits["left"])
    return x, y

with open("puzzle_input.txt", "r") as fil:
    maze = [line.rstrip() for line in fil.readlines()]

# Get maze limits
maze_limits = {
    "top": -1,
    "bottom": len(maze),
    "left": -1,
    "right": len(maze[0])
}

# Directions and rotations
directions = {
    "up": "right",
    "right": "down",
    "down": "left",
    "left": "up"
}

starting_guard_position = find_guard_start_pos(maze)
print(f"Guard position start is {starting_guard_position}")
print(f"Maze limits are {maze_limits}")

# Part 1: Traverse the maze
unique_positions = {starting_guard_position}
current_position = starting_guard_position
current_direction = "up"

while True:
    next_position = find_next_position(maze, current_position, current_direction)
    next_position = adjust_position_to_limits(next_position, maze_limits)

    # Exit condition when the guard leaves the maze
    if next_position == current_position:
        break

    visited_positions = get_visited_positions(current_position, next_position)
    unique_positions.update(visited_positions)

    current_position = next_position
    current_direction = directions[current_direction]

print(f"Part 1 answer: {len(unique_positions)}")

# Part 2: Loop detection
def is_looping_maze(maze, new_obstruction):
    new_maze = copy.deepcopy(maze)
    new_maze[new_obstruction[0]] = new_maze[new_obstruction[0]][:new_obstruction[1]] + "#" + new_maze[new_obstruction[0]][new_obstruction[1] + 1:]

    starting_guard_position = find_guard_start_pos(new_maze)
    current_position = starting_guard_position
    current_direction = "up"

    visited_positions_history = set()

    while True:
        next_position = find_next_position(new_maze, current_position, current_direction)
        next_position = adjust_position_to_limits(next_position, maze_limits)

        if next_position == current_position:
            return False  # No loop

        current_visited_positions = frozenset(get_visited_positions(current_position, next_position))

        if (current_direction, current_visited_positions) in visited_positions_history:
            return True  # Loop detected
        visited_positions_history.add((current_direction, current_visited_positions))

        current_position = next_position
        current_direction = directions[current_direction]

# Remove the starting position from the set of unique positions to test
unique_positions.discard(starting_guard_position)

loops = {pos for pos in unique_positions if is_looping_maze(maze, pos)}
print(f"Part 2 answer is {len(loops)}")