from collections import defaultdict
import itertools
import re


def is_valid_position(position: tuple) -> bool:
    row, col = position

    valid_row = row in range(0, len(grid))
    valid_col = col in range(0, len(grid[0]))

    return valid_row and valid_col


def is_alineated(pair) -> bool:
    # Two SEPARATE points define a line in a 2D grid
    fant, sant = pair

    # Extract coordinates
    x1, y1 = fant
    x2, y2 = sant

    dx = x2 - x1
    dy = y2 - y1

    # All non-identical points define a unique line in a 2D grid
    if dx == 0 and dy == 0:
        return False

    return True


def generate_positions_in_line(pair, step=None):

    fant, sant = pair

    # Extract coordinates
    x1, y1 = fant
    x2, y2 = sant

    # Direction vector (dx, dy)
    dx = x2 - x1
    dy = y2 - y1

    # Initialize positions list
    positions = []

    # generate all positions
    if not step:

        # Check positions in both directions by varying t
        t = 0
        while True:
            # Calculate the next position from the first point (fant)
            x_forward = x1 + t * dx
            y_forward = y1 + t * dy

            # Calculate the next position from the second point (sant)
            x_backward = x2 - t * dx
            y_backward = y2 - t * dy

            forward_position = (x_forward, y_forward)
            backward_position = (x_backward, y_backward)

            # Check if positions are inside the grid boundaries
            is_valid_forward = is_valid_position(forward_position)
            is_valid_backward = is_valid_position(backward_position)

            if is_valid_forward:
                positions.append(forward_position)
            if is_valid_backward:
                positions.append(backward_position)

            # If both forward and backward positions are out of bounds, stop
            if not is_valid_forward and not is_valid_backward:
                break

            # Increment t to step to the next position along the line
            t += 1

    else:
        # Generate two new positions from step
        position_from_fant = (x1 + step * dx, y1 + step * dy)
        position_from_sant = (x2 - step * dx, y2 - step * dy)

        if is_valid_position(position_from_fant):
            positions.append(position_from_fant)

        if is_valid_position(position_from_sant):
            positions.append(position_from_sant)

    return positions


with open("puzzle_input.txt", "r") as fil:
    grid = fil.readlines()


grid = [row.strip() for row in grid]
antenna = r"[^.]"

print(f"Detected grid of {len(grid)}x{len(grid[0])}")
antenna_locations = defaultdict(list)

# Populate the dict of antennas
for rowid, row in enumerate(grid):
    antennas = re.finditer(pattern=antenna, string=row)
    antennas = [(match.group(), match.start()) for match in antennas]

    for found_antenna in antennas:
        antenna_locations[found_antenna[0]].append((rowid, found_antenna[1]))


antinodes = set()

for antenna_type, positions in antenna_locations.items():
    antenna_pairs = itertools.combinations(positions, 2)

    for pair in antenna_pairs:
        valid_antinodes = generate_positions_in_line(pair=pair, step=2)
        antinodes.update(valid_antinodes)


print(f"Part 1 answer is {len(antinodes)}")

part2_antinodes = set()

for antenna_type, positions in antenna_locations.items():
    # generate all possible antenna pairs
    antenna_pairs = itertools.combinations(positions, 2)

    for pair in antenna_pairs:
        # find pssible antinodes
        new_antinodes = generate_positions_in_line(pair, step=None)
        part2_antinodes.update(new_antinodes)


print(f"Part 2 answer is {len(part2_antinodes)}")
