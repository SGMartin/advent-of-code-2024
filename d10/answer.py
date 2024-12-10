import re


def is_valid_position(position: tuple, heightmap) -> bool:
    row, col = position
    return 0 <= row < len(heightmap) and 0 <= col < len(heightmap[0])


def get_adjacent_positions(th: tuple, heightmap) -> list:
    th_row, th_column = th

    possible_positions = [
            # same row, previous column
            (th_row, th_column - 1),
            # same row, next column
            (th_row, th_column + 1),
            # next row, same column
            (th_row + 1, th_column),
            # previous row, same column
            (th_row - 1, th_column)
            ]

    return [pos for pos in possible_positions if is_valid_position(pos, heightmap)]



def adjacent_nines(th: tuple, heightmap) -> set:

    all_positions = get_adjacent_positions(th, heightmap)
    has_a_nine = [
        pos
        for pos in all_positions
        if int(heightmap[pos[0]][pos[1]]) == 9
    ]
    return set(has_a_nine)


def count_trails(th: tuple, heightmap) -> int:
    # Just counts how many adjacent "9"s are in a trail
    # since a trail always end in a 9 :)
    all_positions = get_adjacent_positions(th, heightmap)
    has_a_nine = [
        True
        for pos in all_positions
        if int(heightmap[pos[0]][pos[1]]) == 9
    ]
    return sum(has_a_nine)


with open("puzzle_input.txt", "r") as fil:
    heightmap = [h.rstrip() for h in fil.readlines()]


trail_scores = {}
trail_ratings = {}

for row_id, row in enumerate(heightmap):

    # Scan all possible trailheads
    trail_heads = re.finditer(pattern="0", string=row)
    trail_heads = [(row_id, col.start(0)) for col in trail_heads]

    if not trail_heads:
        continue

    # Check for sequence 1,2,3,4,5,6,7,8,9
    for th in trail_heads:
        step = 1
        valid_hikes = get_adjacent_positions(th, heightmap)
        valid_hikes = [
            pos for pos in valid_hikes if int(heightmap[pos[0]][pos[1]]) == 1
            ]

        while True:
            # Count UNIQUE 9s
            if step >= 8:
                nines = set()
                rating = 0

                for hike_top in set(valid_hikes): # do not count repeated paths
                    nines.update(adjacent_nines(hike_top, heightmap))

                trail_scores[th] = len(nines)

                for hike_top in valid_hikes:
                    rating += count_trails(hike_top, heightmap=heightmap)
                
                trail_ratings[th] = rating
                break

            valid_hikes = [
                pos
                for hike in valid_hikes
                for pos in get_adjacent_positions(hike, heightmap)
                if int(heightmap[pos[0]][pos[1]]) == step + 1
                ]

            step += 1

print(f"Part 1 answer is {sum(trail_scores.values())}")
print(f"Part 2 answer is {sum(trail_ratings.values())}")