with open("puzzle_input.txt", "r") as fil:
    stones = [int(stone) for stone in fil.readline().split()]


def count_stones(stones, blinks):
    # Let's try to simulate unique values and not stones
    stones = dict.fromkeys(stones, 1)

    for blink in range(blinks):
        new_stones = {}
        for stone_number, n_appearances in stones.items():
            # Add 1 to the dict
            if stone_number == 0:
                new_stones[1] = new_stones.get(1, 0) + n_appearances
            # Even num
            elif len(str(stone_number)) % 2 == 0:
                # split stone in two
                stone_value = str(stone_number)
                stone_1, stone_2 = int(stone_value[:len(stone_value)//2]), int(stone_value[len(stone_value)//2:])

                new_stones[stone_1] = new_stones.get(stone_1, 0) + n_appearances
                new_stones[stone_2] = new_stones.get(stone_2, 0) + n_appearances
            else:
                new_stone_value = stone_number * 2024
                new_stones[new_stone_value] = new_stones.get(new_stone_value, 0) + n_appearances

        # Remove stones with 0 occurrences and update `stones`
        stones = {k: v for k, v in new_stones.items() if v > 0}

    return sum(stones.values())

blinks = 25
print(f"Part 1 answer is {count_stones(stones, blinks)} stones after {blinks} blinks")
blinks = 75
print(f"Part 2 answer is {count_stones(stones, blinks)} stones after {blinks} blinks")